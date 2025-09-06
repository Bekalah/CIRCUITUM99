// UI helpers for ritual interactions

// Initialize a ritual listener on a given element
export function initRitual(element, handler) {
  const el = typeof element === 'string' ? document.querySelector(element) : element;
  if (!el) return;
  el.addEventListener('click', (ev) => {
    const name = ev.target.getAttribute('data-ritual');
    if (name && typeof handler === 'function') {
      handler(name, ev);
    }
  });
}

// Dispatch a ritual start event
export function startRitual(name, detail = {}) {
  const evt = new CustomEvent('ritual:start', { detail: { name, ...detail } });
  document.dispatchEvent(evt);
}
