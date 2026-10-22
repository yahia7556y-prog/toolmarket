// Cloudflare Worker + KV: يعد ضغطات زر التثبيت بلا أي بيانات شخصية
export default{async fetch(req,env){
const u=new URL(req.url),cors={"access-control-allow-origin":"*","access-control-allow-headers":"content-type"};
if(req.method==="OPTIONS")return new Response(null,{headers:cors});
if(u.pathname==="/install"&&req.method==="POST"){
 const {name}=await req.json().catch(()=>({}));
 if(!/^[\w.\-]{1,80}$/.test(name||""))return new Response("bad",{status:400,headers:cors});
 const day=new Date().toISOString().slice(0,10),ip=req.headers.get("cf-connecting-ip")||"";
 const d=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(ip+name+day));
 const k="seen:"+[...new Uint8Array(d)].slice(0,8).map(b=>b.toString(16)).join("");
 if(!(await env.KV.get(k))){await env.KV.put(k,"1",{expirationTtl:90000});
  const c=+(await env.KV.get("n:"+name)||0);await env.KV.put("n:"+name,String(c+1));}
 return new Response("ok",{headers:cors});}
if(u.pathname==="/stats"){const l=await env.KV.list({prefix:"n:"}),o={};
 for(const k of l.keys)o[k.name.slice(2)]=+(await env.KV.get(k.name));
 return new Response(JSON.stringify(o),{headers:{...cors,"content-type":"application/json"}});}
return new Response("not found",{status:404});}}
