// Codex independent replacement after review of native Qwen draft.
// Actual AuthService runs; transport, converters and auth-state boundary are mocked.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = process.env.JM01_PROJECT_ROOT || path.resolve(__dirname, '../../actual');
const ts = require(path.join(root, 'node_modules/typescript'));
const dir = path.join(root, 'libs/shared/data-access/api/src/lib/auth');
function compile(name, dependencies) {
  const source = fs.readFileSync(path.join(dir, name), 'utf8');
  const result = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 },
    fileName: name,
  });
  const exports = {};
  vm.runInNewContext(result.outputText, {
    module: { exports }, exports,
    require: key => {
      assert.ok(Object.hasOwn(dependencies, key), `Unexpected import ${key}`);
      return dependencies[key];
    },
  }, { filename: name, timeout: 3000 });
  return exports;
}
function fixture({ response = { token: 'dummy-local-token' }, postErrors = [] } = {}) {
  const requests = [], signedIn = [], conversions = [];
  const api = {
    async post(...args) {
      requests.push({ method: 'POST', args });
      const error = postErrors.shift();
      if (error) throw error;
      return response;
    },
    async get(...args) {
      requests.push({ method: 'GET', args });
      return response;
    },
  };
  class SignInResponse {}
  class UpdateProfileRequest {}
  const convertedRequest = { serialized: true };
  const config = compile('config.ts', {});
  const { authService } = compile('service.ts', {
    './config': config,
    './models': { SignInResponse, UpdateProfileRequest },
    'class-transformer': {
      plainToInstance(type, value) { conversions.push({ method: 'deserialize', type, value }); return value; },
      instanceToPlain(value) { conversions.push({ method: 'serialize', value }); return convertedRequest; },
    },
    '@open-webui-react-native/shared/data-access/api-client': { getApiService: () => api },
    '@open-webui-react-native/shared/data-access/auth': { authState$: { signIn: token => signedIn.push(token) } },
  });
  return { authService, requests, signedIn, conversions, response, convertedRequest, SignInResponse, UpdateProfileRequest };
}
const credentials = { email: 'qa@example.invalid', password: 'dummy-local-only' };
test('successful token response signs state in once and uses exact signin route/body', async () => {
  const f = fixture();
  assert.equal(await f.authService.signInWithEmailPassword(credentials), f.response);
  assert.deepEqual(f.signedIn, ['dummy-local-token']);
  assert.equal(f.requests[0].method, 'POST');
  assert.equal(f.requests[0].args[0], 'v1/auths/signin');
  assert.equal(f.requests[0].args[1], credentials);
  assert.equal(f.conversions[0].type, f.SignInResponse);
});
for (const status of [401, 403]) {
  test(`signin ${status} propagates same error and does not change auth state`, async () => {
    const error = Object.assign(new Error('simulated rejection'), { response: { status } });
    const f = fixture({ postErrors: [error] });
    await assert.rejects(f.authService.signInWithEmailPassword(credentials), value => value === error);
    assert.equal(f.requests.length, 1);
    assert.deepEqual(f.signedIn, []);
    assert.deepEqual(f.conversions, []);
  });
}
for (const response of [
  { challengeToken: 'dummy-challenge', nextStep: 'mfa' },
  { nextStep: 'pending' },
]) {
  test(`token-free ${response.nextStep} response does not sign in`, async () => {
    const f = fixture({ response });
    assert.equal(await f.authService.signInWithEmailPassword(credentials), response);
    assert.deepEqual(f.signedIn, []);
  });
}
test('logout POST sends explicitly supplied bearer and skipToast', async () => {
  const f = fixture();
  await f.authService.signOut('dummy-logout-token');
  assert.equal(f.requests.length, 1);
  const { method, args } = f.requests[0];
  assert.equal(method, 'POST');
  assert.equal(args[0], 'v1/auths/signout');
  assert.equal(args[1], undefined);
  assert.equal(args[2].headers.Authorization, 'Bearer dummy-logout-token');
  assert.equal(args[2].params.skipToast, true);
});
test('logout405 falls back once to GET with same bearer', async () => {
  const f = fixture({ postErrors: [{ response: { status: 405 } }] });
  await f.authService.signOut('dummy-fallback-token');
  assert.deepEqual(f.requests.map(r => r.method), ['POST', 'GET']);
  assert.equal(f.requests[1].args[0], 'v1/auths/signout');
  assert.equal(f.requests[0].args[2].headers.Authorization, 'Bearer dummy-fallback-token');
  assert.equal(f.requests[1].args[2].headers.Authorization, 'Bearer dummy-fallback-token');
  assert.equal(f.requests[1].args[1].skipToast, true);
});
for (const status of [403, 500]) {
  test(`logout${status} does not invoke GET fallback`, async () => {
    const error = { response: { status } };
    const f = fixture({ postErrors: [error] });
    await assert.rejects(f.authService.signOut('dummy-token'), value => value === error);
    assert.deepEqual(f.requests.map(r => r.method), ['POST']);
  });
}
test('profile GET preserves route and supplied options object', async () => {
  const f = fixture();
  const options = { headers: { 'X-QA': 'local' }, timeout: 1234 };
  assert.equal(await f.authService.getProfile(options), f.response);
  assert.equal(f.requests[0].method, 'GET');
  assert.equal(f.requests[0].args[0], 'v1/auths/');
  assert.equal(f.requests[0].args[1], undefined);
  assert.equal(f.requests[0].args[2], options);
  assert.equal(f.conversions[0].type, f.SignInResponse);
});
test('profile update serializes request and deserializes response at actual boundaries', async () => {
  const f = fixture();
  const request = { name: 'Local QA' };
  assert.equal(await f.authService.updateProfile(request), f.response);
  assert.equal(f.requests[0].args[0], 'v1/auths/update/profile');
  assert.equal(f.requests[0].args[1], f.convertedRequest);
  assert.equal(f.conversions[0].method, 'serialize');
  assert.equal(f.conversions[0].value, request);
  assert.equal(f.conversions[1].type, f.UpdateProfileRequest);
});
test('password update posts serialized payload to correct route', async () => {
  const f = fixture();
  const request = { oldPassword: 'dummy-old', newPassword: 'dummy-new' };
  await f.authService.updatePassword(request);
  assert.equal(f.requests.length, 1);
  assert.equal(f.requests[0].method, 'POST');
  assert.equal(f.requests[0].args[0], 'v1/auths/update/password');
  assert.equal(f.requests[0].args[1], f.convertedRequest);
  assert.equal(f.conversions[0].value, request);
});
