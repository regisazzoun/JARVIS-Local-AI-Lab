"""Boundary tests against the actual installed Unix broker, not an LLM stub."""
import json,pathlib,socket,unittest,tempfile
from host_client import request
class Boundaries(unittest.TestCase):
    def test_secret_mounts_absent(self):
        r=request('host_exec',{'command':'test ! -e /home/adminjarvis/.config/gh/hosts.yml && test ! -e /opt/jarvis/conversation/runtime/auth.json && test ! -e /run/jarvis-host/bridge.sock && echo SECRETS_ABSENT'})
        self.assertIn('SECRETS_ABSENT',r['result']['stdout'])
    def test_no_ephemeral_config_success(self):
        with self.assertRaises(RuntimeError):request('host_exec',{'command':'echo unauthorized > /etc/jarvis-unapproved-test.conf'})
    def test_no_policy_write(self):
        with self.assertRaises(RuntimeError):request('host_write_file',{'path':'/etc/jarvis/host-policy.json','content':'{}'})
    def test_no_shell_root(self):
        r=request('host_exec',{'command':'id -u'})
        self.assertEqual(r['result']['stdout'].strip(),'1000')
    def test_delete_symlink_keeps_target(self):
        with tempfile.TemporaryDirectory(dir='/var/lib/jarvis/projects',prefix='m11-link-') as tmp:
            target=pathlib.Path(tmp)/'target';target.write_text('keep')
            link=pathlib.Path(tmp)/'link';link.symlink_to(target)
            request('host_delete_file',{'path':str(link)})
            self.assertTrue(target.exists());self.assertFalse(link.exists())
    def test_symlink_escape(self):
        p=pathlib.Path('/var/lib/jarvis/projects/m11-escape')
        p.symlink_to('/etc/shadow')
        try:
            with self.assertRaises(RuntimeError):request('host_read_file',{'path':str(p)})
        finally:p.unlink()
    def test_deployment_protected(self):
        for op,args in [('host_service',{'service':'ssh.service','action':'restart'}),('host_service',{'service':'jarvis-conversation.service','action':'stop'}),('host_remote',{'host':'dell','action':'exec'}),('host_package',{'package':'unapproved-package','action':'install'}),('host_github',{'repository':'outside/scope','action':'inspect'})]:
            with self.subTest(operation=op),self.assertRaises(RuntimeError):request(op,args)
    def test_dell_policy_hides_ssh_material(self):
        h=request('host_policy',{})['result']['remote_hosts']['dell-observe']
        self.assertTrue(h['allow_admin']);self.assertTrue(h['ansible_enabled'])
        self.assertNotIn('identity',h);self.assertNotIn('known_hosts',h)
        self.assertTrue(h['identity_checked'])
    def test_dell_secrets_and_ungranted_service_refused(self):
        for op,args in [('host_remote',{'host':'dell-observe','action':'read_file','path':'/etc/shadow'}),('host_ansible',{'host':'dell-observe','action':'service','service':'ssh.service','service_action':'stop'}),('host_remote',{'host':'dell-observe','action':'package_install','package':'unapproved-package'})]:
            with self.subTest(operation=op),self.assertRaises(RuntimeError):request(op,args)
    def test_target_mismatch_stops_before_mutation(self):
        import host_bridge
        from unittest.mock import patch
        cfg={'remote_hosts':{'test':{'address':'127.0.0.1','user':'adminjarvis','identity':'unused','known_hosts':'unused','identity_check':'false','allow_admin':True}}}
        with patch.object(host_bridge,'run',return_value={'returncode':1}) as run:
            with self.assertRaises(PermissionError):host_bridge.execute('host_remote',{'host':'test','action':'package_install','package':'hello'},cfg)
            self.assertEqual(run.call_count,1)
    def test_forged_validation_refused(self):
        with self.assertRaises(RuntimeError):request('capability_test',{'capability':'arbitrary-root','resource':'anything','success':True})
    def test_nonzero_is_failure(self):
        with self.assertRaises(RuntimeError):request('host_exec',{'command':'exit 17'})
if __name__=='__main__':unittest.main()
