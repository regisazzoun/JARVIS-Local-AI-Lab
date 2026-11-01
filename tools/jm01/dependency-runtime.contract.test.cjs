process.env.TZ='Europe/Paris';
const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');const vm=require('node:vm');const {createRequire}=require('node:module');
const projectRoot=process.env.JM01_CLIENT_ROOT||path.join(__dirname,'../../clients/mobile');const req=createRequire(path.join(projectRoot,'package.json'));req('reflect-metadata');const ct=req('class-transformer');const dayjs=req('dayjs');
function transform(mode){
 const file=path.join(projectRoot,'node_modules/@ronas-it/rtkq-entity-api/dist',mode==='cjs'?'index.js':'index.mjs');const source=fs.readFileSync(file,'utf8');const start=source.indexOf('// src/utils/class-transformer/transform-date.ts');assert.ok(start>=0);const next=source.indexOf('\n// src/',start+4);let code=source.slice(start,next<0?undefined:next);
 if(mode==='esm'){code=code.replace(/import \{ Transform as Transform2 \} from "class-transformer";/,'const Transform2=require("class-transformer").Transform;').replace(/import dayjs from "dayjs";/,'const dayjs=require("dayjs");').replace(/import utc from "dayjs\/plugin\/utc.js";/,'const utc=require("dayjs/plugin/utc");').replace(/import customParseFormat from "dayjs\/plugin\/customParseFormat.js";/,'const customParseFormat=require("dayjs/plugin/customParseFormat");');}
 return vm.runInNewContext(code+'\nTransformDate;',{require:req,Reflect});
}
for(const mode of ['cjs','esm']){
 const decorate=transform(mode);
 function model(options){class Entity{}ct.Expose()(Entity.prototype,'value');ct.Type(()=>dayjs)(Entity.prototype,'value');decorate(options)(Entity.prototype,'value');return Entity;}
 test(mode+': ISO date becomes Dayjs and roundtrips UTC',()=>{const C=model({});const v=ct.plainToInstance(C,{value:'2026-11-02T00:30:00.000Z'});assert.ok(dayjs.isDayjs(v.value));assert.equal(ct.instanceToPlain(v).value,'2026-11-02T00:30:00.000Z');});
 test(mode+': formatted date is serialized in UTC per upstream contract',()=>{const C=model({format:'DD/MM/YYYY'});const v=ct.plainToInstance(C,{value:'02/11/2026'});assert.ok(dayjs.isDayjs(v.value));assert.equal(ct.instanceToPlain(v).value,'01/11/2026');});
 test(mode+': dateOnly returns calendar date',()=>{const C=model({dateOnly:true});const v=ct.plainToInstance(C,{value:'2026-11-02T00:30:00Z'});assert.equal(ct.instanceToPlain(v).value,'2026-11-02');});
 test(mode+': null stays null',()=>{const C=model({});assert.equal(ct.plainToInstance(C,{value:null}).value,null);});
}
