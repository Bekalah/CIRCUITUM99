/*
  bridge-loader.mjs
  Minimal helper to load c99-bridge.json and expose route getters.
  ND-safe: no external requests, small pure functions.
*/

let bridgeCache = null;

// Load the bridge file once. Returns parsed object or empty fallback.
export async function loadBridge(path = "./bridge/c99-bridge.json") {
  if (bridgeCache) return bridgeCache;
  try {
    const res = await fetch(path, { cache: "no-store" });
    if (!res.ok) throw new Error(String(res.status));
    const txt = await res.text();
    // Tolerate trailing commas by stripping them before parsing.
    const clean = txt.replace(/,\s*(\}|\])/g, "$1");
    bridgeCache = JSON.parse(clean);
  } catch (err) {
    // Safe fallback: empty structure
    bridgeCache = { routes:{}, tokens:{} };
  }
  return bridgeCache;
}

// Retrieve a route path for a repository key pair.
export function getRoute(repo, key) {
  return bridgeCache?.routes?.[repo]?.[key] || null;
}

// Retrieve a token entry such as css or json path.
export function getToken(key) {
  return bridgeCache?.tokens?.[key] || null;
}

