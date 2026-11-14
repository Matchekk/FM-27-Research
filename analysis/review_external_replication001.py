"""Independent public metadata/arithmetic and optional immutable-blob checks.

External Python is read as bytes, never imported or executed. No upstream files
are stored, and no engine, save, registry or seed interface is available here.
"""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha1
import json
from math import isclose, sqrt
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT/'data/night-001-external-replication/sources.json'


def need(value, reason):
    if not value:
        raise ValueError(reason)


def pinned_entries(value):
    if isinstance(value,dict):
        if 'git_blob_sha1' in value:
            yield value['url'],value['git_blob_sha1']
        for child in value.values(): yield from pinned_entries(child)
    elif isinstance(value,list):
        for child in value: yield from pinned_entries(child)


def get(url):
    with urlopen(Request(url,headers={'User-Agent':'FM27-independent-source-review'}),timeout=25) as response:
        payload=response.read(2*1024**2+1)
    need(len(payload)<=2*1024**2,'External text resource exceeds review bound')
    return payload


def verify_blob(item):
    url,expected=item
    matched=re.fullmatch(r'https://github.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/(.+)',url)
    need(matched is not None,'Expected immutable original GitHub source URL')
    repo,commit,name=matched.groups()
    payload=get(f'https://raw.githubusercontent.com/{repo}/{commit}/{name}')
    actual=sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
    need(actual==expected,'Original Git blob mismatch: '+name)
    return dict(repository=repo,commit=commit,path=name,git_blob_sha1=actual,bytes=len(payload))


def audit(online=False):
    value=json.loads(REGISTER.read_text(encoding='utf8'))
    sources=value['sources']; observations=value['summary_arithmetic']['observations']
    need(len(sources)==len({s['id'] for s in sources})==9,'Source inventory differs')
    need(all(s['raw_job_rows_audited']==0 and s['independently_reproduced'] is False and
             s['author_engine_sha256'] is s['author_host_sha256'] is None for s in sources),
         'Unverified raw/build identity became an observed claim')
    need(len(observations)==len({(r['arm'],r['attribute']) for r in observations})==9,'SD approximation inventory differs')
    for row in observations:
        n,mean,t=row['n_assumed'],abs(row['reported_mean']),abs(row['reported_t'])
        need(n==300 and mean>.005 and t>.05,'Unsupported rounding/denominator assumption')
        expected=[mean/t,mean/t*sqrt(n),(mean-.005)/(t+.05)*sqrt(n),(mean+.005)/(t-.05)*sqrt(n)]
        actual=[row['approximate_SE'],row['approximate_contrast_SD'],*row['rounding_SD_range']]
        need(all(isclose(a,b,rel_tol=1e-13,abs_tol=1e-14) for a,b in zip(actual,expected,strict=True)),
             'SD/SE/rounding arithmetic differs')
    entries=dict(pinned_entries(value))
    result=dict(source_entries=9,sd_approximations_verified=9,pinned_blob_entries=len(entries),
                raw_data_reproduced=False,external_code_executed=False,native_starts=0)
    if online:
        with ThreadPoolExecutor(max_workers=4) as pool:
            checked=list(pool.map(verify_blob,entries.items()))
        inventory=value['repository_inventory']
        # The configured GitHub client handles the platform trust store; TLS is
        # not disabled when the local Python API certificate chain is unavailable.
        endpoint=f"repos/{inventory['repository']}/git/trees/{inventory['commit']}?recursive=1"
        tree=json.loads(subprocess.check_output(['gh','api',endpoint],cwd=ROOT,timeout=25))
        need(tree['truncated'] is False and len(tree['tree'])==inventory['tracked_entries']==176,'Pinned Git tree inventory differs')
        need(not any(r['path'].endswith('.jsonl') for r in tree['tree']),'Tracked raw JSONL exists')
        result.update(original_blobs_verified=len(checked),git_tree_entries_verified=176,
                      original_blob_manifest=checked)
    return result


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--online',action='store_true')
    print(json.dumps(audit(parser.parse_args().online),indent=2))
