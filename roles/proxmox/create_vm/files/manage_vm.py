#!/usr/bin/python3
"""Converge a declared VM without touching other guests or shrinking disks."""
import ipaddress,json,re,subprocess,sys

def run(*args):
    return subprocess.run(list(args),check=True,capture_output=True,text=True).stdout.strip()

def main(spec):
    vmid=int(spec['id']);name=spec['name'];node=spec.get('node','heartogold')
    if vmid < 100 or not re.fullmatch(r'[a-z][a-z0-9-]+',name):raise ValueError('Invalid VM identity')
    ip=ipaddress.ip_interface(spec['ip'] if '/' in spec['ip'] else spec['ip']+'/24')
    resources=json.loads(run('pvesh','get','/cluster/resources','--type','vm','--output-format','json'))
    target=next((v for v in resources if v.get('vmid')==vmid),None)
    if target and (target.get('name')!=name or target.get('node')!=node):raise ValueError('VM ID belongs to another guest')
    if any(v.get('name')==name and v.get('vmid')!=vmid for v in resources):raise ValueError('VM name belongs to another ID')
    created=target is None;changed=False
    if created:
        template=next(v for v in resources if v.get('name')==spec.get('template','deepthot-24-04') and v.get('template')==1)
        run('qm','clone',str(template['vmid']),str(vmid),'--name',name,'--full','1','--storage',spec.get('storage','heartogold'),'--format','qcow2');changed=True
    cfg=json.loads(run('pvesh','get',f'/nodes/{node}/qemu/{vmid}/config','--output-format','json'))
    desired={'name':name,'cores':spec.get('cores',2),'memory':spec.get('memory',2048),'cpu':'host','agent':'enabled=1,fstrim_cloned_disks=1','ciupgrade':0,'vga':'serial0','serial0':'socket','boot':'order=scsi0','ipconfig0':f"gw={spec.get('gateway','192.168.42.1')},ip={ip}",'nameserver':spec.get('dns','192.168.42.2'),'searchdomain':spec.get('domain','local.deepthot.org')}
    if 'tags' in spec:desired['tags']=';'.join(sorted(spec['tags']))
    for key in ('bios','machine'):
        if key in spec:desired[key]=spec[key]
    for key,value in spec.get('hostpci',{}).items():desired[key]=value
    update={k:v for k,v in desired.items() if str(cfg.get(k,''))!=str(v)}
    if spec.get('bios')=='ovmf' and 'efidisk0' not in cfg:
        update['efidisk0']=spec.get('storage','heartogold')+':0,efitype=4m,pre-enrolled-keys=0'
    if update:
        args=['qm','set',str(vmid)]
        for key,value in update.items():args += ['--'+key,str(value)]
        run(*args);changed=True
    def size(value):
        match=re.search(r'(?:^|,)size=(\d+(?:\.\d+)?)([KMGTP])',value)
        if not match:raise ValueError('Cannot determine root disk size')
        return float(match[1])*1024**('KMGTP'.index(match[2])+1)
    wanted=spec.get('disk','12G')
    if size('size='+wanted)>size(cfg['scsi0']):run('qm','resize',str(vmid),'scsi0',wanted);changed=True
    if run('qm','status',str(vmid))!='status: running':run('qm','start',str(vmid));changed=True
    cfg=json.loads(run('pvesh','get',f'/nodes/{node}/qemu/{vmid}/config','--output-format','json'))
    mac=re.search(r'(?:virtio|e1000|e1000e|vmxnet3)=([0-9A-Fa-f:]+)',cfg['net0'])[1]
    return {'changed':changed,'created':created,'id':vmid,'name':name,'ip':str(ip.ip),'mac':mac,'tags':cfg.get('tags','').split(';') if cfg.get('tags') else []}

if __name__=='__main__':
    try:print(json.dumps(main(json.loads(sys.argv[1]))))
    except Exception as exc:
        print(type(exc).__name__+': VM convergence failed; inspect the declared identity, template and host task log.',file=sys.stderr);sys.exit(1)
