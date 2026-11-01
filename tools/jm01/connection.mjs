// JM-01 connection correction authored by Codex after invalid native candidates.
export function normalizeBaseUrl(input) {
  let url;
  try { url = new URL(input); } catch { throw new Error('Invalid base URL'); }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
    throw new Error('Invalid base URL');
  }
  return url.origin + url.pathname.replace(/\/+$/, '');
}
async function getJson(url, token, timeoutMs) {
  const abort = new AbortController();
  const timer = setTimeout(() => abort.abort(), timeoutMs);
  try {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    let response;
    try { response = await fetch(url, { headers, signal: abort.signal, redirect: 'error' }); }
    catch { throw new Error(abort.signal.aborted ? 'Request timeout' : 'Network request failed'); }
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    try { return await response.json(); } catch { throw new Error('Invalid JSON response'); }
  } finally { clearTimeout(timer); }
}
export async function connect(baseUrl, { token, timeoutMs = 1000 } = {}) {
  const base = normalizeBaseUrl(baseUrl);
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) throw new Error('Invalid timeout');
  if (token !== undefined && typeof token !== 'string') throw new Error('Invalid token');
  const config = await getJson(`${base}/api/config`, token, timeoutMs);
  const models = await getJson(`${base}/api/models`, token, timeoutMs);
  return { config, models };
}
