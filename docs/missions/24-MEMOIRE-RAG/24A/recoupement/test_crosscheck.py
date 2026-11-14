"""Offline controller regressions using synthetic sources; no network or index."""
import asyncio
import copy
import importlib.util
import pathlib
import sys
import unittest
import io
import json
from unittest.mock import patch

ROOT = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location('provenance24a', ROOT/'provenance24a.py')
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)
sys.modules['open_webui.utils.provenance24a'] = provenance
import crosscheck24a as controller

QUESTION = 'Drive Éducation : téléphonie salle 99, réseau, IPBX, téléphones, SIP, appels, reste à faire.'
FILES = [
    {'id': 'synthetic-network-001', 'name': 'Salle 99 — Architecture réseau', 'modifiedTime': '2026-11-12'},
    {'id': 'synthetic-ipbx-001', 'name': 'FusionPBX — Installation et exploitation', 'modifiedTime': '2026-11-13'},
    {'id': 'synthetic-deployment-001', 'name': 'Salle-99-Documentation-deploiement.md', 'modifiedTime': '2026-11-13'},
]
for source in FILES:
    source['mimeType'] = 'text/markdown' if source['name'].endswith('.md') else 'application/vnd.google-apps.document'
TOOLS = {name: {'tool_id': 'server:jarvis-standard-mcp'} for name in
         ('tool_education_drive_search_post', 'tool_education_docs_get_text_post')}
TEXT = 'Observation 13/11/2026. VLAN réseau. FusionPBX FreeSWITCH. Téléphones physiques. SIP enregistré. Appels audio. Recette à faire.'


