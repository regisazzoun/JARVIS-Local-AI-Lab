"""Offline regression cases; synthetic content only. Run beside provenance24a.py."""
import copy
import unittest
from provenance24a import citation_sources, enrich_document, result_failed


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.ident = 'synthetic-document-12345'
        self.raw = {'returncode': 0, 'remote_access_verified': True,
                    'content': [{'text': 'Observation dated 2026-11-12.'}]}
        self.read = enrich_document(copy.deepcopy(self.raw), {'documentId': self.ident},
            {self.ident: {'name': 'Synthetic', 'mimeType': 'application/vnd.google-apps.document',
                         'modifiedTime': '2026-11-14T00:00:00Z'}})

    def test_provenance_and_unchanged_content(self):
        p = self.read['provenance_24a']
        self.assertEqual(self.raw['content'], self.read['content'])
        self.assertEqual(64, len(p['content_sha256']))
        self.assertEqual('2026-11-14T00:00:00Z', p['modified_time'])
        self.assertIn('2026-11-12', p['excerpt'])
        self.assertIn('/document/d/', p['url'])
        self.assertTrue(citation_sources(self.read))

    def test_failure_or_unverified_never_cited(self):
        for patch in ({'returncode': 1}, {'mcp_is_error': True},
                      {'remote_access_verified': False}, {'content': [{'error': 'denied'}]}):
            with self.subTest(patch=patch):
                self.assertFalse(citation_sources({**self.read, **patch}))

    def test_http_success_does_not_override_receipt(self):
        self.assertTrue(result_failed({'returncode': 1}))
        self.assertTrue(result_failed({'content': [{'isError': True}]}))
        self.assertFalse(result_failed(self.raw))

    def test_unknown_dates_stay_unknown(self):
        result = enrich_document(copy.deepcopy(self.raw), {'documentId': self.ident}, {})
        self.assertIsNone(result['provenance_24a']['modified_time'])

    def test_invalid_id_not_promoted(self):
        self.assertNotIn('provenance_24a', enrich_document(self.raw, {'documentId': 'bad/url'}, {}))

    def test_search_not_document_read(self):
        self.assertEqual([], citation_sources({'returncode': 0, 'content': [{'files': []}]}))


if __name__ == '__main__':
    unittest.main()
