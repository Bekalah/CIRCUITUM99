(()=>{
 "use strict";

let artifacts=[],grimoires={},provenance={},fusionists={},quests=[];

 let artifacts=[],grimoires={},provenance={},fusionists={},quests=[];

 const qs=s=>document.querySelector(s);
 function safeFetchJSON(path){
  return fetch(path,{cache:"no-store"}).then(r=>{if(!r.ok) throw new Error("Missing: "+path);return r.json();});
 }
 function el(tag,attrs={},children=[]){
  const n=document.createElement(tag);
  Object.entries(attrs).forEach(([k,v])=>{if(k==="class") n.className=v; else if(k.startsWith("on")&&typeof v==="function") n.addEventListener(k.slice(2),v); else n.setAttribute(k,v);});
  children.forEach(c=>n.appendChild(typeof c==="string"?document.createTextNode(c):c));
  return n;
 }
 async function loadData(){
  const [g,f,a,p,q]=await Promise.all([
   safeFetchJSON("/assets/data/fusion/grimoires.json"),
   safeFetchJSON("/assets/data/fusion/fusionist_registry.json"),
   safeFetchJSON("/assets/data/fusion/artifacts.json"),
   safeFetchJSON("/assets/data/fusion/provenance.json"),
   safeFetchJSON("/assets/data/fusion/quests.json")
  ]);
  grimoires=Object.fromEntries(g.items.map(x=>[x.id,x]));
  fusionists=Object.fromEntries(f.fusionists.map(x=>[x.id,x]));
  provenance=Object.fromEntries(p.records.map(x=>[x.id,x]));
  quests=q.quests||[];
  artifacts=a.artifacts.map(x=>Object.assign({},x));

 await Promise.all(Object.values(grimoires).map(async gr=>{
  try{const r=await fetch(gr.path,{method:"HEAD"});gr.missing=!r.ok;}
  catch(e){gr.missing=true;}
 }));
  if(localStorage.getItem("sophia7_spawn_all")==="true"){artifacts.forEach(x=>x.unlocked=true);}
  renderStairs();
  renderShelves();
 window._grimoires=grimoires;
 window._provenance=provenance;
 window._artifacts=artifacts;
 window._quests=quests;
}
function renderStairs(){
 const stairs=qs("#stairs");if(!stairs) return;stairs.innerHTML="";
 for(let i=1;i<=33;i++){
  const b=el("button",{class:"stair","aria-label":"Stair "+i,onclick:()=>scrollToShelf(i)},[String(i)]);
  stairs.appendChild(b);
 }
}
 function shelfIndexFromLocation(loc){const m=/shelf_(\d+)/.exec(loc||"");if(!m){const m2=/shelf(\d+)/.exec(loc||"");return m2?parseInt(m2[1],10):null;}return parseInt(m[1],10);}
 function groupedByShelf(){const map=new Map();artifacts.forEach(a=>{const idx=shelfIndexFromLocation(a.location)||0;if(!map.has(idx)) map.set(idx,[]);map.get(idx).push(a);});return [...map.entries()].sort((a,b)=>a[0]-b[0]);}
function renderShelves(){
 const root=qs("#shelves");if(!root) return;root.innerHTML="";
 groupedByShelf().forEach(([shelf,items])=>{
  const shelfEl=el("section",{"aria-label":"Shelf "+shelf,class:"shelf"},[el("h2",{},["Shelf ",String(shelf)])]);
  items.forEach(item=>{
   const unlocked=item.unlocked===true;
   const btn=el("button",{class:"drawer","aria-label":item.title,onclick:()=>onOpenArtifact(item)},[(unlocked?"📖 ":"🔒 ")+item.title]);
   shelfEl.appendChild(btn);
  });
  root.appendChild(shelfEl);
 });
}
function onOpenArtifact(artifact){
 if(!artifact.unlocked && localStorage.getItem("sophia7_spawn_all")!=="true"){
  artifact.unlocked=true;
  if(window.recordLoot) window.recordLoot(artifact.id);
 }
 renderWorkbench(artifact);
 renderShelves();
}
function scrollToShelf(num){
 const target=[...document.querySelectorAll(".shelf")].find(s=>s.querySelector("h2")?.textContent?.includes(" "+num));
 if(target){
  const behavior=window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth";
  target.scrollIntoView({behavior,block:"start"});
 }
}

  await Promise.all(Object.values(grimoires).map(async gr=>{try{const r=await fetch(gr.path,{method:"HEAD"});gr.missing=!r.ok;}catch(e){gr.missing=true;}}));
  if(localStorage.getItem("sophia7_spawn_all")==="true"){artifacts.forEach(x=>x.unlocked=true);}
  renderStairs();
  renderShelves();
  window._grimoires=grimoires;window._provenance=provenance;window._artifacts=artifacts;window._quests=quests;
 }
 function renderStairs(){
  const stairs=qs("#stairs");if(!stairs) return;stairs.innerHTML="";
  for(let i=1;i<=33;i++){const b=el("button",{class:"stair",onclick:()=>scrollToShelf(i)},[String(i)]);stairs.appendChild(b);}
 }
 function shelfIndexFromLocation(loc){const m=/shelf_(\d+)/.exec(loc||"");if(!m){const m2=/shelf(\d+)/.exec(loc||"");return m2?parseInt(m2[1],10):null;}return parseInt(m[1],10);}
 function groupedByShelf(){const map=new Map();artifacts.forEach(a=>{const idx=shelfIndexFromLocation(a.location)||0;if(!map.has(idx)) map.set(idx,[]);map.get(idx).push(a);});return [...map.entries()].sort((a,b)=>a[0]-b[0]);}
 function renderShelves(){const root=qs("#shelves");if(!root) return;root.innerHTML="";groupedByShelf().forEach(([shelf,items])=>{const shelfEl=el("section",{"aria-label":"Shelf "+shelf,class:"shelf"},[el("h2",{},["Shelf ",String(shelf)])]);items.forEach(item=>{const unlocked=item.unlocked===true;const btn=el("button",{class:"drawer",onclick:()=>onOpenArtifact(item)},[(unlocked?"📖 ":"🔒 ")+item.title]);shelfEl.appendChild(btn);});root.appendChild(shelfEl);});}
 function onOpenArtifact(artifact){if(!artifact.unlocked && localStorage.getItem("sophia7_spawn_all")!=="true"){artifact.unlocked=true;if(window.recordLoot) window.recordLoot(artifact.id);}renderWorkbench(artifact);renderShelves();}
 function scrollToShelf(num){const target=[...document.querySelectorAll(".shelf")].find(s=>s.querySelector("h2")?.textContent?.includes(" "+num));if(target) target.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});}

 window.renderShelves=renderShelves;window.onOpenArtifact=onOpenArtifact;document.addEventListener("DOMContentLoaded",loadData);
})();