class ControllerTests(unittest.IsolatedAsyncioTestCase):
    async def simulate(self, failed_id=None, missing_family=None, text=TEXT):
        calls = []
        async def invoke(name, args):
            calls.append((name, args))
            if 'search' in name:
                files = [f for f in FILES if f['id'] != missing_family]
                return ({'returncode': 0, 'remote_access_verified': True,
                         'content': [{'files': files + files}]}, {})
            if args['documentId'] == failed_id:
                return ({'returncode': 1, 'mcp_is_error': True, 'content': [{'error': 'denied'}]}, {})
            raw = {'returncode': 0, 'remote_access_verified': True, 'content': [{'text': text}]}
            meta = {f['id']: f for f in FILES}
            return (provenance.enrich_document(raw, args, meta), {})
        result = await controller.run(QUESTION, TOOLS, invoke)
        return result, calls

    async def test_bounded_three_distinct_reads_before_synthesis(self):
        result, calls = await self.simulate()
        self.assertEqual('ready', result['status'])
        self.assertEqual(5, len(calls))
        self.assertTrue(all('search' in name for name, _ in calls[:2]))
        self.assertEqual(3, len(result['sources']))
        self.assertEqual(3, len({r['provenance']['id'] for r in result['reads']}))
        self.assertTrue(all(result['evidence'].values()))
        self.assertFalse(result['persistent_index_written'])

    async def test_failed_read_never_counts_as_family(self):
        result, _ = await self.simulate(failed_id=FILES[1]['id'])
        self.assertEqual('incomplete', result['status'])
        self.assertIn('ipbx', result['missing_families'])
        self.assertEqual(2, len(result['sources']))

    async def test_missing_candidate_is_explicit_gap(self):
        result, _ = await self.simulate(missing_family=FILES[0]['id'])
        self.assertEqual('incomplete', result['status'])
        self.assertIn('reseau', result['missing_families'])

    async def test_missing_topic_prevents_ready(self):
        result, _ = await self.simulate(text='Source sans couverture technique.')
        self.assertEqual('incomplete', result['status'])
        self.assertIn('sip', result['missing_topics'])

    async def test_no_authorized_tools_no_calls(self):
        async def forbidden(*args):
            self.fail('An unauthorized tool was invoked')
        result = await controller.run(QUESTION, {}, forbidden)
        self.assertEqual('tools_not_authorized', result['status'])

    async def test_foreign_connection_no_calls(self):
        async def forbidden(*args):
            self.fail('A foreign connection was invoked')
        tools = copy.deepcopy(TOOLS)
        for tool in tools.values():
            tool['tool_id'] = 'server:someone-else'
        self.assertEqual('tools_not_authorized', (await controller.run(QUESTION, tools, forbidden))['status'])

    async def test_request_isolation(self):
        first, _ = await self.simulate()
        second, _ = await self.simulate(failed_id=FILES[1]['id'])
        self.assertEqual('ready', first['status'])
        self.assertEqual('incomplete', second['status'])

    async def test_large_document_explicitly_not_truncated(self):
        result, _ = await self.simulate(text=TEXT * 500)
        self.assertEqual('incomplete', result['status'])
        self.assertEqual([], result['sources'])

    async def test_fabricated_scope_fails_exact_quote_check(self):
        result, _ = await self.simulate()
        proposed = {topic: [{'source': family, 'quote': TEXT} for family in required]
                    for topic, required in controller.REQUIRED_EVIDENCE.items()}
        proposed['telephones'][0]['quote'] = 'Tous les téléphones sont physiquement sur le même banc.'
        _, rejected, missing = controller.validate_quotes(result, proposed)
        self.assertTrue(rejected)
        self.assertIn('telephones', missing)

    async def test_required_cross_source_comparison_cannot_be_skipped(self):
        result, _ = await self.simulate()
        proposed = {topic: [{'source': 'ipbx', 'quote': TEXT}] for topic in controller.TOPICS}
        _, _, missing = controller.validate_quotes(result, proposed)
        self.assertIn('sip', missing)
        self.assertIn('telephones', missing)

    async def test_sip_history_cannot_replace_physical_registration_state(self):
        result, _ = await self.simulate()
        history = 'Le problème initial de timeout empêchait le téléphone de s’enregistrer.'
        result['reads'][1]['text'] += '\n' + history
        proposed = {topic: [{'source': family, 'quote': TEXT} for family in required]
                    for topic, required in controller.REQUIRED_EVIDENCE.items()}
        proposed['sip'] = [{'source': 'reseau', 'quote': TEXT}, {'source': 'ipbx', 'quote': history}]
        _, rejected, missing = controller.validate_quotes(result, proposed)
        self.assertTrue(rejected)
        self.assertEqual(['ipbx'], missing['sip'])

    async def test_exact_quoted_answer_rendered_without_free_claims(self):
        result, _ = await self.simulate()
        proposed = {topic: [{'source': family, 'quote': TEXT} for family in required]
                    for topic, required in controller.REQUIRED_EVIDENCE.items()}
        class FakeResponse(io.StringIO):
            pass
        selection = {topic: [{'source': family, 'passage_ids': [0]} for family in required] for topic, required in controller.REQUIRED_EVIDENCE.items()}
        response = {'message': {'content': json.dumps(selection)}, 'done_reason': 'stop'}
        with patch('urllib.request.urlopen', return_value=FakeResponse(json.dumps(response))):
            await controller.quoted_report(result)
        self.assertEqual('ready', result['status'])
        self.assertEqual({}, result['quote_check']['missing_required_evidence'])
        self.assertIn(TEXT, result['answer'])
        self.assertIn('Sources effectivement lues', result['answer'])

    async def test_invalid_model_passage_abstains(self):
        result, _ = await self.simulate()
        response = {'message': {'content': json.dumps({topic: [] for topic in controller.TOPICS})}}
        with patch('urllib.request.urlopen', return_value=io.StringIO(json.dumps(response))):
            await controller.quoted_report(result)
        self.assertEqual('unverified_quotes', result['status'])
        self.assertIn('non validé', result['answer'])

    async def test_unknown_passage_id_abstains(self):
        result, _ = await self.simulate()
        selected = {topic: [{'source': 'ipbx', 'passage_ids': [999999]}] for topic in controller.TOPICS}
        response = {'message': {'content': json.dumps(selected)}}
        with patch('urllib.request.urlopen', return_value=io.StringIO(json.dumps(response))):
            await controller.quoted_report(result)
        self.assertEqual('unverified_quotes', result['status'])
        self.assertTrue(result['quote_check']['rejected'])

    def test_passages_preserve_source_words(self):
        text = 'Un passage de source suffisamment long.\n\nUn autre passage, avec sa propre portée.'
        self.assertTrue(all(p['text'] in controller.normalized(text) for p in controller.passages(text)))

    def test_unrelated_question_does_not_activate(self):
        self.assertIsNone(controller.pilot_room('Quel temps fait-il ?'))
        self.assertEqual('99', controller.pilot_room(QUESTION))

    def test_selection_does_not_use_known_document_ids(self):
        selected = controller.choose_sources(FILES + [
            {'id': 'unrelated-network-001', 'name': 'Salle 12 — Architecture réseau', 'modifiedTime': '2027-01-01'}], '99')
        self.assertEqual(FILES[0]['id'], selected['reseau']['id'])

    def test_newer_spreadsheet_cannot_replace_readable_document(self):
        selected = controller.choose_sources(FILES + [
            {'id': 'synthetic-inventory-001', 'name': 'Inventaire-provisionnement-salle-99.xlsx',
             'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
             'modifiedTime': '2027-01-01'}], '99')
        self.assertEqual(FILES[2]['id'], selected['deploiement']['id'])


if __name__ == '__main__':
    unittest.main()
