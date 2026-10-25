// Codex escalation: execute sendPrompt read from the actual candidate source.
// API and DOM are fixtures: these tests do not prove a real inference/browser run.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source = readFileSync(new URL('../site/app.js', import.meta.url), 'utf8');
const start = source.indexOf('async function sendPrompt(text) {');
const end = source.indexOf('// Mission launch', start);
assert.ok(start >= 0 && end > start, 'Locate the production function, never a copied implementation');
const production = source.slice(start, end);
function harness(request = async () => ({answer: 'Réponse reçue'})) {
  const state = {currentConversation: {id: 'conv1'}, currentProject: 'p', history: [], busy: false,
    messageQueue: [], autoplay: false};
  const els = {sendBtn: {disabled: false}, promptInput: {value: 'question'}, statusText: {textContent: ''}};
  const calls = [];
  const context = vm.createContext({state, els, cfg: {default_model: 'fixture'},
    api: (...args) => { calls.push(args); return request(...args); },
    renderHistory() {}, syncOrb() {}, createNewConversation: async () => {state.currentConversation = {id: 'created'};}});
  vm.runInContext(production, context);
  return {state, els, calls, send: text => context.sendPrompt(text)};
}
const deferred = () => {let resolve; const promise = new Promise(r => {resolve = r;}); return {promise, resolve};};
test('normal request: user then exactly one answer', async () => {
  const h = harness(); await h.send('bonjour');
  assert.equal(h.calls.length, 1); assert.equal(h.state.history.length, 2);
  assert.equal(h.state.history[1].content, 'Réponse reçue'); assert.equal(h.state.busy, false);
  assert.equal(h.els.sendBtn.disabled, false);
});
test('empty response: one visible error, retry text retained', async () => {
  const h = harness(async () => ({answer: ''})); await h.send('question vide');
  assert.equal(h.state.history.length, 2, 'one user and one error, never two errors');
  assert.match(h.state.history[1].content, /Aucune réponse/);
  assert.equal(h.els.promptInput.value, 'question vide'); assert.equal(h.state.pendingRetry, 'question vide');
});
test('network/auth error: visible once and input restored', async () => {
  const h = harness(async () => {throw new Error('HTTP401');}); await h.send('question réseau');
  assert.equal(h.state.history.length, 2); assert.match(h.state.history[1].content, /HTTP401/);
  assert.equal(h.els.promptInput.value, 'question réseau'); assert.equal(h.state.busy, false);
});
test('two rapid requests: serialized, both resolved once', async () => {
  const gate = deferred();
  const h = harness(async (_p, opts) => {if(opts.body.text === 'premier') await gate.promise; return {answer: opts.body.text};});
  const one = h.send('premier'); const two = h.send('second');
  assert.equal(h.calls.length, 1); assert.equal(h.state.messageQueue.length, 1);
  gate.resolve(); await Promise.all([one, two]);
  assert.equal(h.calls.length, 2); assert.equal(h.state.history.length, 4);
  assert.equal(h.state.history.map(m => m.content).join('|'), 'premier|premier|second|second');
  assert.equal(h.state.busy, false);
});
test('queue limit: extra request rejected without an API call', async () => {
  const h = harness(); h.state.busy = true; h.state.messageQueue = Array(5).fill({text: 'waiting'});
  await assert.rejects(h.send('extra'), /File de messages pleine/); assert.equal(h.calls.length, 0);
});
test('spoken field preserved and mission selection still forwarded', async () => {
  const spoken = [], selected = [];
  const h = harness(async () => ({answer: 'Texte détaillé', spoken_answer: 'Texte parlé', mission_id: 'm1'}));
  h.state.autoplay = true; h.state.voiceCtrl = {speak: async t => spoken.push(t)};
  h.state.consoleCtrl = {selectMission: m => selected.push(m)};
  await h.send('parle'); assert.equal(spoken.join(), 'Texte parlé'); assert.equal(selected.join(), 'm1');
});
