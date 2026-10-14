'use strict';
const $=id=>document.getElementById(id);let config,conversation=null,busy=false,recorder,stream,timer,chunks=[],audio,objectURL,voiceEpoch=0,recordPending=false,held=false,finishPlayback,lastAnswer='';
let vadStream=null,vadContext=null,vadNode=null,vadActive=false,vadFrames=[],vadPre=[],vadPreSize=0,vadSamples=0,vadVoiced=0,vadStart=0,vadLast=0,vadOnset=0,vadCooldown=0,vadSending=false;
const state=t=>{$('state').textContent=t;};const error=e=>{$('error').textContent=e?.message||String(e);};
async function api(path,data,raw=false){const control=new AbortController();const timeout=setTimeout(()=>control.abort(),300000);try{const options={signal:control.signal};if(data!==undefined){options.method='POST';options.headers={'X-Jarvis-Request':'1','Content-Type':raw?'application/octet-stream':'application/json'};options.body=raw?data:JSON.stringify(data);}const r=await fetch(path,options);if(!r.ok){let d;try{d=await r.json();}catch{d={error:'Erreur HTTP '+r.status};}if(r.status===401){$('workspace').hidden=true;$('loginpanel').hidden=false;}throw new Error(d.error);}return r.headers.get('Content-Type').startsWith('audio/')?r.blob():r.json();}catch(e){if(e.name==='AbortError')throw new Error('Délai dépassé. Le serveur peut encore terminer son opération.');throw e;}finally{clearTimeout(timeout);}}
function add(role,text){const el=document.createElement('article');el.className=role;const b=document.createElement('b');b.textContent=role==='user'?'VOUS':'JARVIS';el.append(b,document.createTextNode(text));$('history').append(el);el.scrollIntoView({block:'nearest'});}
function stop(){voiceEpoch++;if(finishPlayback){finishPlayback();finishPlayback=null;}if(audio){audio.pause();audio.src='';audio=null;}if(objectURL){URL.revokeObjectURL(objectURL);objectURL=null;}state('Lecture arrêtée');}
function setBusy(v){busy=v;$('send').disabled=v;$('new').disabled=v;$('conversations').disabled=v;$('ptt').disabled=v;$('retain').disabled=v;}
async function talk(text){stop();const epoch=voiceEpoch;const parts=text.match(/[^.!?]+[.!?]*|[.!?]+/g)||[text];const chunks=[];let chunk='';for(const part of parts){if((chunk+part).length>600&&chunk){chunks.push(chunk);chunk='';}for(let i=0;i<part.length;i+=600){const segment=part.slice(i,i+600);if((chunk+segment).length>600){chunks.push(chunk);chunk='';}chunk+=segment;}}if(chunk.trim())chunks.push(chunk);for(const part of chunks){if(epoch!==voiceEpoch)return;state('Synthèse vocale');const blob=await api('/api/tts',{text:part});if(epoch!==voiceEpoch)return;objectURL=URL.createObjectURL(blob);audio=$('player');audio.src=objectURL;state('Lecture vocale');await new Promise((resolve,reject)=>{finishPlayback=resolve;audio.onended=resolve;audio.onerror=()=>reject(new Error('Lecture audio impossible'));audio.play().catch(()=>state('Audio prêt · appuyer sur ▶ dans le lecteur'));});finishPlayback=null;if(epoch!==voiceEpoch)return;if(objectURL){URL.revokeObjectURL(objectURL);objectURL=null;}}audio=null;vadCooldown=performance.now()+600;state(vadActive?'Écoute · parlez':'Prêt');}
$('stop').onclick=stop;
$('form').onsubmit=async e=>{e.preventDefault();if(busy||recordPending||recorder?.state==='recording')return;const text=$('text').value.trim();if(!text)return;setBusy(true);stop();$('error').textContent='';state('Réflexion du modèle');try{const d=await api('/api/chat',{text,model:$('model').value,conversation,project:$('project').value,retain:$('retain').checked,agent_mode:$('labmode').checked});conversation=d.conversation;lastAnswer=d.spoken_answer||d.answer;await memories();add('user',text);add('assistant',d.answer);$('text').value='';if($('speak').checked)await talk(lastAnswer);else state('Prêt');await loadConversations();}catch(e){error(e);state('Erreur');}finally{setBusy(false);}};
async function begin(){if(vadActive)await stopVad();if(busy||recordPending)return;held=true;recordPending=true;setBusy(true);$('ptt').disabled=false;try{if(!window.isSecureContext||!navigator.mediaDevices)throw new Error('Microphone : ouvrir localhost par tunnel SSH.');stop();stream=await navigator.mediaDevices.getUserMedia({audio:true});if(!held){stream.getTracks().forEach(t=>t.stop());return;}chunks=[];recorder=new MediaRecorder(stream);recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onstop=async()=>{clearTimeout(timer);stream.getTracks().forEach(t=>t.stop());$('ptt').classList.remove('recording');setBusy(true);state('Transcription');try{const data=new Blob(chunks,{type:recorder.mimeType});chunks=[];const d=await api('/api/stt',data,true);$('text').value=d.text;state('Transcription prête · vérifier puis envoyer');if($('autosend').checked)setTimeout(()=>$('form').requestSubmit(),0);}catch(e){error(e);state('Erreur');}finally{setBusy(false);}};recorder.start();state('Enregistrement');$('ptt').classList.add('recording');timer=setTimeout(end,config.max_record_seconds*1000);}catch(e){stream?.getTracks().forEach(t=>t.stop());error(e);state('Erreur');}finally{recordPending=false;if(recorder?.state!=='recording')setBusy(false);}}
function end(){held=false;if(recorder?.state==='recording')recorder.stop();}
$('ptt').onpointerdown=e=>{e.preventDefault();$('ptt').setPointerCapture(e.pointerId);begin();};$('ptt').onpointerup=end;$('ptt').onpointercancel=end;$('ptt').onkeydown=e=>{if((e.code==='Space'||e.code==='Enter')&&!e.repeat){e.preventDefault();begin();}};$('ptt').onkeyup=e=>{if(e.code==='Space'||e.code==='Enter')end();};window.addEventListener('blur',end);
$('new').onclick=()=>{stop();conversation=null;$('history').replaceChildren();state('Prêt');};$('retain').onchange=()=>{$('new').click();};
async function loadConversations(){const rows=await api('/api/conversations');$('conversations').replaceChildren(new Option('Choisir…',''));for(const r of rows)$('conversations').add(new Option(r.created+' · '+r.project,r.id));}
$('reload').onclick=()=>loadConversations().catch(error);$('conversations').onchange=async()=>{if(!$('conversations').value)return;try{stop();conversation=$('conversations').value;$('retain').checked=true;$('history').replaceChildren();for(const r of await api('/api/history?id='+encodeURIComponent(conversation)))add(r.role,r.content);}catch(e){error(e);}};
async function memories(){const rows=await api('/api/memories');$('memories').replaceChildren();for(const r of rows){const el=document.createElement('div');el.className='memory';const p=document.createElement('p');p.textContent=r.content+' · '+r.kind+' · '+r.status+' · '+r.project+(r.active?'':' · obsolète');el.append(p);function button(label,action){const b=document.createElement('button');b.textContent=label;b.onclick=async()=>{try{await action();await memories();}catch(e){error(e);}};el.append(b);}if(r.status==='pending'){button('Approuver explicitement',()=>api('/api/memory/approve',{id:r.id,explicit:true}));button('Refuser',()=>api('/api/memory/reject',{id:r.id}));}if(r.status==='approved'&&r.active)button('Modifier et valider',async()=>{const content=prompt('Contenu validé',r.content);if(content===null)return;const project=prompt('Projet associé (vide pour global)',r.project);if(project===null)return;return api('/api/memory/edit',{id:r.id,content,project,explicit:true});});if(r.status==='approved'&&r.active)button('Marquer obsolète',()=>api('/api/memory/obsolete',{id:r.id,explicit:true}));button('Supprimer',()=>api('/api/memory/delete',{id:r.id}));$('memories').append(el);}}
$('propose').onclick=async()=>{try{if($('kind').value==='temporary'&&!conversation)throw new Error('Commencer une conversation avant une mémoire temporaire.');await api('/api/memory/propose',{content:$('memory').value,kind:$('kind').value,project:$('project').value,conversation});$('memory').value='';await memories();}catch(e){error(e);}};$('refreshmem').onclick=()=>memories().catch(error);
$('search').onclick=async()=>{try{$('results').textContent=JSON.stringify(await api('/api/search?q='+encodeURIComponent($('query').value)+'&project='+encodeURIComponent($('project').value)+'&type='+$('searchtype').value),null,2);}catch(e){error(e);}};
async function initialize(){config=await api('/api/config');$('model').replaceChildren();for(const model of config.models)$('model').add(new Option(model,model));$('model').value=config.default_model;await loadConversations();await memories();const prefs=await api('/api/preferences');$('voiceLength').value=prefs.voice_length||'short';$('loginpanel').hidden=true;$('workspace').hidden=false;state('Prêt');}
$('loginform').onsubmit=async e=>{e.preventDefault();try{await api('/api/login',{username:$('username').value,password:$('password').value});$('password').value='';await initialize();}catch(e){$('loginerror').textContent=e.message;}};
$('logout').onclick=async()=>{await stopVad();stop();end();await api('/api/logout',{});$('workspace').hidden=true;$('loginpanel').hidden=false;$('history').replaceChildren();conversation=null;};
$('togglemic').onclick=()=>{if(recorder?.state==='recording'||recordPending)end();else begin();};
$('replay').onclick=async()=>{if(!lastAnswer||busy)return;setBusy(true);try{await talk(lastAnswer);}catch(e){error(e);}finally{setBusy(false);}};
(async()=>{try{const s=await api('/api/session');if(s.authenticated)await initialize();}catch(e){$('loginerror').textContent=e.message;}})();

