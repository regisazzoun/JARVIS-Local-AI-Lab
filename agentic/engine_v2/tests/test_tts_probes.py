import json
from pathlib import Path
import sys
import io
import tempfile
import wave
import zipfile
import subprocess
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]/'broker'))
from remote_project import project_program
from remote_probes import probe_command,PROBES
from jarvis.verification import Verifier,validate_contract


class FixedIndependentProbes(unittest.TestCase):
    def test_sample_probe_rejects_silence_wrong_text_and_false_duration(self):
        # Synthetic PCM is a verifier fixture, never a TTS reception sample.
        import array,os,contextlib
        texts=["Bonsoir monsieur. Tous les systèmes sont opérationnels. Je suis prêt à recevoir vos instructions.","L'analyse du serveur est terminée. Le processeur graphique fonctionne normalement et les services de communication sont disponibles.","J'ai examiné votre demande. Plusieurs solutions sont envisageables. Souhaitez-vous que je vous présente celle qui me paraît la plus efficace ?"]
        for mutation in ('none','silence','text','duration'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);(root/'generated').mkdir();rows=[]
                for name,text in zip(['accueil.wav','diagnostic.wav','conversation.wav'],texts):
                    with wave.open(str(root/'generated'/name),'wb') as w:
                        w.setparams((1,2,8000,0,'NONE','not compressed'));w.writeframes(array.array('h',[0 if mutation=='silence' else 1000]*8000).tobytes())
                    rows.append({'file':name,'text':text,'t_gen_s':.2,'load_time_s':1,'duree_audio_s':1,'rtf':.2,'engine_version':'fixture','model_id':'Qwen/fixture','speaker':'Ryan'})
                if mutation=='text':rows[0]['text']='Wrong words'
                if mutation=='duration':rows[0]['duree_audio_s']=2
                (root/'generated/MESURES_PERFORMANCES.json').write_text(json.dumps({'samples':rows}))
                old=os.getcwd();output=io.StringIO()
                try:
                    os.chdir(root)
                    with patch('importlib.metadata.version',return_value='fixture'),contextlib.redirect_stdout(output):exec(compile(PROBES['tts_samples'][1],'fixed-test-probe','exec'),{})
                finally:os.chdir(old)
                self.assertEqual(json.loads(output.getvalue())['pass'],mutation=='none')

    def test_project_probe_is_accepted_but_arbitrary_execution_is_not(self):
        class Registry:
            def execute(self,name,args):
                assert name=='host_remote' and args['action']=='project_probe'
                return {'ok':True,'result':{'returncode':0,'stdout':json.dumps({'cuda_available':True,'cuda_tensor_sum':6.0})}}
        contract={'kind':'json','source':{'tool':'host_remote','arguments':{'host':'dell-observe','action':'project_probe','project':'tts-01','probe':'tts_runtime'}},'expected':{'/cuda_tensor_sum':6.0}}
        self.assertEqual(Verifier(Registry()).verify(contract)['status'],'PASS')
        bad={**contract,'source':{'tool':'host_remote','arguments':{'action':'project_exec','command':'touch result'}}}
        with self.assertRaises(ValueError):validate_contract(bad)

    def test_fixed_names_have_no_shell_injection_parameter(self):
        with self.assertRaises(ValueError):probe_command('/opt/jarvis-lab/tts-01','gpu_inventory; touch /bad')
        command=probe_command('/opt/jarvis-lab/tts-01','tts_runtime')
        self.assertIn('venv/bin/python',command)

    def test_probe_project_mount_is_read_only(self):
        script=project_program('/opt/jarvis-lab/tts-01','true',True,readonly=True)
        with patch('pathlib.Path.mkdir'),patch('pathlib.Path.glob',return_value=[]),patch('subprocess.call',return_value=0) as call:
            with self.assertRaises(SystemExit):exec(compile(script,'probe-runtime','exec'),{})
        argv=call.call_args.args[0];index=argv.index('/opt/jarvis-lab/tts-01')
        self.assertEqual(argv[index-1],'--ro-bind')

    def test_archive_probe_measures_pcm_and_excludes_appledouble(self):
        body=io.BytesIO()
        with wave.open(body,'wb') as wav:
            wav.setparams((1,2,8000,0,'NONE','not compressed'))
            wav.writeframes(b'\xff\x7f\x00\x80\x00\x00\x01\x00')
        with tempfile.TemporaryDirectory() as root:
            with zipfile.ZipFile(Path(root)/'references.zip','w') as z:
                z.writestr('a.wav',body.getvalue());z.writestr('__MACOSX/._a.wav',b'not an audio file')
            result=subprocess.run([sys.executable,'-c',PROBES['archive_inventory'][1]],cwd=root,capture_output=True,text=True,check=True)
        observed=json.loads(result.stdout)
        self.assertEqual(observed['wav_files'],1)
        self.assertEqual(observed['full_scale_samples_total'],2)
        self.assertEqual(observed['files'][0]['pcm_bit_rate_bps'],128000)
        self.assertAlmostEqual(observed['total_duration_s'],4/8000)
        self.assertLess(observed['files'][0]['rms_dbfs'],0)
