import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cookieService } from '../../clients/mobile/libs/shared/data-access/cookie/src/service.web.ts';
import { compressImage } from '../../clients/mobile/libs/mobile/shared/utils/compressor/src/image-compressor.web.ts';
test('web cookie adapter imports without native bridge and does not expose token',async()=>{await cookieService.setToken('fixture-not-a-secret');assert.equal(Object.keys(cookieService).length,0);});
test('web cookie adapter clears no unrelated browser state',async()=>assert.equal(await cookieService.clearAll(),undefined));
test('web image adapter preserves file URI',async()=>assert.equal(await compressImage('file:///fixture/image.jpg'),'file:///fixture/image.jpg'));
test('web image adapter preserves data URI and does not claim native compression',async()=>assert.equal(await compressImage('data:image/png;base64,AA=='),'data:image/png;base64,AA=='));
