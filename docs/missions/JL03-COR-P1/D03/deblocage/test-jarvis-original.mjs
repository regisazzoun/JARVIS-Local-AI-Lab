import { test } from 'node:test';
import assert from 'node:assert';

function makeState() {
  return {
    currentConversation: { id: 'conv-1' },
    history: [],
    busy: false,
    messageQueue: [],
    error: null,
    pendingRetry: null,
    currentProject: 'proj-1',
    autoplay: false,
  };
}

function makeEls() {
  return {
    sendBtn: { disabled: false },
    promptInput: { value: '' },
    statusText: { textContent: '' },
  };
}

function syncOrb(state) {
  state.phase = state.busy ? 'thinking' : 'listening';
}

function renderHistory() {
  // Pas de DOM → pas d'effet
}

async function api(endpoint, { method, body }) {
  if (body.text === 'erreur-reseau') {
    const err = new Error('Erreur réseau 401');
    err.status = 401;
    throw err;
  }
  if (body.text === 'erreur-vide') {
    return { answer: '' };
  }
  if (body.text === 'ok') {
    return { answer: 'Réponse normale', spoken_answer: '' };
  }
  if (body.text === 'erreur-vide-api') {
    return { answer: '' };
  }
  return { answer: 'Réponse par défaut', spoken_answer: '' };
}

async function sendPrompt(text, state, els) {
  if (!text) return;
  if (state.busy) {
    state.messageQueue ??= [];
    if (state.messageQueue.length >= 5) throw new Error('File de messages pleine ; attendre la réponse en cours.');
    return new Promise((resolve, reject) => state.messageQueue.push({ text, resolve, reject }));
  }
  state.error = null;
  state.busy = true;
  els.sendBtn.disabled = true;
  els.promptInput.value = '';
  const userMsg = { role: 'user', content: text };
  state.history.push(userMsg);
  renderHistory();
  syncOrb(state);
  state.pendingRetry = text;
  try {
    const res = await api('/api/chat', {
      method: 'POST',
      body: {
        text,
        model: null,
        conversation: state.currentConversation.id,
        project: state.currentProject,
        retain: true,
        agent_mode: false,
      },
    });
    if (res?.answer) {
      const assistantMsg = { role: 'assistant', content: res.answer };
      state.history.push(assistantMsg);
      renderHistory();
      state.pendingRetry = null;
    } else {
      state.history.push({ role: 'system', content: '[ERREUR] Aucune réponse reçue du serveur.' });
      renderHistory();
      throw new Error('Réponse vide');
    }
  } catch (e) {
    const errMessage = `[ERREUR] ${e.message}`;
    state.error = errMessage;
    els.statusText.textContent = errMessage;
    state.history.push({ role: 'system', content: errMessage });
    renderHistory();
    state.pendingRetry = text;
    els.promptInput.value = text;
  } finally {
    state.busy = false;
    els.sendBtn.disabled = false;
    syncOrb(state);
    const next = state.messageQueue?.shift();
    if (next) sendPrompt(next.text, state, els).then(next.resolve, next.reject);
  }
}

test('D03 - Message normal → ajout dans historique', async () => {
  const state = makeState();
  const els = makeEls();
  await sendPrompt('ok', state, els);
  assert.equal(state.history.length, 2, 'un message utilisateur + une réponse');
  assert.equal(state.history[0].role, 'user');
  assert.equal(state.history[1].role, 'assistant');
  assert.equal(state.history[1].content, 'Réponse normale');
});

test('D03 - File pleine → exception levée', async () => {
  const state = makeState();
  const els = makeEls();
  state.busy = true;
  state.messageQueue = [];
  for (let i = 0; i < 5; i++) {
    state.messageQueue.push({ text: `msg-${i}`, resolve: () => {}, reject: () => {} });
  }

  let caught = false;
  try {
    await sendPrompt('msg-6', state, els);
  } catch (e) {
    caught = true;
    assert.equal(e.message, 'File de messages pleine ; attendre la réponse en cours.');
  }
  assert.equal(caught, true, 'Exception attendue pour file pleine');
});

test('D03 - Erreur réseau 401 → message [ERREUR] dans historique', async () => {
  const state = makeState();
  const els = makeEls();
  await sendPrompt('erreur-reseau', state, els);
  assert.equal(state.history.length, 2, 'un message utilisateur + une erreur système');
  assert.equal(state.history[1].role, 'system');
  assert.ok(state.history[1].content.includes('[ERREUR]'));
  assert.ok(state.history[1].content.includes('Erreur réseau 401'));
  assert.equal(els.promptInput.value, 'erreur-reseau', 'Input conservé en cas derreur');
});

test('D03 - Réponse vide → message [ERREUR] dans historique', async () => {
  const state = makeState();
  const els = makeEls();
  await sendPrompt('erreur-vide-api', state, els);
  assert.equal(state.history.length, 2, 'un message utilisateur + une erreur système');
  assert.equal(state.history[1].role, 'system');
  assert.ok(state.history[1].content.includes('[ERREUR]'));
  assert.ok(state.history[1].content.includes('Aucune réponse reçue du serveur'));
});

test('D03 - File dattente : messages successifs', async () => {
  const state = makeState();
  const els = makeEls();
  let resolve1, resolve2;
  const p1 = new Promise((r) => (resolve1 = r));
  const p2 = new Promise((r) => (resolve2 = r));

  // Premier message lance une simulation d'attente asynchrone
  const pSend1 = sendPrompt('t1', state, els);

  // Tant que busy, les suivants sont mis en file
  state.messageQueue.push({ text: 't2', resolve: resolve1, reject: () => {} });
  state.messageQueue.push({ text: 't3', resolve: resolve2, reject: () => {} });

  assert.equal(state.messageQueue.length, 2, 'deux messages en file');
  assert.equal(state.busy, true, 'busy=true pendant traitement');

  // Simuler fin traitement t1 → traitement t2
  resolve1();
  await p1;

  assert.equal(state.messageQueue.length, 1, 'un message restant en file après t2 démarre');
  resolve2();
  await p2;

  // Fin des files
  await pSend1;
  assert.equal(state.messageQueue.length, 0, 'file vide à la fin');
});

test('D03 - État busy remis à false après traitement', async () => {
  const state = makeState();
  const els = makeEls();
  await sendPrompt('ok', state, els);
  assert.equal(state.busy, false, 'busy remis à false après fin');
  assert.equal(els.sendBtn.disabled, false, 'sendBtn réactivé après fin');
});