function wavBlob(frames,rate){
 const size=frames.reduce((n,f)=>n+f.length,0);const buf=new ArrayBuffer(44+size*2),v=new DataView(buf);
 function ascii(at,s){for(let i=0;i<s.length;i++)v.setUint8(at+i,s.charCodeAt(i));}
 ascii(0,'RIFF');v.setUint32(4,36+size*2,true);ascii(8,'WAVE');ascii(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,rate,true);v.setUint32(28,rate*2,true);v.setUint16(32,2,true);v.setUint16(34,16,true);ascii(36,'data');v.setUint32(40,size*2,true);
 let pos=44;for(const frame of frames)for(const x of frame){v.setInt16(pos,Math.round(Math.max(-1,Math.min(1,x))*32767),true);pos+=2;}
 return new Blob([buf],{type:'audio/wav'});
}
function resetVad(){vadFrames=[];vadPre=[];vadPreSize=0;vadSamples=0;vadVoiced=0;vadStart=0;vadOnset=0;}
async function stopVad(){
 vadActive=false;vadNode?.disconnect();vadStream?.getTracks().forEach(t=>t.stop());if(vadContext)await vadContext.close();vadNode=null;vadContext=null;vadStream=null;resetVad();$('vad').textContent='Conversation automatique';
}
async function finishVad(){
 const frames=vadFrames,rate=vadContext.sampleRate,voiced=vadVoiced;resetVad();vadCooldown=performance.now()+600;
 if(voiced<0.25||vadSending)return;
 vadSending=true;state('Transcription automatique');
 try{
  const deadline=performance.now()+10000;while(busy&&performance.now()<deadline)await new Promise(r=>setTimeout(r,100));
  if(busy)throw new Error('Opération précédente en cours. Réessayez après sa fin.');
  setBusy(true);const d=await api('/api/stt',wavBlob(frames,rate),true);$('text').value=d.text;
  setBusy(false);state('Transcription prête');if(vadActive&&$('autosend').checked)setTimeout(()=>$('form').requestSubmit(),0);
 }catch(e){error(e);state('Erreur de transcription · écoute reprise');}finally{setBusy(false);vadSending=false;vadCooldown=performance.now()+600;}
}
function vadFrame(frame){
 if(!vadActive||vadSending||performance.now()<vadCooldown)return;
 const playing=audio&&!audio.paused;
 if(busy&&!(playing&&$('barge').checked)){resetVad();return;}
 const now=performance.now(),rate=vadContext.sampleRate;let energy=0;for(const x of frame)energy+=x*x;
 const rms=Math.sqrt(energy/frame.length),threshold=playing?0.035:0.012;const voiced=rms>threshold;
 if(!vadStart){
  vadPre.push(frame);vadPreSize+=frame.length;while(vadPreSize>rate*.3&&vadPre.length>1)vadPreSize-=vadPre.shift().length;
  if(voiced){if(!vadOnset)vadOnset=now;if(now-vadOnset>=140){if(playing)stop();vadStart=now;vadLast=now;vadFrames=vadPre.slice();vadSamples=vadPreSize;vadVoiced=.14;vadPre=[];vadPreSize=0;state('Parole détectée');}}
  else vadOnset=0;
 }else{
  vadFrames.push(frame);vadSamples+=frame.length;if(voiced){vadLast=now;vadVoiced+=frame.length/rate;}
  if(now-vadLast>850||vadSamples>=rate*Math.min(40,config.max_record_seconds-1))finishVad();
 }
}
$('vad').onclick=async()=>{
 if(vadActive){await stopVad();state('Écoute automatique arrêtée');return;}
 if(busy||recorder?.state==='recording')return;
 try{
  if(!isSecureContext||!navigator.mediaDevices)throw new Error('Microphone : ouvrir localhost par tunnel SSH.');
  stop();vadStream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
  vadContext=new AudioContext();await vadContext.audioWorklet.addModule('/vad-worklet.js');await vadContext.resume();
  const source=vadContext.createMediaStreamSource(vadStream);vadNode=new AudioWorkletNode(vadContext,'jarvis-capture');source.connect(vadNode);vadNode.connect(vadContext.destination);vadNode.port.onmessage=e=>vadFrame(e.data);
  resetVad();vadActive=true;$('vad').textContent='Arrêter la conversation automatique';state('Écoute · parlez');
 }catch(e){await stopVad();error(e);}
};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&vadActive)stopVad();});
window.addEventListener('pagehide',()=>{stopVad();});

$('voiceLength').onchange=async()=>{try{await api('/api/preferences',{key:'voice_length',value:$('voiceLength').value});await memories();}catch(e){error(e);}};
