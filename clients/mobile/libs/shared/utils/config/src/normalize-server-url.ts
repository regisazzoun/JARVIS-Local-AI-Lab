// JARVIS correction: validate before any lossy URL reconstruction.
const schemePattern = /^([a-z][a-z\d+.-]*:\/\/|https?:)/i;
export const normalizeServerUrl = (url?: string): string => {
  const trimmed = (url ?? '').trim();
  if (!trimmed) return '';
  const withScheme = schemePattern.test(trimmed) ? trimmed : `https://${trimmed}`;
  return withScheme.replace(/\/+$/, '').replace(/\/api$/i, '');
};
export const isValidServerUrl = (url?: string): boolean => {
  const normalized = normalizeServerUrl(url);
  if (!normalized) return false;
  try {
    const parsed = new URL(normalized);
    return ['http:', 'https:'].includes(parsed.protocol) && !!parsed.hostname &&
      !parsed.username && !parsed.password && !parsed.search && !parsed.hash;
  } catch { return false; }
};
