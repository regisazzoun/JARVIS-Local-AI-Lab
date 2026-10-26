// Codex provided regression infrastructure; actual renderer/route, explicit fixtures.
import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {renderTelemetry} from '../site/telemetry.js';
class Element {
 constructor(){this.children=[];this.style={};this.textContent='';}
 set innerHTML(v){this.children=[];this.textContent=v;}
 appendChild(n){this.children.push(n);return n;}
 text(){return this.textContent+this.children.map(n=>n.text()).join('\n');}
}
function draw(node){globalThis.document={createElement:()=>new Element()};const el=new Element();renderTelemetry(el,{machines:{'dell-2':node}});return el.text();}
const gpu=name=>({name,utilization:0,temperature:50,vram_used_mb:0,vram_total_mb:24576});
test('actual renderer displays CPU zero and both measured GPU names',()=>{
 const text=draw({available:true,cpu_percent:0,gpus:[gpu('RTX 3090'),gpu('RTX 3080')],sampled_at:Date.now()/1000});
 assert.match(text,/CPU : 0\.0%/);assert.match(text,/RTX 3090/);assert.match(text,/RTX 3080/);assert.match(text,/0%/);
});
test('unknown CPU is never fabricated as zero',()=>{const text=draw({available:true,cpu_percent:null,gpus:[]});assert.doesNotMatch(text,/CPU : 0\.0%/);});
test('absent GPUs occupy two slots labelled not detected',()=>{const text=draw({available:true,gpus:[]});assert.match(text,/GPU1 : non détecté/);assert.match(text,/GPU2 : non détecté/);});
test('offline node states unavailability and its reason',()=>{const text=draw({available:false,gpus:[],reason:'fixture SSH indisponible'});assert.match(text,/indisponible/);assert.match(text,/fixture SSH indisponible/);});
test('stale actual-renderer sample is labelled old',()=>{assert.match(draw({available:true,gpus:[],sampled_at:Date.now()/1000-45}),/ancien/);});
test('unmeasured GPU utilization is labelled N/A',()=>{assert.match(draw({available:true,gpus:[{name:'fixture GPU',utilization:null}]}),/N\/A/);});
test('actual backend Handler consumes Dell2 probe and propagates zero/two GPUs',()=>{
 const result=spawnSync('python3',[new URL('./d17-route.py',import.meta.url).pathname],{encoding:'utf8'});
 assert.equal(result.status,0,result.stdout+result.stderr);
});
