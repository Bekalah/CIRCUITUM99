// Planetary light effect -- applies overlay blend mode to vitrail overlays
export function applyPlanetaryLight(root = document) {
  const nodes = root.querySelectorAll('.overlay-vitrail');
  nodes.forEach(el => {
    el.style.mixBlendMode = 'overlay';
  });
}
