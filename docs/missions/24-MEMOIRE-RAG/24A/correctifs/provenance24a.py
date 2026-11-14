"""Provenance for successful account-bound document reads; no content filtering."""
import datetime
import hashlib
import json
import re


def result_failed(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            return value.lstrip().lower().startswith(('error:', 'exception:', 'traceback', 'http error!'))
    if not isinstance(value, dict):
        return False
    if value.get('error') or value.get('mcp_is_error') is True or value.get('isError') is True:
        return True
    rc = value.get('returncode')
    if rc is not None and rc != 0:
        return True
    if value.get('success') is False or value.get('ok') is False:
        return True
    if str(value.get('status', '')).lower() in ('failed', 'error'):
        return True
    return any(result_failed(block) for block in value.get('content', []) if isinstance(block, dict))


def enrich_document(result, arguments, metadata):
    """A body hash identifies this read, never pretends to be a Drive revision ID."""
    if result_failed(result) or result.get('remote_access_verified') is not True:
        return result
    raw_id = arguments.get('documentId') or arguments.get('fileId') or ''
    match = re.search(r'/d/([\w-]+)', raw_id)
    ident = match.group(1) if match else raw_id
    if not re.fullmatch(r'[\w-]{10,256}', ident):
        return result
    text = '\n'.join(b.get('text', '') for b in result.get('content', []) if isinstance(b, dict))
    if not text.strip():
        return result
    meta = metadata.get(ident, {})
    native_doc = meta.get('mimeType') == 'application/vnd.google-apps.document'
    url = 'https://docs.google.com/document/d/' + ident + '/edit' if native_doc else 'https://drive.google.com/file/d/' + ident + '/view'
    result['provenance_24a'] = {
        'id': ident, 'title': meta.get('name') or ident, 'url': url,
        'modified_time': meta.get('modifiedTime'),
        'version_kind': 'sha256_of_read_text_not_drive_revision',
        'content_sha256': hashlib.sha256(text.encode()).hexdigest(),
        'read_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'excerpt': text[:600], 'successful_read': True,
    }
    return result


def citation_sources(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            return []
    if not isinstance(value, dict) or result_failed(value):
        return []
    p = value.get('provenance_24a') or {}
    if not (p.get('successful_read') is True and value.get('remote_access_verified') is True
            and value.get('returncode') == 0 and p.get('url')):
        return []
    return [{'source': {'id': p['url'], 'name': p['title'], 'type': 'url', 'url': p['url']},
             'document': [p['excerpt']],
             'metadata': [{'source': p['url'], 'url': p['url'], 'name': p['title'],
                           'date_modified': p['modified_time'], 'version': p['content_sha256'],
                           'version_kind': p['version_kind'], 'read_at_utc': p['read_at_utc']}]}]
