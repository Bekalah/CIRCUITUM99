(()=>{
 "use strict";
 function renderWorkbench(artifact){
  const viewer=document.getElementById("doc-viewer");
  const prov=document.getElementById("provenance-card");
  if(!artifact){if(viewer) viewer.src="";if(prov) prov.textContent="";return;}
  const g=(window._grimoires||{})[artifact.primary_text_id];
  if(!g){if(viewer) viewer.src="";if(prov) prov.innerHTML="Missing grimoire entry.";return;}

  if(g.missing){if(viewer) viewer.src="";if(prov) prov.innerHTML="<p>Missing source file.</p>";return;}
  if(viewer) viewer.src=g.path;

  if(viewer) viewer.src=g.missing?"about:blank":g.path;

  const p=(window._provenance||{})[g.provenance_id]||{};
  const safe=s=>String(s||"");
  let extra="";
  if(g.id==="ars_notoria"){
   extra='<svg width="100%" height="200" viewBox="0 0 200 200" role="img" aria-label="Concentric prayer-notae labeled for rapid learning, invoking divine names around a central intent."><circle cx="100" cy="100" r="90" stroke="gold" fill="none"/><circle cx="100" cy="100" r="60" stroke="gold" fill="none"/><circle cx="100" cy="100" r="30" stroke="gold" fill="none"/><text x="100" y="100" fill="gold" text-anchor="middle" dominant-baseline="middle" font-size="10">NOTAE</text></svg>';
  }

  let questBtns="";
  const quests=(window.getQuestsForArtifact?window.getQuestsForArtifact(artifact.id):[]);
  quests.forEach(q=>{if(!(window.isQuestStarted&&window.isQuestStarted(q.id)))questBtns+=`<button class="startQuest" data-q="${q.id}">Start Quest: ${q.title}</button>`;});
  let corrBtn="";
  if(artifact.id==="correspondence_tablet"){
   corrBtn='<button id="btnCorr">Correspondence Tablet</button><div id="corrWrap"></div>';
  }
  if(prov) prov.innerHTML=`<h3>${safe(g.title)}</h3><p><strong>Author:</strong> ${safe(g.author)}</p><p><strong>Summary:</strong> ${safe(g.summary)}</p><p><strong>License:</strong> ${safe(p.license)}</p>${questBtns}${corrBtn}<p><a href="${safe(g.path)}" download>Download Source</a></p>${extra}`;
  if(questBtns) prov.querySelectorAll('.startQuest').forEach(btn=>btn.addEventListener('click',()=>startQuest(btn.dataset.q)));
  if(window.recordRead) window.recordRead(g.id);
  if(artifact.id==="correspondence_tablet") prov.querySelector('#btnCorr')?.addEventListener('click',()=>renderCorr(prov.querySelector('#corrWrap')));
  const marks=Object.keys(localStorage).filter(k=>k.startsWith('mark_')).map(k=>k.replace('mark_',''));
  if(marks.length>0 && prov) prov.innerHTML+=`<p>Mark Earned: ${marks.join(', ')}</p>`;
 }

 const corrData=[
  {Letter:"Aleph",Path:"0",Tarot:"Fool",Planet:"Air",Zodiac:"Aries",Stone:"Diamond",Perfume:"Musk"},
  {Letter:"Bet",Path:"1",Tarot:"Magus",Planet:"Mercury",Zodiac:"Taurus",Stone:"Topaz",Perfume:"Sandal"}
 ];
 function renderCorr(container){
  if(!container) return;
  container.innerHTML='<input id="corrFilter" aria-label="Filter correspondences" placeholder="Filter"/><div id="colToggles"></div><table id="corrTable"><thead><tr><th>Letter</th><th>Path</th><th>Tarot</th><th>Planet</th><th>Zodiac</th><th>Stone</th><th>Perfume</th></tr></thead><tbody></tbody></table>';
  const cols=["Letter","Path","Tarot","Planet","Zodiac","Stone","Perfume"];
  const tbody=container.querySelector('tbody');
  const toggles=container.querySelector('#colToggles');
  cols.forEach((c,i)=>{const lbl=document.createElement('label');lbl.innerHTML=`<input type="checkbox" checked data-col="${i}" aria-label="Toggle ${c} column"/>${c}`;lbl.querySelector('input').addEventListener('change',e=>{const idx=e.target.dataset.col;container.querySelectorAll('#corrTable tr').forEach(r=>{r.children[idx].style.display=e.target.checked?'':'none';});});toggles.appendChild(lbl);});
  function renderRows(){const f=container.querySelector('#corrFilter').value.toLowerCase();tbody.innerHTML='';corrData.filter(d=>Object.values(d).some(v=>String(v).toLowerCase().includes(f))).forEach(d=>{const tr=document.createElement('tr');cols.forEach(c=>{const td=document.createElement('td');td.textContent=d[c];tr.appendChild(td);});tbody.appendChild(tr);});}
  container.querySelector('#corrFilter').addEventListener('input',renderRows);
  renderRows();

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
