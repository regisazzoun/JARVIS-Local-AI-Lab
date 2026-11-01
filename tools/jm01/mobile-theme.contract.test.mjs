import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { colors, spacings, fontFamily } from '../../clients/mobile/libs/mobile/shared/ui/styles/src/lib/variables.ts';
const css=readFileSync(new URL('../../clients/mobile/apps/mobile/global.css',import.meta.url),'utf8').toLowerCase();
const root=css.match(/(?<![.\w]):root\s*\{([^}]+)\}/)?.[1]||'';
const dark=css.match(/\.dark:root\s*\{([^}]+)\}/)?.[1]||'';
const prop=(s,key)=>s.match(new RegExp('--'+key+'\\s*:\\s*([^;]+);'))?.[1].trim();
test('NativeWind directives retained',()=>{for(const x of ['base','components','utilities'])assert.ok(css.includes('@tailwind '+x+';'));});
test('Launcher background and panels are applied in CSS',()=>{assert.equal(prop(root,'background-primary'),'#0b1018');assert.equal(prop(root,'background-secondary'),'#111925');});
test('Launcher accent and text applied in CSS',()=>{assert.equal(prop(root,'brand-primary'),'#67e2c5');assert.equal(prop(root,'text-primary'),'#e6edf7');assert.equal(prop(root,'text-secondary'),'#8c9ab1');});
test('dark theme also uses Launcher palette',()=>{assert.equal(prop(dark,'background-primary'),'#0b1018');assert.equal(prop(dark,'text-primary'),'#e6edf7');});
test('native styles agree with CSS',()=>{assert.equal(colors.brandPrimary.toLowerCase(),'#67e2c5');assert.equal(colors.backgroundPrimary.toLowerCase(),'#0b1018');assert.equal(colors.backgroundSecondary.toLowerCase(),'#111925');assert.equal(colors.textPrimary.toLowerCase(),'#e6edf7');});
test('semantic state colors and spacing exports retained',()=>{for(const k of ['statusDanger','statusSuccess','statusWarning','brandPrimaryHover','brandPrimaryPressed','darkTextPrimary','darkBackgroundPrimary'])assert.ok(colors[k]);assert.equal(spacings.contentOffset,20);assert.equal(spacings.screenHorizontalOffset,40);assert.ok(fontFamily.regular);});
test('Launcher primary text has accessible contrast',()=>{const lum=h=>{let a=h.slice(1).match(/../g).map(x=>parseInt(x,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return a[0]*.2126+a[1]*.7152+a[2]*.0722;};assert.ok((lum(colors.textPrimary)+.05)/(lum(colors.backgroundPrimary)+.05)>=7);});

const baseline=await import('./fixtures/upstream-style-variables.ts');
test('all native style keys retained',()=>{for(const k of Object.keys(baseline.colors))assert.ok(Object.hasOwn(colors,k),k);});
test('all original CSS tokens retained',()=>{const original=readFileSync(new URL('./fixtures/upstream-global.css',import.meta.url),'utf8');for(const name of new Set(original.match(/--[a-z-]+(?=\s*:)/g)))assert.ok(css.includes(name+':'),name);});
