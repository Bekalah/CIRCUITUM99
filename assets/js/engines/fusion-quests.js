(()=>{
 "use strict";
 let questsIndex={};
 function safeFetchJSON(path){return fetch(path,{cache:"no-store"}).then(r=>r.json());}
 async function loadQuests(){const data=await safeFetchJSON("/assets/data/fusion/quests.json");questsIndex=Object.fromEntries((data.quests||[]).map(q=>[q.id,q]));}

 function startQuest(id){const q=questsIndex[id];if(!q) return alert("Quest not found.");localStorage.setItem(`quest_${id}_started`,`true`);alert("Quest started: "+q.title);}
 function isQuestStarted(id){return localStorage.getItem(`quest_${id}_started`)==="true";}
 function recordRead(textId){Object.values(questsIndex).forEach(q=>{(q.steps||[]).forEach(s=>{if(s.action==="read"&&s.text_id===textId&&isQuestStarted(q.id)){localStorage.setItem(`quest_${q.id}_${s.id}`,"done");checkCompletion(q);}});});}
 function recordLoot(artifactId){Object.values(questsIndex).forEach(q=>{(q.steps||[]).forEach(s=>{if(s.action==="loot"&&s.artifact_id===artifactId&&isQuestStarted(q.id)){localStorage.setItem(`quest_${q.id}_${s.id}`,"done");checkCompletion(q);}});});}
 function checkCompletion(q){const done=(q.steps||[]).every(s=>localStorage.getItem(`quest_${q.id}_${s.id}`)==="done");if(done&&!localStorage.getItem(`quest_${q.id}_complete`)){localStorage.setItem(`quest_${q.id}_complete`,"true");const marks=(window.checkMarks?window.checkMarks():[]);q.rewards.forEach(m=>{if(marks.includes(m)) localStorage.setItem(`mark_${m}`,"earned");});alert(`Quest complete: ${q.title}`);}}
 function getQuestsForArtifact(id){return Object.values(questsIndex).filter(q=>q.requires.includes(id));}

 function startQuest(id){const q=questsIndex[id];if(!q) return alert("Quest not found.");localStorage.setItem("quest_"+id+"_started","true");alert("Quest started: "+q.title);}
 function recordRead(textId){Object.values(questsIndex).forEach(q=>{(q.steps||[]).forEach(s=>{if(s.action==="read"&&s.text_id===textId){localStorage.setItem(`quest_${q.id}_${s.id}`,"done");checkCompletion(q);}});});}
 function recordLoot(artifactId){Object.values(questsIndex).forEach(q=>{(q.steps||[]).forEach(s=>{if(s.action==="loot"&&s.artifact_id===artifactId){localStorage.setItem(`quest_${q.id}_${s.id}`,"done");checkCompletion(q);}});});}
 function checkCompletion(q){const done=(q.steps||[]).every(s=>localStorage.getItem(`quest_${q.id}_${s.id}`)==="done");if(done&&!localStorage.getItem(`quest_${q.id}_complete`)){localStorage.setItem(`quest_${q.id}_complete`,"true");alert(`Quest complete: ${q.title}`);}}

 document.addEventListener("DOMContentLoaded",loadQuests);
 window.startQuest=startQuest;
 window.recordRead=recordRead;
 window.recordLoot=recordLoot;

 window.getQuestsForArtifact=getQuestsForArtifact;
 window.isQuestStarted=isQuestStarted;

})();
