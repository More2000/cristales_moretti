#!/usr/bin/env python3
"""Chequea por script las assertions objetivas de cada eval.
Devuelve JSON con {assertion_index: {passed, evidence}} para las que sabe evaluar.
Las que no sabe evaluar quedan fuera y las gradúa un agente."""
import json, os, re, sys, subprocess

def lum(c):
    def f(v):
        v/=255
        return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=[f(x) for x in c]
    return .2126*r+.7152*g+.0722*b

def ratio(c1,c2):
    l1,l2=lum(c1),lum(c2)
    return (max(l1,l2)+.05)/(min(l1,l2)+.05)

def html_checks(path):
    """Chequeos sobre HTML usando Chromium (contraste real computado)."""
    js = r'''
const {chromium}=require("/opt/node22/lib/node_modules/playwright");
(async()=>{
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1280,height:900}});
 await p.goto("file://"+process.argv[2]);
 await p.waitForTimeout(900);
 const r=await p.evaluate(()=>{
   const lum=c=>{const[r,g,b]=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
   // color() moderno usa 0-1; rgb() usa 0-255. Normalizar o el cálculo da cualquier cosa.
   const parse=s=>{const n=s.match(/[\d.]+/g).slice(0,3).map(Number);
     return /^color\(/.test(s.trim()) ? n.map(v=>v*255) : n;};
   const bgOf=el=>{let n=el;while(n&&n!==document.documentElement){const bg=getComputedStyle(n).backgroundColor;const m=bg.match(/[\d.]+/g);if(m&&(m.length<4||parseFloat(m[3])>0.85))return parse(bg);n=n.parentElement}return[255,255,255]};
   const fails=[];
   document.querySelectorAll("p,h1,h2,h3,h4,a,span,li,button,dt,dd,summary,td,th,label").forEach(el=>{
     const t=[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(" ");
     if(!t)return;const cs=getComputedStyle(el);
     if(cs.display==="none"||cs.visibility==="hidden"||parseFloat(cs.opacity)===0)return;
     const fs=parseFloat(cs.fontSize),grande=fs>=24||(fs>=18.66&&parseInt(cs.fontWeight)>=700);
     const L1=lum(parse(cs.color)),L2=lum(bgOf(el));
     const rr=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
     if(rr<(grande?3:4.5))fails.push(t.slice(0,30)+" ("+cs.color+", "+fs+"px) = "+rr.toFixed(2));
   });
   const hs=[...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].map(h=>+h.tagName[1]);
   let salto=null;
   for(let i=1;i<hs.length;i++) if(hs[i]-hs[i-1]>1){salto=`h${hs[i-1]} -> h${hs[i]}`;break}
   const cta=[...document.querySelectorAll("button,a")].filter(e=>/contrat|elegir|empezar|comprar|suscrib|plan/i.test(e.textContent));
   const alturas=cta.map(e=>Math.round(e.getBoundingClientRect().height)).filter(h=>h>0);
   const divClick=document.querySelectorAll("div[onclick],span[onclick]").length;
   return {contrasteFails:fails, h1:document.querySelectorAll("h1").length, saltoHeading:salto,
           ctaAlturas:alturas, divClickeable:divClick};
 });
 // 320px
 const p2=await b.newPage({viewport:{width:320,height:700}});
 await p2.goto("file://"+process.argv[2]); await p2.waitForTimeout(700);
 r.desborda320=await p2.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1);
 console.log(JSON.stringify(r));
 await b.close();
})();'''
    tmp="/tmp/_chk.js"; open(tmp,"w").write(js)
    out=subprocess.run(["node",tmp,path],capture_output=True,text=True,timeout=120)
    if out.returncode!=0: return {"error":out.stderr[-400:]}
    return json.loads(out.stdout.strip().splitlines()[-1])

def src_checks(text):
    """Chequeos sobre código fuente por regex."""
    c={}
    c["useEffect_count"]=len(re.findall(r"useEffect\s*\(", text))
    # useEffect que llama a setState
    efectos=re.findall(r"useEffect\s*\(\s*\(\s*\)\s*=>\s*\{(.*?)\}\s*,\s*\[", text, re.S)
    c["useEffect_con_setState"]=sum(1 for e in efectos if re.search(r"\bset[A-Z]\w*\s*\(", e))
    c["usa_key_prop"]=bool(re.search(r"<\w+[^>]*\skey=\{", text))
    c["key_index"]=bool(re.search(r"key=\{\s*(i|idx|index)\s*\}", text))
    c["useState_count"]=len(re.findall(r"useState\s*[<(]", text))
    c["promise_all"]=bool(re.search(r"Promise\.all", text))
    c["await_secuencial"]=len(re.findall(r"^\s*const\s+\w+\s*=\s*await\s", text, re.M))
    c["use_client"]=bool(re.search(r"['\"]use client['\"]", text))
    c["use_server"]=bool(re.search(r"['\"]use server['\"]", text))
    c["auth_en_action"]=bool(re.search(r"(auth|session|getSession|currentUser|getUser\(\)|unauthorized|no autorizado)", text, re.I))
    c["validacion"]=bool(re.search(r"(zod|\.parse\(|safeParse|typeof\s+\w+\s*!==\s*['\"]string|trim\(\)\.length|schema)", text))
    c["revalidate"]=bool(re.search(r"revalidate(Path|Tag)", text))
    c["startViewTransition"]=bool(re.search(r"startViewTransition", text))
    c["feature_detect_vt"]=bool(re.search(r"(!?\s*document\.startViewTransition|'startViewTransition'\s+in\s+document|typeof\s+document\.startViewTransition)", text))
    c["flushSync"]=bool(re.search(r"flushSync", text))
    c["vt_name_dinamico"]=bool(re.search(r"view[-T]ransition[-N]ame[^\n]*[`$]\{|viewTransitionName:\s*[`'\"]?\$?\{|viewTransitionName:\s*`", text))
    c["reduced_motion"]=bool(re.search(r"prefers-reduced-motion", text))
    return c

def props_count(text):
    m=re.search(r"function\s+Card\s*\(\s*\{(.*?)\}\s*\)", text, re.S)
    if not m: 
        m=re.search(r"(?:const|export function)\s+Card\w*\s*=?\s*\(?\s*\{(.*?)\}", text, re.S)
    if not m: return None
    inner=m.group(1)
    return len([p for p in re.split(r",\s*", inner) if p.strip() and not p.strip().startswith("//")])

if __name__=="__main__":
    modo,path=sys.argv[1],sys.argv[2]
    if modo=="html": print(json.dumps(html_checks(path),ensure_ascii=False,indent=1))
    elif modo=="src": print(json.dumps(src_checks(open(path,encoding="utf-8").read()),ensure_ascii=False,indent=1))
    elif modo=="props": print(json.dumps({"props":props_count(open(path,encoding="utf-8").read())}))

def strip_comments(text):
    """Saca comentarios de línea y de bloque: el código comentado no cuenta como implementado."""
    text=re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text=re.sub(r"^\s*//.*$", "", text, flags=re.M)
    text=re.sub(r"(?<![:'\"])//[^\n]*$", "", text, flags=re.M)
    text=re.sub(r"\{\s*/\*.*?\*/\s*\}", "", text, flags=re.S)
    return text
