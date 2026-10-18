#!/usr/bin/env python3
"""Static site generator. Source: live Apps Script export (API_URL + EXPORT_KEY env) or --csv opportunities.csv. Output: ./docs (GitHub Pages / Cloudflare Pages)."""
import os,sys,json,csv,html,urllib.request,urllib.parse,shutil,datetime
OUT='docs'; e=html.escape
def load():
    if '--csv' in sys.argv:
        rows=list(csv.DictReader(open('opportunities.csv',encoding='utf-8')))
        for r in rows: r['price']=r['price'] or ('999' if r['type']=='Software Tool' else '499')
        s={'brand_name':'Venture Atlas','brand_color':'#0f766e','site_url':os.environ.get('SITE_URL','https://example.github.io/repo'),'support_email':'','disclaimer':'Income figures are unverified illustrative estimates from the source research, not guarantees.','currency':'INR'}
        return s,rows,os.environ.get('API_URL','')
    api=os.environ['API_URL']; u=api+('&' if '?' in api else '?')+urllib.parse.urlencode({'action':'export','key':os.environ['EXPORT_KEY']})
    d=json.load(urllib.request.urlopen(u,timeout=60)); return d['settings'],d['items'],api
S,ITEMS,API=load(); SITE=S['site_url'].rstrip('/'); B=e(S['brand_name'])
CSS="""*{box-sizing:border-box}body{margin:0;font:16px/1.6 system-ui,Segoe UI,Arial;color:#0f172a;background:#f8fafc}a{color:var(--c)}
:root{--c:%s}.w{max-width:1100px;margin:auto;padding:0 18px}header{background:#fff;border-bottom:1px solid #e2e8f0;position:sticky;top:0;z-index:9}
header .w{display:flex;justify-content:space-between;align-items:center;height:60px}.logo{font-weight:800;color:var(--c);text-decoration:none;font-size:20px}
.hero{background:linear-gradient(135deg,var(--c),#0f172a);color:#fff;padding:56px 0}.hero h1{font-size:clamp(28px,5vw,46px);margin:0 0 10px}.hero p{max-width:640px;opacity:.9}
.bar{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:10px;margin:-26px 0 18px}input,select{width:100%%;padding:12px;border:1px solid #cbd5e1;border-radius:10px;font:inherit;background:#fff}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}.card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit;transition:.2s}
.card:hover{transform:translateY(-3px);box-shadow:0 10px 24px #0001}.tag{display:inline-block;font-size:12px;padding:2px 9px;border-radius:99px;background:#ecfeff;color:var(--c);margin-right:4px}
.btn{background:var(--c);color:#fff;border:0;padding:13px 22px;border-radius:10px;font:600 16px inherit;cursor:pointer;text-decoration:none;display:inline-block}.btn:disabled{opacity:.5}
.lock{position:relative;background:#fff;border:1px dashed #94a3b8;border-radius:12px;padding:16px;margin:16px 0}.lock li{filter:blur(4px);user-select:none}.buy{background:#fff;border:2px solid var(--c);border-radius:14px;padding:20px;position:sticky;top:80px}
.two{display:grid;grid-template-columns:2fr 1fr;gap:24px;margin:28px 0}.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:22px 0}.kpi div{background:#fff;border-radius:12px;padding:14px;text-align:center;border:1px solid #e2e8f0}.kpi b{display:block;font-size:22px;color:var(--c)}
footer{padding:30px 0;color:#64748b;font-size:13px}.msg{margin-top:10px;font-size:14px}@media(max-width:760px){.bar,.two{grid-template-columns:1fr}.buy{position:static}.kpi{grid-template-columns:1fr 1fr}}"""%S['brand_color']
CFG='window.MP='+json.dumps({'api':API,'currency':S.get('currency','INR'),'brand':S['brand_name']})+';'
JS=r"""
const $=s=>document.querySelector(s),post=b=>fetch(MP.api,{method:'POST',headers:{'Content-Type':'text/plain'},body:JSON.stringify(b)}).then(r=>r.json());
async function lead(f,src){f.preventDefault();const m=f.target.querySelector('.msg');m.textContent='Sending…';const r=await post({action:'lead',email:f.target.email.value,source:src});m.textContent=r.ok?'Check your inbox ✔':(r.error||'Error')}
async function buy(slug){const em=$('#em').value,m=$('#bm'),btn=$('#bb');m.textContent='';if(!/^\S+@\S+\.\S+$/.test(em)){m.textContent='Enter a valid email (access is linked to it).';return}
btn.disabled=true;btn.textContent='Please wait…';const o=await post({action:'createOrder',slug,email:em});if(o.error){m.textContent=o.error;btn.disabled=false;btn.textContent='Unlock full blueprint';return}
const load=()=>new Promise(r=>{if(window.Razorpay)return r();const s=document.createElement('script');s.src='https://checkout.razorpay.com/v1/checkout.js';s.onload=r;document.head.appendChild(s)});await load();
new Razorpay({key:o.key,order_id:o.order_id,amount:o.amount,currency:o.currency,name:o.name,description:o.desc,prefill:{email:em},handler:async p=>{m.textContent='Verifying payment…';const v=await post({action:'verify',order_id:p.razorpay_order_id,payment_id:p.razorpay_payment_id,signature:p.razorpay_signature});
if(v.ok){m.innerHTML='Paid ✔ Check your email, or <a href="'+v.access+'" target="_blank" rel="noopener">open your product</a>.'}else{m.textContent=v.error||'Verification failed. Contact support with your payment ID '+p.razorpay_payment_id}btn.textContent='Done'},modal:{ondismiss:()=>{btn.disabled=false;btn.textContent='Unlock full blueprint'}}}).open()}
"""
def page(title,desc,path,body,extra=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc[:160])}"><link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:160])}"><meta property="og:type" content="website"><link rel="stylesheet" href="{'../'*(path.count('/')-1)}style.css">{extra}</head><body>
<header><div class="w"><a class="logo" href="{'../'*(path.count('/')-1) or './'}">{B}</a><a href="{'../'*(path.count('/')-1)}#catalog">Browse</a></div></header>{body}
<footer><div class="w">© {datetime.date.today().year} {B}. {e(S['disclaimer'])} {('Support: '+e(S['support_email'])) if S.get('support_email') else ''}</div></footer>
<script src="{'../'*(path.count('/')-1)}config.js"></script><script src="{'../'*(path.count('/')-1)}app.js"></script></body></html>'''
def leadform(src): return f'<form onsubmit="lead(event,\'{e(src)}\')" style="display:flex;gap:8px;flex-wrap:wrap"><input name="email" type="email" placeholder="you@email.com" required style="flex:1;min-width:180px"><button class="btn">Get free previews</button><div class="msg" style="width:100%"></div></form>'
def item_page(r):
    pv=r['description'][:330].rsplit(' ',1)[0]+'…'; tool=r['type']=='Software Tool'
    labels=['Automation & integrations','Data model','UI/UX','Source estimate'] if tool else ['Scale path','Moat','Beginner step','Source yield estimate (unverified)']
    ld={"@context":"https://schema.org","@type":"Product","name":r['title'],"description":r['summary'],"category":r['category'],"offers":{"@type":"Offer","price":r['price'],"priceCurrency":S.get('currency','INR'),"availability":"https://schema.org/InStock"}}
    body=f'''<div class="w"><div class="two"><main><p><span class="tag">{e(r['type'])}</span><span class="tag">{e(r['location'])}</span><span class="tag">{e(r['category'])}</span></p><h1>{e(r['title'])}</h1><p><b>{e(r['summary'])}.</b></p><h2>Free preview</h2><p>{e(pv)}</p>
