/* Codex browser measurement/RTC support tool. JARVIS page integration is separate. */
(() => {
 'use strict';
 const $=id=>document.getElementById(id), started=performance.now();
 const data={actor:'JARVIS page + Codex client tool',physicalMicrophoneTested:false,events:[],transcripts:[],tests:[]};
 let room=null,credentials=null,ctx=null,dest=null,wavTrack=null,source=null,recorder=null,audioBlob=null,audioParts=[],job=null,busy=false,stopping=false;
 const advanced=document.createElement('details');const summary=document.createElement('summary');summary.textContent='Paramètres avancés';advanced.appendChild(summary);const firstLabel=document.querySelector('label[for="url"]');firstLabel.before(advanced);for(const n of [firstLabel,$('url'),document.querySelector('label[for="tokenApi"]'),$('tokenApi'),$('gettoken'),$('tokenStatus')])advanced.appendChild(n);document.querySelector('label[for="wavFile"]').textContent='Fichier WAV (mono recommandé)';for(const h of document.querySelectorAll('h2'))if(h.textContent==='Connexion LiveKit')h.textContent='Conversation avec JARVIS';
 const outputs=[];let levelTimer=null,lastLoud=-Infinity,lastRms=0;
 const meter=document.createElement('output');meter.setAttribute('aria-label','Niveau audio JARVIS');meter.textContent='Audio JARVIS : silence';$('status').after(meter);
 const box=document.createElement('div');box.id='rtc-audio';document.body.appendChild(box);
 function event(type,values={}) {$('logs').textContent+=new Date().toISOString()+' '+type+' '+JSON.stringify(values)+'\n';data.events.push({utc:new Date().toISOString(),t:(performance.now()-started)/1000,type,...values});$('exportData').textContent=JSON.stringify(data,null,2);}
 function status(text){$('status').textContent=text;}
 function log(text){$('log').textContent+=text+'\n';}
 function download(blob,name){const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),2000);}
 function button(label,handler){const b=document.createElement('button');b.textContent=label;b.onclick=()=>handler().catch(e=>{status(e.message);event('error',{message:e.message});});$('exportJson').parentElement.appendChild(b);return b;}
 async function token(){const r=await fetch('/token');if(!r.ok)throw Error('Jeton : HTTP '+r.status);credentials=await r.json();$('tokenStatus').textContent='Salle temporaire prête';event('room_created',{room:credentials.room});return credentials;}
 async function audioContext(){if(!ctx)ctx=new AudioContext();await ctx.resume();return ctx;}
 async function connect(){
  if(room)return;status('Connexion à JARVIS…');audioBlob=null;let remoteReadyResolve;const remoteReady=new Promise(resolve=>remoteReadyResolve=resolve);
  const c=await token();await audioContext();
  room=new LivekitClient.Room();
  room.on(LivekitClient.RoomEvent.TranscriptionReceived,(segments,peer)=>{
   for(const s of segments){if(!s.final)continue;const agent=peer?.isAgent||peer?.identity?.startsWith('agent-');const entry={speaker:agent?'JARVIS':'Utilisateur',text:s.text};data.transcripts.push(entry);(agent?$('agentTexts'):$('transcripts')).textContent+=entry.speaker+' : '+entry.text+'\n';event('transcription_final',entry);}
  });
  room.on(LivekitClient.RoomEvent.TrackSubscribed,(track,pub,peer)=>{
   if(track.kind!==LivekitClient.Track.Kind.Audio)return;
   const el=track.attach();el.autoplay=true;box.appendChild(el);outputs.push(el);event('remote_audio_track',{peer:peer.identity});remoteReadyResolve();
   const stream=new MediaStream([track.mediaStreamTrack]);
   const input=ctx.createMediaStreamSource(stream),analyser=ctx.createAnalyser();analyser.fftSize=1024;input.connect(analyser);const samples=new Float32Array(1024);
   if(levelTimer)clearInterval(levelTimer);levelTimer=setInterval(()=>{analyser.getFloatTimeDomainData(samples);lastRms=Math.sqrt(samples.reduce((a,b)=>a+b*b,0)/samples.length)*32768;if(lastRms>20)lastLoud=performance.now();meter.textContent='Audio JARVIS : RMS '+lastRms.toFixed(1);data.events.push({utc:new Date().toISOString(),t:(performance.now()-started)/1000,type:'received_pcm_level',rms:lastRms,sample_rate:ctx.sampleRate});},100);
   if(typeof MediaRecorder!=='undefined'&&!recorder){audioParts=[];recorder=new MediaRecorder(stream);recorder.ondataavailable=e=>{if(e.data.size)audioParts.push(e.data);};const activeRecorder=recorder;recorder.onstop=()=>{audioBlob=new Blob(audioParts,{type:activeRecorder.mimeType});event('audio_recorded',{bytes:audioBlob.size,mime:audioBlob.type});};recorder.start(1000);}
  });
  room.on(LivekitClient.RoomEvent.Disconnected,()=>{event('rtc_disconnected');if(!stopping)status('Déconnecté');});
  await room.connect(c.url,c.token);await room.startAudio();await new Promise((resolve,reject)=>{const timeout=setTimeout(()=>reject(Error('Agent audio indisponible après20s')),20000);remoteReady.then(()=>{clearTimeout(timeout);resolve();});});
  if($('sourceMode').value==='mic'){await room.localParticipant.setMicrophoneEnabled(true);event('microphone_enabled');}
  else{
   dest=ctx.createMediaStreamDestination();wavTrack=new LivekitClient.LocalAudioTrack(dest.stream.getAudioTracks()[0]);
   await room.localParticipant.publishTrack(wavTrack,{source:LivekitClient.Track.Source.Microphone});event('wav_track_published');
  }
  $('start').disabled=true;$('stop').disabled=false;$('testBargeIn').disabled=false;status('Connecté — JARVIS écoute');event('connected',{room:c.room});
 }
 async function play(buffer,label){await connect();if($('sourceMode').value!=='wav')throw Error('Choisir le mode WAV pour ce test');await audioContext();if(source)source.stop();const decoded=await ctx.decodeAudioData(buffer.slice(0));source=ctx.createBufferSource();source.buffer=decoded;source.connect(dest);event('wav_started',{label,duration:decoded.duration});await new Promise(resolve=>{source.onended=()=>{event('wav_ended',{label});resolve();};source.start();});}
 async function fixture(name){const r=await fetch('/fixtures/'+name+'.wav');if(!r.ok)throw Error('WAV indisponible');await play(await r.arrayBuffer(),name);}
 async function stop(){const start=performance.now(),activeBeforeStop=performance.now()-lastLoud<=200;stopping=true;
  if(source){try{source.stop();}catch{}source=null;}
  if(job){await fetch('/test/stop',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:job})});event('test_stop_requested',{id:job});}
  for(const el of outputs){el.pause();el.srcObject=null;el.remove();}outputs.length=0;
  if(levelTimer){clearInterval(levelTimer);levelTimer=null;}meter.textContent='Audio JARVIS : arrêté';event('local_audio_stopped',{elapsed_ms:performance.now()-start,audio_active_in_previous_200ms:activeBeforeStop,last_rms:lastRms,remaining_audio_elements:box.querySelectorAll('audio').length});
  if(recorder&&recorder.state!=='inactive')recorder.stop();recorder=null;
  if(room){await room.localParticipant.setMicrophoneEnabled(false).catch(()=>{});await room.disconnect();room=null;}
  if(wavTrack){wavTrack.stop();wavTrack=null;}
  if(credentials){await fetch('/stop',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({room:credentials.room})});credentials=null;}
  if(ctx){await ctx.close();ctx=null;dest=null;}
  $('start').disabled=false;$('stop').disabled=true;$('testBargeIn').disabled=false;status('Arrêté');event('stopped');setTimeout(()=>event('stop_observation_2s',{session_still_disconnected:room===null,audio_elements:box.querySelectorAll('audio').length}),2000);stopping=false;
 }
 async function test(){
  if(busy)throw Error('Un test est déjà en cours');busy=true;$('stop').disabled=false;$('testBargeIn').disabled=true;
  try{const r=await fetch('/test',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenario:scenario.value})});const first=await r.json();if(!r.ok)throw Error(first.error||'Test refusé');job=first.id;event('test_started',{id:job,scenario:scenario.value});status('Test WAV réel en cours — sans microphone');
   for(let i=0;i<360;i++){await new Promise(resolve=>setTimeout(resolve,1000));const response=await fetch('/test/'+job);const v=await response.json();if(v.done){const finalStatus=v.result?.status||((v.returncode===-2||v.returncode===130)?'ABORTED':'FAIL');data.tests.push({...v,status:finalStatus});event('test_finished',{id:job,returncode:v.returncode,status:finalStatus,captured_result_present:!!v.result});status(finalStatus==='PASS'?'Test terminé : PASS':finalStatus==='ABORTED'?'Test interrompu':'Test terminé : FAIL / voir résultats');if(v.audio&&v.result){const link=document.createElement('a');link.href=v.audio;link.textContent='Télécharger le WAV reçu';link.download='received.wav';$('exportJson').parentElement.appendChild(link);}job=null;return;}}
   throw Error('Test encore actif après360s — consulter le rapport serveur');
  }finally{busy=false;$('testBargeIn').disabled=false;if(!room)$('stop').disabled=true;}
 }
 $('gettoken').onclick=()=>token().catch(e=>status(e.message));
 $('start').onclick=()=>connect().catch(e=>{status(e.message);event('error',{message:e.message});});
 $('stop').onclick=()=>stop().catch(e=>status(e.message));
 $('testBargeIn').disabled=false;$('testBargeIn').textContent='Lancer le test WAV automatique';$('testBargeIn').onclick=()=>test().catch(e=>status(e.message));
 $('exportJson').onclick=()=>download(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),'jarvis-23d-results.json');
 $('sourceMode').value='wav';$('wavSection').style.display='block';$('sourceMode').onchange=()=>{$('wavSection').style.display=$('sourceMode').value==='wav'?'block':'none';};
 const scenario=document.createElement('select');scenario.id='testScenario';scenario.setAttribute('aria-label','Scénario automatique');
 for(const [value,label] of [['barge-early','Interruption précoce'],['barge-late','Interruption tardive'],['nominal','Conversation nominale'],['silence','Silence'],['noise','Bruit sans mots']]){const o=document.createElement('option');o.value=value;o.textContent=label;scenario.appendChild(o);}
 $('testBargeIn').before(scenario);
 button('Envoyer le scénario musée',()=>fixture('initial'));
 button('Interrompre : dimanche10h20€',()=>fixture('interrupt'));
 button('Question de continuité',()=>fixture('continuity'));
 button('Envoyer le WAV choisi',async()=>{const f=$('wavFile').files[0];if(!f)throw Error('Choisir un fichier WAV');await play(await f.arrayBuffer(),f.name);});
 button('Exporter audio conversation',async()=>{if(!audioBlob)throw Error('Arrêter la session pour finaliser l’audio');download(audioBlob,'jarvis-conversation.'+(audioBlob.type.includes('mp4')?'mp4':'webm'));});
 event('client_ready');status('Prêt — micro ou WAV, tests sans microphone');
})();
