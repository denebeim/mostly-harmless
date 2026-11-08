import copy,importlib.util,json,os,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('manage_vm',ROOT/'roles/proxmox/create_vm/files/manage_vm.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class VMTests(unittest.TestCase):
    def fixture(self):
        spec={'name':'fixture','id':8314,'ip':'192.168.42.250','tags':[]}
        conf={'name':'fixture','cores':2,'memory':2048,'cpu':'host','agent':'enabled=1,fstrim_cloned_disks=1','ciupgrade':0,'vga':'serial0','serial0':'socket','boot':'order=scsi0','ipconfig0':'gw=192.168.42.1,ip=192.168.42.250/24','nameserver':'192.168.42.2','searchdomain':'local.deepthot.org','net0':'virtio=AA:BB:CC:DD:EE:FF,bridge=vmbr0','scsi0':'heartogold:8314/root,size=12G'}
        calls=[]
        def run(*args):
            calls.append(args)
            if args[:3]==('pvesh','get','/cluster/resources'):return json.dumps([{'vmid':8314,'name':'fixture','node':'heartogold'}])
            if args[:2]==('pvesh','get'):return json.dumps(conf)
            if args[:2]==('qm','status'):return 'status: running'
            if args[:2]==('qm','set'):return ''
            raise AssertionError(args)
        return spec,conf,calls,run

    def test_existing_vm_is_unchanged_and_mac_preserved(self):
        spec,conf,calls,run=self.fixture()
        with patch.object(module,'run',run):result=module.main(spec)
        self.assertFalse(result['changed']);self.assertEqual(result['mac'],'AA:BB:CC:DD:EE:FF')
        self.assertFalse(any(c[:2] in [('qm','set'),('qm','resize')] for c in calls))

    def test_vm_id_collision_aborts_without_mutation(self):
        spec,conf,calls,run=self.fixture();spec['name']='other'
        with patch.object(module,'run',run),self.assertRaises(ValueError):module.main(spec)
        self.assertEqual(len(calls),1)

    def test_larger_existing_disk_is_not_shrunk(self):
        spec,conf,calls,run=self.fixture();conf['scsi0']='heartogold:8314/root,size=40G'
        with patch.object(module,'run',run):result=module.main(spec)
        self.assertFalse(result['changed']);self.assertFalse(any(c[:2]==('qm','resize') for c in calls))

    def test_new_tag_changes_only_the_tag_setting(self):
        spec,conf,calls,run=self.fixture();spec['tags']=['docker']
        with patch.object(module,'run',run):self.assertTrue(module.main(spec)['changed'])
        changes=[c for c in calls if c[:2]==('qm','set')]
        self.assertEqual(changes,[('qm','set','8314','--tags','docker')])

    def test_secret_and_private_pem_are_redacted_before_logging(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'session.log';env=dict(os.environ,DEEPTHOT_SESSION_LOG=str(path),TEST_API_KEY='fixture-secret-123456')
            cmd=['python3',str(ROOT/'scripts/log-session.py'),'python3','-c',"print('fixture-secret-123456');print('-----BEGIN PRIVATE KEY-----');print('private-material');print('-----END PRIVATE KEY-----');print('safe-ip 192.168.42.132')"]
            r=subprocess.run(cmd,env=env,capture_output=True,text=True,check=True)
            for text in (r.stdout,path.read_text()):
                self.assertNotIn('fixture-secret-123456',text);self.assertNotIn('\nprivate-material\n',text);self.assertIn('safe-ip 192.168.42.132',text)

if __name__=='__main__':unittest.main()
