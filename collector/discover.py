'''Discovers new repos on GitHub and writes collector/discovered.json'''
import json,os,datetime as dt,urllib.request as U,urllib.parse as P
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
Q=[('topic:mcp-server','tool'),('topic:claude-skills','skill'),('topic:agent-skills','skill'),('topic:ai-agent','agent')]
DOM=[('Security',['security','vuln','pentest']),('Data',['sql','data','scrape','crawl','database']),('Docs',['pdf','docx','word','excel','document']),('Automation',['browser','automation','playwright','selenium']),('Code',['code','git','github','dev','ide']),('Communication',['slack','discord','email','chat']),('Design',['figma','design','ui']),('Search',['search'])]
def dom(t):
    t=t.lower()
    for d,ks in DOM:
        if any(k in t for k in ks):return d
    return 'General'
def main():
    since=(dt.date.today()-dt.timedelta(days=180)).isoformat();out={}
    h={'User-Agent':'toolmarket','Accept':'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):h['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    for q,ty in Q:
        url='https://api.github.com/search/repositories?'+P.urlencode({'q':'%s stars:>200 archived:false pushed:>%s'%(q,since),'sort':'stars','per_page':50})
        try:j=json.load(U.urlopen(U.Request(url,headers=h),timeout=20))
        except Exception as e:print('skip',q,e);continue
        for r in j.get('items',[]):
            if not r.get('license') or r['fork']:continue
            t=r['name']+' '+(r.get('description') or '')+' '+' '.join(r.get('topics',[]))
            out[r['full_name']]={'repo':r['full_name'],'type':ty,'dom':dom(t),'desc':(r.get('description') or r['name'])[:110],'cmd':'git clone '+r['clone_url']}
    if out:json.dump(list(out.values()),open(os.path.join(R,'collector','discovered.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    print('discovered:',len(out))
main()
