// Durable missions use the same authenticated API and selected model as chat.
{
  const panel=document.createElement('details'), summary=document.createElement('summary');
  summary.textContent='Missions persistantes · reprise et progression';panel.append(summary);
  const submit=document.createElement('button'), refresh=document.createElement('button'), output=document.createElement('pre');
  submit.type=refresh.type='button';submit.textContent='Confier le message saisi comme mission';refresh.textContent='Actualiser les missions';
  async function showMissions(){
    const rows=await api('/api/missions');
    output.textContent=JSON.stringify(rows.map(m=>({id:m.id,objectif:m.goal,état:m.state,tentatives:m.attempts,outils_validés:m.validated_tools,progression:m.progress,tâches:m.tasks,dernière_activité:new Date(m.updated*1000).toLocaleString()})),null,2);
  }
  submit.onclick=async()=>{try{const goal=$('text').value.trim();if(!goal)throw new Error('Saisissez un objectif dans votre message.');const m=await api('/api/missions',{goal,model:$('model').value});output.textContent='Mission enregistrée : '+m.id;await showMissions();}catch(e){error(e);}};
  refresh.onclick=async()=>{try{await showMissions();}catch(e){error(e);}};
  const ident=document.createElement('input'), resume=document.createElement('button');ident.placeholder='Identifiant de mission à reprendre';resume.type='button';resume.textContent='Reprendre';resume.onclick=async()=>{try{await api('/api/missions/resume',{id:ident.value.trim()});await showMissions();}catch(e){error(e);}};
  panel.append(submit,refresh,ident,resume,output);$('workspace').append(panel);
}
