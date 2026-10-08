// Real HTTP/WS boundary regression. EXCALIDRAW_TEST_SERVER can select the
// pristine published server to demonstrate that the protection fails pre-fix.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import net from 'node:net';
import { once } from 'node:events';
import { spawn } from 'node:child_process';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';

test('canvas accepts local editor/MCP but rejects foreign HTTP and WebSocket access', { timeout: 30000 }, async t => {
  const reservation = net.createServer();
  reservation.listen(0, '127.0.0.1');
  await once(reservation, 'listening');
  const port = reservation.address().port;
  await new Promise(resolve => reservation.close(resolve));
  const url = `http://127.0.0.1:${port}`;
  const cache = path.resolve('.cache/excalidraw');
  await mkdir(path.join(cache, 'check-home'), { recursive: true });
  const entry = process.env.EXCALIDRAW_TEST_SERVER ||
    path.join(cache, 'runtime/node_modules/mcp-excalidraw-server/dist/server.js');
  const child = spawn(process.execPath, [entry], {
    env: { ...process.env, HOME: path.join(cache, 'check-home'),
      LOG_FILE_PATH: path.join(cache, 'security-check.log'),
      EXPRESS_SERVER_URL: url, HOST: '127.0.0.1', PORT: String(port) },
    stdio: ['ignore', 'ignore', 'inherit'],
  });
  const exited = once(child, 'exit');
  t.after(async () => { child.kill('SIGTERM'); await exited; });

  function request(route, { method = 'GET', headers = {}, body } = {}) {
    return new Promise((resolve, reject) => {
      const req = http.request(url + route, { method, headers }, res => {
        let text = '';
        res.on('data', chunk => { text += chunk; });
        res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, text }));
      });
      req.on('error', reject);
      req.setTimeout(3000, () => req.destroy(new Error('HTTP timeout')));
      req.end(body);
    });
  }
  let ready = false;
  for (let attempt = 0; attempt < 60; attempt++) {
    if (child.exitCode !== null) throw new Error(`Canvas exited: ${child.exitCode}`);
    try { ready = (await request('/health')).status === 200; } catch {}
    if (ready) break;
    await delay(100);
  }
  assert.ok(ready, 'real canvas starts');
  const element = { id: 'probe', type: 'rectangle', x: 20, y: 20, width: 160, height: 80, text: 'Private diagram' };
  assert.equal((await request('/api/elements', { method: 'POST',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(element) })).status, 200);
  const before = JSON.parse((await request('/api/elements')).text);
  assert.equal(before.elements[0].id, 'probe');

  // Each request is otherwise valid: denial must be at the access boundary,
  // not an unrelated parser, route, or schema error. Verify no writes occurred.
  await t.test('HTTP rejects foreign reads and writes without changing the scene', async () => {
  for (const headers of [
    { Origin: 'https://unrelated.invalid' },
    { Origin: 'null' },
    { Origin: `${url}.unrelated.invalid` },
    { Host: `rebound.invalid:${port}` },
    { 'Sec-Fetch-Site': 'cross-site' },
    { 'Sec-Fetch-Site': 'same-site' },
  ]) {
    for (const method of ['GET', 'POST']) {
      const result = await request('/api/elements', { method,
        headers: { 'Content-Type': 'application/json', ...headers },
        body: method === 'POST' ? JSON.stringify({ ...element, id: 'intruder' }) : undefined });
      assert.equal(result.status, 403, `${method} ${JSON.stringify(headers)}`);
    }
  }
  assert.equal((await request('/api/elements', { method: 'OPTIONS', headers: {
    Origin: 'https://unrelated.invalid', 'Access-Control-Request-Method': 'POST',
  } })).status, 403);
  assert.deepEqual(JSON.parse((await request('/api/elements')).text), before);
  const local = await request('/api/elements', { headers: { Origin: url, 'Sec-Fetch-Site': 'same-origin' } });
  assert.equal(local.status, 200);
  assert.notEqual(local.headers['access-control-allow-origin'], '*');
  const page = await request('/', { headers: { 'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Dest': 'document' } });
  assert.equal(page.status, 200, 'user can follow a link to the editor');
  assert.equal(page.headers['x-frame-options'], 'DENY');
  assert.equal((await request('/', { headers: { 'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Dest': 'iframe' } })).status, 403);
  });

  function upgrade(headers) {
    return new Promise((resolve, reject) => {
      const req = http.request(url, { headers: {
        Connection: 'Upgrade', Upgrade: 'websocket', 'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Key': 'dGhlIHNhbXBsZSBub25jZQ==', ...headers,
      } });
      req.on('upgrade', (res, socket) => { socket.destroy(); resolve(res.statusCode); });
      req.on('response', res => { res.resume(); resolve(res.statusCode); });
      req.on('error', reject);
      req.setTimeout(3000, () => req.destroy(new Error('WebSocket timeout')));
      req.end();
    });
  }
  await t.test('WebSocket rejects foreign handshakes before exposing the scene', async () => {
  for (const headers of [
    {}, { Origin: 'null' }, { Origin: 'https://unrelated.invalid' },
    { Origin: url, Host: `rebound.invalid:${port}` },
    { Origin: url, 'Sec-Fetch-Site': 'cross-site' },
  ]) assert.equal(await upgrade(headers), 403, `WS ${JSON.stringify(headers)}`);
  assert.equal(await upgrade({ Origin: url }), 101, 'local editor WebSocket accepted');
  });
});
