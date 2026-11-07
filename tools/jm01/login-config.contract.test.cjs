// Native Qwen draft reviewed and corrected by Codex; actual source behavior, no network.
const vm = require('vm');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { test } = require('node:test');

// Paths
const projectRoot = process.env.JM01_PROJECT_ROOT || path.resolve(__dirname, '../../actual');
const libsRoot = path.join(projectRoot, 'libs/shared');

const normalizeServerUrlPath = path.join(libsRoot, 'utils/config/src/normalize-server-url.ts');
const getApiUrlPath = path.join(libsRoot, 'utils/config/src/get-api-url.ts');
const getConfigPathPath = path.join(libsRoot, 'data-access/api/src/lib/app-configuration/utils/get-config-path.ts');
const authConfigPath = path.join(libsRoot, 'data-access/api/src/lib/auth/config.ts');

// Read sources
const srcNormalizeServerUrl = fs.readFileSync(normalizeServerUrlPath, 'utf-8');
const srcGetApiUrl = fs.readFileSync(getApiUrlPath, 'utf-8');
const srcGetConfigPath = fs.readFileSync(getConfigPathPath, 'utf-8');
const srcAuthConfig = fs.readFileSync(authConfigPath, 'utf-8');

// Common ts compile options
const ts = require(path.join(projectRoot, 'node_modules/typescript'));
const compileOptions = { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS };

// Helper to compile and evaluate a module in isolated vm
function compileModule(src, dependencies = {}) {
  const compiled = ts.transpileModule(src, {
    compilerOptions: compileOptions,
  });

  const requireMap = { path, assert, ...dependencies };

  const exported = {};
  const context = vm.createContext({
    require: (mod) => {
      if (!Object.hasOwn(requireMap, mod)) throw new Error('Unexpected import: ' + mod);
      return requireMap[mod];
    },
    module: { exports: exported },
    exports: exported,
    URL,
    __filename: '',
    __dirname: '',
    Buffer: Buffer,
    console: console,
  });

  vm.runInContext(compiled.outputText, context, { timeout: 3000 });
  return context.module.exports;
}

// Dummy mocked dependencies
const appEnvMock = {
  select: function (choices) {
    return choices.development; // always return development for testing
  },
};

let storedUrl = '';
const appStorageServiceMock = {
  apiUrl: {
    get: () => storedUrl,
    set: () => {},
  },
};

const actualModuleExports = compileModule(srcNormalizeServerUrl, { path, assert });

// Export actual functions for use in get-api-url tests
const normalizeServerUrl = actualModuleExports.normalizeServerUrl;
const isValidServerUrl = actualModuleExports.isValidServerUrl;

const getApiModule = compileModule(srcGetApiUrl, {
  path,
  assert,
  './normalize-server-url': actualModuleExports,
  '@open-webui-react-native/shared/data-access/storage': { appStorageService: appStorageServiceMock },
  '@open-webui-react-native/shared/utils/app-env': { appEnv: appEnvMock },
});

// Expose functions under test
const ronasApiUrl = getApiModule.ronasApiUrl;
const testApiUrl = getApiModule.testApiUrl;
const resolveApiUrl = getApiModule.resolveApiUrl;
const isTestApiUrl = getApiModule.isTestApiUrl;
const getDisplayApiUrl = getApiModule.getDisplayApiUrl;
const getApiUrl = getApiModule.getApiUrl;
const getHost = getApiModule.getHost;

const getConfigPathModule = compileModule(srcGetConfigPath, { path, assert });
const getConfigPath = getConfigPathModule.getConfigPath;

const authConfigModule = compileModule(srcAuthConfig, { path, assert });
const authApiConfig = authConfigModule.authApiConfig;

// Helper for test grouping
function describe(name, fn) {
  fn();
}

