import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { connect } from './connection.mjs';
const TOKEN='jm01-fixture-token';
async function fixture(t, handler) {
 const server=createServer(handler);
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 t.after(()=>new Promise(resolve=>{server.closeAllConnections();server.close(resolve);}));
 return `http://127.0.0.1:${server.address().port}`;
}
function json(res, value) {res.setHeader('content-type','application/json');res.end(JSON.stringify(value));}
test('independent: successful config/models with preserved prefix and memory bearer',async t=>{
 const paths=[]; const url=await fixture(t,(req,res)=>{paths.push(req.url);assert.equal(req.headers.authorization,`Bearer ${TOKEN}`);json(res,req.url.endsWith('/config')?{version:'fixture'}:[{id:'fixture-model'}]);});
 const actual=await connect(url+'/prefix/',{token:TOKEN,timeoutMs:1000});
 assert.deepEqual(actual,{config:{version:'fixture'},models:[{id:'fixture-model'}]});
 assert.deepEqual(paths,['/prefix/api/config','/prefix/api/models']);
});
for (const status of [401,403]) test(`independent: HTTP ${status}, no bearer leaked`,async t=>{
 const url=await fixture(t,(_req,res)=>{res.statusCode=status;json(res,{error:TOKEN});});
 await assert.rejects(()=>connect(url,{token:TOKEN}),err=>err instanceof Error&&err.message.includes(String(status))&&!err.message.includes(TOKEN));
});
test('independent: timeout is bounded',async t=>{
 const url=await fixture(t,(_req,res)=>{const timer=setTimeout(()=>json(res,{}),300);timer.unref();});
 const start=Date.now();await assert.rejects(()=>connect(url,{timeoutMs:30}));assert.ok(Date.now()-start<1500);
});
test('independent: malformed JSON rejected without leaking response',async t=>{
 const url=await fixture(t,(_req,res)=>{res.end(TOKEN);});
 await assert.rejects(()=>connect(url,{token:TOKEN}),err=>err instanceof Error&&!err.message.includes(TOKEN));
});
test('independent: missing bearer is not added',async t=>{
 const url=await fixture(t,(req,res)=>{assert.equal(req.headers.authorization,undefined);json(res,req.url.endsWith('/config')?{}:[]);});
 assert.deepEqual(await connect(url),{config:{},models:[]});
});
test('independent: unsupported schemes and embedded credentials rejected',async()=>{
 for(const url of ['file:///etc/passwd','ftp://localhost','not-a-url','https://user:password@localhost/']) await assert.rejects(()=>connect(url));
});
test('independent: models HTTP failure is not silently converted to empty array',async t=>{
 const url=await fixture(t,(req,res)=>{if(req.url.endsWith('/models'))res.statusCode=403;json(res,{});});
 await assert.rejects(()=>connect(url),err=>err.message.includes('403'));
});
