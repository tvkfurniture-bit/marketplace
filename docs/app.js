
const $=s=>document.querySelector(s),post=b=>fetch(MP.api,{method:'POST',headers:{'Content-Type':'text/plain'},body:JSON.stringify(b)}).then(r=>r.json());
async function lead(f,src){f.preventDefault();const m=f.target.querySelector('.msg');m.textContent='Sending…';const r=await post({action:'lead',email:f.target.email.value,source:src});m.textContent=r.ok?'Check your inbox ✔':(r.error||'Error')}
async function buy(slug){const em=$('#em').value,m=$('#bm'),btn=$('#bb');m.textContent='';if(!/^\S+@\S+\.\S+$/.test(em)){m.textContent='Enter a valid email (access is linked to it).';return}
btn.disabled=true;btn.textContent='Please wait…';const o=await post({action:'createOrder',slug,email:em});if(o.error){m.textContent=o.error;btn.disabled=false;btn.textContent='Unlock full blueprint';return}
const load=()=>new Promise(r=>{if(window.Razorpay)return r();const s=document.createElement('script');s.src='https://checkout.razorpay.com/v1/checkout.js';s.onload=r;document.head.appendChild(s)});await load();
new Razorpay({key:o.key,order_id:o.order_id,amount:o.amount,currency:o.currency,name:o.name,description:o.desc,prefill:{email:em},handler:async p=>{m.textContent='Verifying payment…';const v=await post({action:'verify',order_id:p.razorpay_order_id,payment_id:p.razorpay_payment_id,signature:p.razorpay_signature});
if(v.ok){m.innerHTML='Paid ✔ Check your email, or <a href="'+v.access+'" target="_blank" rel="noopener">open your product</a>.'}else{m.textContent=v.error||'Verification failed. Contact support with your payment ID '+p.razorpay_payment_id}btn.textContent='Done'},modal:{ondismiss:()=>{btn.disabled=false;btn.textContent='Unlock full blueprint'}}}).open()}

let D=[],shown=0;const N=48,g=$('#grid');const uniq=k=>[...new Set(D.map(x=>x[k]))].sort();
function fill(id,k,all){$(id).innerHTML='<option value="">'+all+'</option>'+uniq(k).map(v=>'<option>'+v.replace(/&/g,'&amp;')+'</option>').join('')}
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function view(more){const q=$('#q').value.toLowerCase(),t=$('#ty').value,l=$('#lo').value,c=$('#ca').value;const f=D.filter(x=>(!t||x.ty==t)&&(!l||x.l==l)&&(!c||x.c==c)&&(!q||(x.t+' '+x.m+' '+x.c+' '+x.l).toLowerCase().includes(q)));
if(!more){shown=0;g.innerHTML=''}f.slice(shown,shown+N).forEach(x=>g.insertAdjacentHTML('beforeend','<a class="card" href="o/'+x.s+'/"><div><span class="tag">'+esc(x.ty)+'</span><span class="tag">'+esc(x.l)+'</span></div><b>'+esc(x.t)+'</b><span style="color:#475569;font-size:14px">'+esc(x.m.slice(0,130))+'…</span><b style="margin-top:auto;color:var(--c)">'+MP.currency+' '+x.p+' · Preview free</b></a>'));
shown+=N;$('#more').style.display=shown<f.length?'inline-block':'none';$('#cnt').textContent=f.length+' results'}
if($('#grid'))fetch('catalog.json').then(r=>r.json()).then(d=>{D=d;fill('#ty','ty','All types');fill('#lo','l','All locations');fill('#ca','c','All categories');$('#kt').textContent=d.length;$('#kl').textContent=uniq('l').length;$('#kc').textContent=uniq('c').length;view()});
if($('#grid'))['q','ty','lo','ca'].forEach(i=>$('#'+i).addEventListener('input',()=>view()));$('#more').onclick=()=>view(true);
