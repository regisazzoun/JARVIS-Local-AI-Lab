import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch
from jarvis.launcher_api import Launcher


class PrivateAudioArtifact(unittest.TestCase):
    def test_reads_wav_but_rejects_fake_wav_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            allowed=Path(root);api=Launcher.__new__(Launcher)
            audio=allowed/'sample.wav'
            with wave.open(str(audio),'wb') as wav:
                wav.setparams((1,2,24000,0,'NONE','not compressed'));wav.writeframes(b'\0\0'*240)
            with patch('jarvis.launcher_api.PROJECTS_ROOT',allowed):
                self.assertEqual(api.artifact(str(audio)),audio.read_bytes())
                fake=allowed/'fake.wav';fake.write_bytes(b'not an audio file')
                with self.assertRaises(ValueError):api.artifact(str(fake))
                secret=Path(outside)/'secret.wav';secret.write_bytes(audio.read_bytes())
                link=allowed/'escape.wav';link.symlink_to(secret)
                with self.assertRaises(PermissionError):api.artifact(str(link))
                private=allowed/'private';private.mkdir();hidden=private/'sample.wav';hidden.write_bytes(audio.read_bytes())
                with self.assertRaises(PermissionError):api.artifact(str(hidden))