<div class="lock"><b>🔒 Included in the full blueprint</b><ul>{''.join(f'<li>{l}: ████████ ████ ██████ ███</li>' for l in labels)}</ul></div>
<h3>Get more like this</h3>{leadform(r['title'])}</main><aside><div class="buy"><div style="font-size:30px;font-weight:800">{e(S.get('currency','INR'))} {e(str(r['price']))}</div><p>One-time purchase. Delivered as a Google Doc shared to your email.</p>
<input id="em" type="email" placeholder="Your Google account email"><br><br><button id="bb" class="btn" style="width:100%" onclick="buy('{e(r['slug'])}')">Unlock full blueprint</button><div id="bm" class="msg"></div></div></aside></div></div>'''
    return page(r['seo_title'] or r['title'],r['seo_desc'] or r['summary'],f"/o/{r['slug']}/",body,f'<script type="application/ld+json">{json.dumps(ld)}</script>')
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'/o')
open(OUT+'/style.css','w').write(CSS); open(OUT+'/config.js','w').write(CFG); open(OUT+'/.nojekyll','w').write('')
for r in ITEMS:
    os.makedirs(f"{OUT}/o/{r['slug']}"); open(f"{OUT}/o/{r['slug']}/index.html",'w',encoding='utf-8').write(item_page(r))
cat=[{'s':r['slug'],'t':r['title'],'ty':r['type'],'l':r['location'],'c':r['category'],'m':r['summary'],'p':r['price']} for r in ITEMS]
json.dump(cat,open(OUT+'/catalog.json','w'),separators=(',',':'))
HOME_JS=r"""
let D=[],shown=0;const N=48,g=$('#grid');const uniq=k=>[...new Set(D.map(x=>x[k]))].sort();
function fill(id,k,all){$(id).innerHTML='<option value="">'+all+'</option>'+uniq(k).map(v=>'<option>'+v.replace(/&/g,'&amp;')+'</option>').join('')}
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function view(more){const q=$('#q').value.toLowerCase(),t=$('#ty').value,l=$('#lo').value,c=$('#ca').value;const f=D.filter(x=>(!t||x.ty==t)&&(!l||x.l==l)&&(!c||x.c==c)&&(!q||(x.t+' '+x.m+' '+x.c+' '+x.l).toLowerCase().includes(q)));
if(!more){shown=0;g.innerHTML=''}f.slice(shown,shown+N).forEach(x=>g.insertAdjacentHTML('beforeend','<a class="card" href="o/'+x.s+'/"><div><span class="tag">'+esc(x.ty)+'</span><span class="tag">'+esc(x.l)+'</span></div><b>'+esc(x.t)+'</b><span style="color:#475569;font-size:14px">'+esc(x.m.slice(0,130))+'…</span><b style="margin-top:auto;color:var(--c)">'+MP.currency+' '+x.p+' · Preview free</b></a>'));
shown+=N;$('#more').style.display=shown<f.length?'inline-block':'none';$('#cnt').textContent=f.length+' results'}
fetch('catalog.json').then(r=>r.json()).then(d=>{D=d;fill('#ty','ty','All types');fill('#lo','l','All locations');fill('#ca','c','All categories');$('#kt').textContent=d.length;$('#kl').textContent=uniq('l').length;$('#kc').textContent=uniq('c').length;view()});
['q','ty','lo','ca'].forEach(i=>$('#'+i).addEventListener('input',()=>view()));$('#more').onclick=()=>view(true);
"""
open(OUT+'/app.js','w').write(JS+HOME_JS.replace("fetch('catalog.json')","if($('#grid'))fetch('catalog.json')").replace("['q','ty','lo','ca'].forEach","if($('#grid'))['q','ty','lo','ca'].forEach"))
home=f'''<section class="hero"><div class="w"><h1>Validated business blueprints &amp; ready-to-deploy tools</h1><p>Search {len(ITEMS)}+ opportunities by city and industry. Preview free, unlock the full blueprint when you are ready.</p><br>{leadform('homepage')}</div></section>
<div class="w"><div class="bar" id="catalog"><input id="q" placeholder="Search e.g. clinic, logistics, Garia…"><select id="ty"></select><select id="lo"></select><select id="ca"></select></div>
<div class="kpi"><div><b id="kt">–</b>Products</div><div><b id="kl">–</b>Locations</div><div><b id="kc">–</b>Categories</div><div><b id="cnt">–</b>Showing</div></div>
<div class="g" id="grid"></div><p style="text-align:center"><button class="btn" id="more">Load more</button></p></div>'''
open(OUT+'/index.html','w',encoding='utf-8').write(page(S['brand_name']+' – Business Opportunity Marketplace','Search validated local business blueprints and automation tools. Free previews, instant delivery.','/',home))
urls=[SITE+'/']+[f"{SITE}/o/{r['slug']}/" for r in ITEMS]
open(OUT+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>')
open(OUT+'/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print('built',len(ITEMS),'pages')
