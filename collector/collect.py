'''Collects stats and writes web/data.json. Usage: python collector/collect.py [--demo]'''
import json,os,sys,math,random,datetime as dt,urllib.request as U
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
DEMO='--demo' in sys.argv
def now():return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
def get(url,h=None):
    try:
        return json.load(U.urlopen(U.Request(url,headers=h or {'User-Agent':'toolmarket'}),timeout=20))
    except Exception as e:
        print('skip',url,e);return None
def gh(repo):
    if DEMO:
        r=random.Random(repo);return {'stargazers_count':r.randint(500,60000),'pushed_at':now().isoformat(),'license':{'spdx_id':'MIT'}}
    h={'User-Agent':'toolmarket','Accept':'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):h['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    return get('https://api.github.com/repos/'+repo,h)
def downloads(s):
    if DEMO:return random.Random(s['repo']+'d').randint(200,50000) if (s.get('npm') or s.get('pypi')) else None
    if s.get('npm'):
        j=get('https://api.npmjs.org/downloads/point/last-week/'+s['npm']);return round(j['downloads']/7) if j else None
    if s.get('pypi'):
        j=get('https://pypistats.org/api/packages/%s/recent'%s['pypi']);return j['data']['last_day'] if j else None
def score(stars,use,days,lic):
    q=min(1,math.log10(stars+1)/5)*2+(1 if days<30 else .5 if days<180 else 0)+(.5 if lic else 0)+min(1.5,math.log10(use+1)/6*1.5)
    return round(min(5,q),1)
def seeds():
    S=[]
    for ln in open(os.path.join(R,'collector','seeds.txt'),encoding='utf-8'):
        ln=ln.strip()
        if not ln or ln[0]=='#':continue
        f=(ln.split('|')+['']*9)[:9]
        S.append(dict(repo=f[0],type=f[1],dom=f[2],name=f[3],npm=f[4],pypi=f[5],cmd=f[6],desc=f[7],ar=f[8]))
    seen={s['repo'] for s in S}
    p=os.path.join(R,'collector','discovered.json')
    if os.path.exists(p):
        for d in json.load(open(p,encoding='utf-8')):
            if d['repo'] not in seen:S.append(d);seen.add(d['repo'])
    return S
def main():
    today=dt.date.today().isoformat();hp=os.path.join(R,'data','history.json')
    os.makedirs(os.path.join(R,'data'),exist_ok=True);os.makedirs(os.path.join(R,'web'),exist_ok=True)
    H=json.load(open(hp)) if os.path.exists(hp) else {}
    items=[];used=set()
    T=(get(os.environ['TELEMETRY_URL']+'/stats') if os.environ.get('TELEMETRY_URL') else None) or {}
    for s in seeds():
        g=gh(s['repo'])
        if not g:continue
        stars=g['stargazers_count'];use=downloads(s) or stars
        n=s.get('name') or s['repo'].split('/')[1]
        if n in used:n=s['repo'].replace('/','-')
        used.add(n);h=H.setdefault(n,{})
        if DEMO and len(h)<2:
            for k in range(1,7):h[(dt.date.today()-dt.timedelta(days=k)).isoformat()]=round(use*random.uniform(.8,1.1))
        h[today]=use
        sp=[h[d] for d in sorted(h)[-7:]]
        prev=[h[d] for d in sorted(h) if d<today]
        chg=round((use-prev[-1])/prev[-1]*100,1) if prev and prev[-1] else 0
        age=(now()-dt.datetime.strptime(g['pushed_at'][:19],'%Y-%m-%dT%H:%M:%S')).days
        sc=min(5,round(score(stars,use,age,bool(g.get('license')))+min(.5,math.log10(T.get(n,0)+1)/4),1))
        items.append({'name':n,'repo':s['repo'],'type':s['type'],'dom':s['dom'],'desc':s['desc'],'ar':s.get('ar',''),'score':sc,'inst':T.get(n,0),'use':use,'chg':chg,'cmd':s['cmd'],'sp':sp if len(sp)>1 else sp*2})
    json.dump({'updated':today,'demo':DEMO,'telemetry':os.environ.get('TELEMETRY_URL',''),'items':items},open(os.path.join(R,'web','data.json'),'w',encoding='utf-8'),ensure_ascii=False)
    json.dump(H,open(hp,'w'))
    print('items:',len(items))
main()
