// Browser isolation, not authentication against other processes on this machine.
export function installBrowserAccess(app, server, wss) {
  const url = new URL(process.env.EXPRESS_SERVER_URL || 'http://127.0.0.1:3210');
  if (url.protocol !== 'http:' || url.hostname !== '127.0.0.1' || !url.port ||
      url.username || url.password || url.pathname !== '/' || url.search || url.hash ||
      (process.env.HOST && process.env.HOST !== '127.0.0.1') ||
      (process.env.PORT && process.env.PORT !== url.port)) {
    throw new Error('Excalidraw requires a matching http://127.0.0.1:<port> canvas URL and bind address');
  }
  // Also constrain direct launches of the patched canvas, not just auto-starts.
  process.env.HOST = '127.0.0.1';
  process.env.PORT = url.port;

  function allowed(req, websocket = false) {
    if (req.headers.host !== url.host) return false;
    const origin = req.headers.origin;
    if (origin !== undefined && origin !== url.origin) return false;
    if (websocket && origin !== url.origin) return false;
    const site = req.headers['sec-fetch-site'];
    if (site && site !== 'same-origin' && site !== 'none') {
      // Opening a link in a top-level tab is safe; embedding or fetching data isn't.
      return !websocket && req.method === 'GET' && req.url === '/' &&
        req.headers['sec-fetch-mode'] === 'navigate' &&
        req.headers['sec-fetch-dest'] === 'document';
    }
    return true; // No Origin/Fetch Metadata is normal for local MCP HTTP calls.
  }

  app.use((req, res, next) => {
    res.setHeader('Content-Security-Policy', "frame-ancestors 'none'");
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    if (!allowed(req)) return res.status(403).end('Forbidden');
    next();
  });
  server.on('upgrade', (req, socket, head) => {
    if (!allowed(req, true)) {
      socket.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Length: 0\r\n\r\n');
      return;
    }
    wss.handleUpgrade(req, socket, head, ws => wss.emit('connection', ws, req));
  });
}
