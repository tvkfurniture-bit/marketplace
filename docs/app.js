
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],post=b=>fetch(MP.api,{method:'POST',headers:{'Content-Type':'text/plain'},body:JSON.stringify(b)}).then(r=>r.json());
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
async function lead(ev,src){ev.preventDefault();const f=ev.target,m=f.querySelector('.msg');m.textContent='Sending…';try{const r=await post({action:'lead',email:f.email.value,source:src});m.textContent=r.ok?'Done! Check your inbox.':(r.error||'Something went wrong.')}catch(x){m.textContent='Network error. Please retry.'}}
async function buy(slug){const em=$('#em').value,m=$('#bm'),btn=$('#bb'),L='Unlock full blueprint';m.textContent='';if(!/^\S+@\S+\.\S+$/.test(em)){m.textContent='Enter the Google account email you want access on.';return}
btn.disabled=true;btn.textContent='Please wait…';let o;try{o=await post({action:'createOrder',slug,email:em})}catch(x){o={error:'Network error. Please retry.'}}
if(o.error){m.textContent=o.error;btn.disabled=false;btn.textContent=L;return}
await new Promise(r=>{if(window.Razorpay)return r();const s=document.createElement('script');s.src='https://checkout.razorpay.com/v1/checkout.js';s.onload=r;document.head.appendChild(s)});
new Razorpay({key:o.key,order_id:o.order_id,amount:o.amount,currency:o.currency,name:o.name,description:o.desc,prefill:{email:em},handler:async p=>{m.textContent='Verifying payment…';const v=await post({action:'verify',order_id:p.razorpay_order_id,payment_id:p.razorpay_payment_id,signature:p.razorpay_signature});
if(v.ok){m.innerHTML='✅ Paid. Check your email, or <a href="'+v.access+'" target="_blank" rel="noopener">open your product</a>.'}else{m.textContent=(v.error||'Verification failed.')+' Payment ID: '+p.razorpay_payment_id}btn.textContent='Done'},modal:{ondismiss:()=>{btn.disabled=false;btn.textContent=L}}}).open()}
$('#mb')&&($('#mb').onclick=()=>$('nav').classList.toggle('open'));
const io=new IntersectionObserver(a=>a.forEach(x=>x.isIntersecting&&x.target.classList.add('in')),{threshold:.1});const rv=()=>$$('.rv:not(.in)').forEach(x=>io.observe(x));rv();
if($('#grid')){let D=[],shown=0,ty='';const N=24,g=$('#grid'),uniq=k=>[...new Set(D.map(x=>x[k]))].sort();
const fill=(id,k,all)=>$(id).innerHTML='<option value="">'+all+'</option>'+uniq(k).map(v=>'<option>'+esc(v)+'</option>').join('');
function view(more){const q=$('#q').value.toLowerCase(),l=$('#lo').value,c=$('#ca').value,so=$('#so').value;let f=D.filter(x=>(!ty||x.ty==ty)&&(!l||x.l==l)&&(!c||x.c==c)&&(!q||(x.t+' '+x.m+' '+x.c+' '+x.l).toLowerCase().includes(q)));
if(so=='pa')f.sort((a,b)=>a.p-b.p);if(so=='pd')f.sort((a,b)=>b.p-a.p);if(so=='az')f.sort((a,b)=>a.t.localeCompare(b.t));
if(!more){shown=0;g.innerHTML=''}f.slice(shown,shown+N).forEach(x=>g.insertAdjacentHTML('beforeend','<a class="card rv" href="o/'+x.s+'/"><div class="ct"><span class="tag '+(x.ty=='Software Tool'?'t':'')+'">'+(x.ty=='Software Tool'?'⚙ Software tool':'💡 Business blueprint')+'</span><span class="loc">📍 '+esc(x.l)+'</span></div><h3>'+esc(x.t)+'</h3><p>'+esc(x.m.slice(0,140))+'…</p><div class="cf"><span>'+esc(x.c)+'</span><b>'+MP.cur+' '+x.p+'</b></div><span class="go">Preview free →</span></a>'));
shown+=N;$('#more').style.display=shown<f.length?'inline-block':'none';$('#cnt').textContent=f.length+' of '+D.length+' shown';rv()}
fetch('catalog.json').then(r=>r.json()).then(d=>{D=d;fill('#lo','l','All locations');fill('#ca','c','All categories');view()});
['q','lo','ca','so'].forEach(i=>$('#'+i).addEventListener('input',()=>view()));$('#more').onclick=()=>view(true);
$$('.tab').forEach(t=>t.onclick=()=>{ty=t.dataset.ty;$$('.tab').forEach(x=>x.classList.toggle('on',x==t));view()});
$$('[data-cat]').forEach(b=>b.onclick=()=>{$('#ca').value=b.dataset.cat;$('#catalog').scrollIntoView();view()});$$('[data-q]').forEach(b=>b.onclick=()=>{$('#q').value=b.dataset.q;$('#catalog').scrollIntoView();view()});
$('#hq')&&$('#hq').addEventListener('submit',ev=>{ev.preventDefault();$('#q').value=$('#hs').value;$('#catalog').scrollIntoView();view()})}
