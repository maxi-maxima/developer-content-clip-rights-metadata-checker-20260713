#!/usr/bin/env python
import argparse, json, os, re
from pathlib import Path
REQUIRED=('source_url','license','creator','consent','ai_generated_disclosure')

def load_meta(path):
    p=Path(path)
    if p.suffix=='.json': return json.loads(p.read_text(encoding='utf-8'))
    data={}
    for line in p.read_text(encoding='utf-8').splitlines():
        if ':' in line:
            k,v=line.split(':',1); data[k.strip()]=v.strip()
    return data

def check(path):
    meta=load_meta(path); missing=[k for k in REQUIRED if not str(meta.get(k,'')).strip()]
    warnings=[]
    if meta.get('source_url') and not re.match(r'https?://', str(meta['source_url'])): warnings.append('source_url is not http(s)')
    if str(meta.get('consent','')).lower() not in ('yes','true','granted','public-domain'): warnings.append('consent is not clearly granted')
    return {'file':str(path),'status':'FAIL' if missing or warnings else 'PASS','missing':missing,'warnings':warnings}

def main(argv=None):
    p=argparse.ArgumentParser(description='Check clip metadata before publishing developer content snippets.')
    p.add_argument('metadata', nargs='+'); p.add_argument('--json',action='store_true')
    a=p.parse_args(argv); results=[check(x) for x in a.metadata]
    if a.json: print(json.dumps(results,indent=2)); return 1 if any(r['status']=='FAIL' for r in results) else 0
    print('# Developer content clip rights metadata report\n')
    print('| status | file | missing | warnings |\n|---|---|---|---|')
    for r in results: print(f"| {r['status']} | {r['file']} | {', '.join(r['missing']) or '-'} | {', '.join(r['warnings']) or '-'} |")
    return 1 if any(r['status']=='FAIL' for r in results) else 0
if __name__=='__main__': raise SystemExit(main())
