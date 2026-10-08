// Install once into the consuming project, patch verified upstream bytes, run MCP.
// The npm download cache is never patched. Unknown upstream bytes fail closed.
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile, rename } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = process.cwd();
const cache = path.join(root, '.cache/excalidraw');
const runtime = path.join(cache, 'runtime');
const pkg = path.join(runtime, 'node_modules/mcp-excalidraw-server');
const env = {
  ...process.env,
  HOME: path.join(cache, 'home'),
  LOG_FILE_PATH: path.join(cache, 'server.log'),
  EXPRESS_SERVER_URL: process.env.EXPRESS_SERVER_URL || 'http://127.0.0.1:3210',
};
const url = new URL(env.EXPRESS_SERVER_URL);
if (url.protocol !== 'http:' || url.hostname !== '127.0.0.1' || !url.port ||
    url.username || url.password || url.pathname !== '/' || url.search || url.hash) {
  throw new Error('Use http://127.0.0.1:<port> for EXPRESS_SERVER_URL');
}
await mkdir(env.HOME, { recursive: true });

function run(command, args, stdio) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd: root, env, stdio });
    child.once('error', reject);
    child.once('exit', (code, signal) => code === 0 ? resolve() :
      reject(new Error(`${command} exited with ${code ?? signal}`)));
  });
}
let version;
try { version = JSON.parse(await readFile(path.join(pkg, 'package.json'), 'utf8')).version; }
catch (error) { if (error.code !== 'ENOENT') throw error; }
if (version !== '2.1.2') {
  await run('npm', ['install', '--prefix', runtime, '--cache', path.join(cache, 'npm'),
    '--no-audit', '--no-fund', '--ignore-scripts', '--save-exact',
    'mcp-excalidraw-server@2.1.2'], ['ignore', 2, 2]);
}

const hash = text => createHash('sha256').update(text).digest('hex');
async function atomicWrite(file, content) {
  const tmp = `${file}.${process.pid}.tmp`;
  await writeFile(tmp, content);
  await rename(tmp, file);
}
async function patch(relative, expectedHash, transform) {
  const file = path.join(pkg, relative);
  const current = await readFile(file, 'utf8');
  const backup = `${file}.upstream`;
  let original;
  try { original = await readFile(backup, 'utf8'); }
  catch (error) {
    if (error.code !== 'ENOENT') throw error;
    original = current;
  }
  if (hash(original) !== expectedHash) throw new Error(`Unrecognized upstream file: ${relative}`);
  const patched = transform(original);
  if (current !== original && current !== patched) throw new Error(`Unexpected local changes: ${relative}`);
  await atomicWrite(backup, original);
  await atomicWrite(file, patched);
}
const scripts = path.dirname(fileURLToPath(import.meta.url));
await atomicWrite(path.join(pkg, 'dist/browser-access.mjs'),
  await readFile(path.join(scripts, 'browser-access.mjs'), 'utf8'));
await patch('dist/server.js', 'c3e3198b6b1b9add84ce05fea4a47cf8c6904020c3d22b6cbb8bddd375de6cb3', source => source
  .replace("import cors from 'cors';", "import { installBrowserAccess } from './browser-access.mjs';")
  .replace('const wss = new WebSocketServer({ server });',
    'const wss = new WebSocketServer({ noServer: true });\ninstallBrowserAccess(app, server, wss);')
  .replace('app.use(cors());', '')
  .replace("service: 'mcp-excalidraw-canvas'", "service: 'mcp-excalidraw-canvas-origin-guard-v1'"));
await patch('dist/core/canvas-client.js', 'cc8494406fc74b9287e033e557c1e8a8bf240ec3341560a63848488007e9d43b', source => source
  .replace("'mcp-excalidraw-canvas'", "'mcp-excalidraw-canvas-origin-guard-v1'"));

// Forward lifecycle signals to the stdio process. The canvas intentionally stays
// running for the user's browser, as it does in the upstream package.
const child = spawn(process.execPath, [path.join(pkg, 'dist/bin.js'), ...process.argv.slice(2)],
  { cwd: root, env, stdio: 'inherit' });
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => child.kill(signal));
child.once('error', error => { console.error(error); process.exitCode = 1; });
child.once('exit', (code, signal) => { process.exitCode = code ?? (signal ? 1 : 0); });
