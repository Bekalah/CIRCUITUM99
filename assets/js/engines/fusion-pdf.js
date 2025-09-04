(()=>{
 "use strict";
 function renderWorkbench(artifact){
  const viewer=document.getElementById("doc-viewer");
  const prov=document.getElementById("provenance-card");
  if(!artifact){if(viewer) viewer.src="";if(prov) prov.textContent="";return;}
  const g=(window._grimoires||{})[artifact.primary_text_id];
  if(!g){if(viewer) viewer.src="";if(prov) prov.innerHTML="Missing grimoire entry.";return;}
  if(viewer) viewer.src=g.missing?"about:blank":g.path;
  const p=(window._provenance||{})[g.provenance_id]||{};
  const safe=s=>String(s||"");
  let extra="";
  if(g.id==="ars_notoria"){
   extra='<svg width="100%" height="200" viewBox="0 0 200 200" role="img" aria-label="Concentric prayer-notae labeled for rapid learning, invoking divine names around a central intent."><circle cx="100" cy="100" r="90" stroke="gold" fill="none"/><circle cx="100" cy="100" r="60" stroke="gold" fill="none"/><circle cx="100" cy="100" r="30" stroke="gold" fill="none"/><text x="100" y="100" fill="gold" text-anchor="middle" dominant-baseline="middle" font-size="10">NOTAE</text></svg>';
  }
  let questBtn="";
  if(window._quests){
   const q=window._quests.find(q=>q.steps&&q.steps[0].action==="read"&&q.steps[0].text_id===g.id);
   if(q) questBtn=`<button id="startQuest" data-q="${q.id}">Start Quest</button>`;
  }
  if(prov) prov.innerHTML=`<h3>${safe(g.title)}</h3><p><strong>Author:</strong> ${safe(g.author)}</p><p><strong>Summary:</strong> ${safe(g.summary)}</p><p><strong>License:</strong> ${g.missing?"Missing Source":safe(p.license)}</p>${questBtn}<p><a href="${safe(g.path)}" download>Download Source</a></p>${extra}`;
  if(questBtn){const btn=document.getElementById("startQuest");btn?.addEventListener("click",()=>startQuest(btn.dataset.q));}
  if(window.recordRead) window.recordRead(g.id);
  const marks=(window.checkMarks?window.checkMarks():[]);
  if(marks.length>0 && prov) prov.innerHTML+=`<p>Mark Earned: ${marks.join(", ")}</p>`;
 }
 window.renderWorkbench=renderWorkbench;
})();
