// Supplemental regression tests authored by Codex; independent suite is separate.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { connect, normalizeBaseUrl } from './connection.mjs';
test('normalization retains prefix and removes trailing slashes',()=>assert.equal(normalizeBaseUrl('https://example.invalid/prefix///'),'https://example.invalid/prefix'));
test('query and fragment base URLs are rejected',async()=>{for(const u of ['https://example.invalid/?token=x','https://example.invalid/#x'])await assert.rejects(()=>connect(u));});
test('invalid timeout rejected before network',async()=>{for(const timeoutMs of [0,-1,NaN,Infinity])await assert.rejects(()=>connect('https://example.invalid',{timeoutMs}));});
test('non-string bearer rejected before network',async()=>assert.rejects(()=>connect('https://example.invalid',{token:{}})));
