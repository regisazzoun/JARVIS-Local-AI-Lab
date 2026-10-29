import unittest
import sys
import os

# Ensure engine is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jarvis.mission_store import MissionStore
from jarvis.attempt_ledger import AttemptLedger
from jarvis.authority_attempts import AuthorityAttempts


class TestAuthorityLedgerIntegration(unittest.TestCase):
    """Test unitaire ciblé du raccordement entre Authority.work et le ledger durable."""

    def test_authority_leverages_attempt_ledger(self):
        """Vérifie que AuthorityAttempts relie Authority au ledger."""
        # Création d'un environnement temporaire isolé
        temp_dir = '/tmp/jarvis_test_integration'
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Instanciation réelle des composants
            store = MissionStore(local=temp_dir, m='test-mission')
            ledger = AttemptLedger(store=store)
            authority = AuthorityAttempts(store=store, ledger=ledger)

            # Vérification des attributs clés
            self.assertIsNotNone(authority.store, "Authority doit avoir un store")
            self.assertIsNotNone(authority.ledger, "Authority doit avoir un ledger")
            self.assertIs(authority.ledger, ledger, "Le ledger doit être celui fourni")

            # Vérification que les méthodes attendues existent
            self.assertTrue(hasattr(authority, 'work'), "Authority doit avoir une méthode work")
            self.assertTrue(hasattr(ledger, 'add'), "AttemptLedger doit avoir une méthode add")

        finally:
            # Nettoyage
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
