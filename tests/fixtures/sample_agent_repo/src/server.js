const express = require("express");
const fs = require("node:fs");
const { resolvePort } = require("./runtime");

function buildApp() {
  const app = express();
  app.get("/health", (_req, res) => {
    res.json({ ok: true });
  });
  return app;
}

function startServer(port = resolvePort()) {
  const app = buildApp();
  fs.mkdirSync("logs", { recursive: true });
  return app.listen(port, () => {
    console.log(`listening on ${port}`);
  });
}

if (require.main === module) {
  startServer();
}

module.exports = { buildApp, startServer };
