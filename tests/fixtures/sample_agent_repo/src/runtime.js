function resolvePort(defaultPort = 3000) {
  return process.env.PORT || defaultPort;
}

module.exports = { resolvePort };