describe('JARVIS 08 LOGIN CONFIG CONTRACT TEST SUITE', () => {
  describe('normalize-server-url.ts', () => {
    test('01: Empty/undefined input returns empty string', () => {
      assert.strictEqual(normalizeServerUrl(undefined), '');
      assert.strictEqual(normalizeServerUrl(''), '');
      assert.strictEqual(normalizeServerUrl('   '), '');
    });

    test('02: HTTP/HTTPS URLs are preserved with scheme', () => {
      assert.strictEqual(normalizeServerUrl('http://example.com'), 'http://example.com');
      assert.strictEqual(normalizeServerUrl('https://example.com'), 'https://example.com');
    });

    test('03: Schemeless input auto-prefixes https://', () => {
      assert.strictEqual(normalizeServerUrl('example.com'), 'https://example.com');
      assert.strictEqual(normalizeServerUrl('192.168.1.1'), 'https://192.168.1.1');
      assert.strictEqual(normalizeServerUrl('localhost'), 'https://localhost');
    });

    test('04: Trailing slashes are stripped', () => {
      assert.strictEqual(normalizeServerUrl('http://example.com/'), 'http://example.com');
      assert.strictEqual(normalizeServerUrl('https://example.com///'), 'https://example.com');
    });

    test('05: /api suffix (case-insensitive) is stripped from normalized output', () => {
      assert.strictEqual(normalizeServerUrl('http://example.com/api'), 'http://example.com');
      assert.strictEqual(normalizeServerUrl('https://example.com/API/'), 'https://example.com');
      assert.strictEqual(normalizeServerUrl('http://example.com/Api'), 'http://example.com');
    });

    test('06: isValidServerUrl validates correct format and rejects unsafe URLs', () => {
      assert.strictEqual(isValidServerUrl('http://example.com'), true);
      assert.strictEqual(isValidServerUrl('https://example.com/api'), true);
      assert.strictEqual(isValidServerUrl('ftp://example.com'), false);
      assert.strictEqual(isValidServerUrl(''), false);
      assert.strictEqual(isValidServerUrl('http://user:pass@example.com'), false);
      assert.strictEqual(isValidServerUrl('http://example.com/path'), true);
    });

    test('07: getHost extracts and lowercases host portion', () => {
      assert.strictEqual(getHost('http://example.com/api'), 'example.com');
      assert.strictEqual(getHost('https://Example.COM/'), 'example.com');
      assert.strictEqual(getHost('https://my-server.local:8080'), 'my-server.local:8080');
    });
  });

  describe('get-api-url.ts', () => {
    test('08: ronasApiUrl and testApiUrl are fixed production URLs', () => {
      assert.strictEqual(ronasApiUrl, 'https://ai.ronas.online');
      assert.strictEqual(testApiUrl, 'https://ai.test-api.online');
    });

    test('09: resolveApiUrl aliases testApiUrl to ronasApiUrl', () => {
      assert.strictEqual(
        resolveApiUrl(testApiUrl),
        ronasApiUrl
      );
      assert.strictEqual(
        resolveApiUrl('https://ai.test-api.online/api'),
        ronasApiUrl
      );
      assert.strictEqual(
        resolveApiUrl('http://ai.ronas.online/'),
        'http://ai.ronas.online'
      );
    });

    test('10: getDisplayApiUrl falls back to ronasApiUrl when no stored URL', () => {
      // storage apiUrl is mocked to return '' (empty)
      assert.strictEqual(getDisplayApiUrl(), ronasApiUrl);
    });

    test('11: getApiUrl returns resolved display API URL', () => {
      // Since fallback storage returns empty, display API is ronasApiUrl, no aliasing
      assert.strictEqual(getApiUrl(), ronasApiUrl);
    });

    test('12: isTestApiUrl detects test URL in input or stored state', () => {
      assert.strictEqual(isTestApiUrl(testApiUrl), true);
      assert.strictEqual(isTestApiUrl(ronasApiUrl), false);
      assert.strictEqual(isTestApiUrl(undefined), false);
    });
  });

  describe('get-config-path.ts', () => {
    test('13: getConfigPath appends /api/ after cleaning trailing slash', () => {
      assert.strictEqual(getConfigPath('http://example.com'), 'http://example.com/api/');
      assert.strictEqual(getConfigPath('http://example.com/'), 'http://example.com/api/');
    });

    test('14: getConfigPath returns empty string for empty input', () => {
      assert.strictEqual(getConfigPath(''), '');
    });
  });

  describe('auth/config.ts', () => {
    test('15: authApiConfig contains expected route and query keys', () => {
      assert.strictEqual(authApiConfig.route, 'v1/auths');
      assert.deepStrictEqual(Array.from(authApiConfig.getProfileQueryKey), ['profile']);
      assert.deepStrictEqual(Array.from(authApiConfig.signOutQueryKey), ['sign-out']);
    });
  });
});

// Codex independent additions: exercise the actual configured prefix and storage paths.
test('16: self-hosted prefix survives resolver and configuration path join', () => {
  for (const base of ['http://127.0.0.1:18935/jarvis', 'https://example.invalid/team/webui']) {
    const resolved = resolveApiUrl(base + '/api/');
    assert.strictEqual(resolved, base);
    assert.strictEqual(getConfigPath(resolved), base + '/api/');
  }
});
test('17: stored custom server overrides upstream fallback', () => {
  storedUrl = 'http://127.0.0.1:18935/jarvis/api/';
  try {
    assert.strictEqual(getDisplayApiUrl(), 'http://127.0.0.1:18935/jarvis');
    assert.strictEqual(getApiUrl(), 'http://127.0.0.1:18935/jarvis');
    assert.strictEqual(isTestApiUrl(), false);
  } finally { storedUrl = ''; }
});
test('18: stored demo alias is displayed but resolves to upstream', () => {
  storedUrl = testApiUrl;
  try {
    assert.strictEqual(getDisplayApiUrl(), testApiUrl);
    assert.strictEqual(getApiUrl(), ronasApiUrl);
    assert.strictEqual(isTestApiUrl(), true);
  } finally { storedUrl = ''; }
});
test('19: validation rejects query and fragment without stripping evidence', () => {
  for (const url of ['https://example.invalid/prefix?token=x', 'https://example.invalid/prefix#x'])
    assert.strictEqual(isValidServerUrl(url), false);
});
