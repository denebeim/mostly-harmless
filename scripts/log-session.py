import datetime,os,re,subprocess,sys
from zoneinfo import ZoneInfo
from pathlib import Path
log=os.environ.get('DEEPTHOT_SESSION_LOG',str(Path(__file__).resolve().parents[1]/'eddie-session.log'))
secret_names=re.compile(r'password|passwd|token|secret|private.?key|api.?key',re.I)
secrets=[v for k,v in os.environ.items() if secret_names.search(k) and len(v)>5]
pem=False
cmd=sys.argv[1:]
with open(log,'a') as out:
 def emit(line):
  global pem
  if '-----BEGIN ' in line and any(x in line for x in ('PRIVATE KEY','CERTIFICATE')):pem=True;line='[REDACTED PEM MATERIAL]\n'
  elif pem:
   if '-----END ' in line:pem=False
   return
  for value in secrets:line=line.replace(value,'[REDACTED]')
  line=re.sub(r'(?i)((?:password|passwd|api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret)\s*[=:]\s*)([^\s,}]+)',r'\1[REDACTED]',line)
  out.write(line);out.flush();sys.stdout.write(line);sys.stdout.flush()
 emit('\nBEGIN '+datetime.datetime.now(ZoneInfo('America/Phoenix')).isoformat()+'\n')
 emit('COMMAND: '+repr(cmd)+'\n')
 p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
 for line in p.stdout:emit(line)
 status=p.wait();emit('END exit='+str(status)+'\n')
sys.exit(status)
