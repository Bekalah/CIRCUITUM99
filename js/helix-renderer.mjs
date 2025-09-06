/*
  helix-renderer.mjs
  ND-safe static renderer for layered sacred geometry.

  Layers:
    1) Vesica field (intersecting circles)
    2) Tree-of-Life scaffold (10 sephirot + 22 paths; simplified layout)
    3) Fibonacci curve (log spiral polyline; static)
    4) Double-helix lattice (two phase-shifted strands with rungs)

  ND-safe rationale:
    - All geometry is static. No motion or flashing.
    - Soft palette supplied by data/palette.json (or safe fallback).
    - Layer order is deliberate: foundational Vesica up to helix lattice.
*/

export function renderHelix(ctx, { width, height, palette, NUM }) {
  // Clear + fill background using palette.bg to avoid flicker
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = palette.bg;
  ctx.fillRect(0, 0, width, height);

  drawVesica(ctx, width, height, palette.layers[0], NUM);
  drawTree(ctx, width, height, palette.layers[1], palette.ink, NUM);
  drawFibonacci(ctx, width, height, palette.layers[2], NUM);
  drawHelixLattice(ctx, width, height, palette.layers[3], palette.layers[4], NUM);
}

function drawVesica(ctx, w, h, color, NUM) {
  // Two intersecting circles echoing the Vesica Piscis; repeated vertically.
  const r = Math.min(w, h) / NUM.THREE; // uses constant 3
  const cx = w / 2;
  const cy = h / 2;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  for (let i = -1; i <= 1; i++) {
    const y = cy + (i * r) / NUM.SEVEN; // vertical repetition keyed to 7
    ctx.beginPath();
    ctx.arc(cx - r / 2, y, r, 0, Math.PI * 2);
    ctx.arc(cx + r / 2, y, r, 0, Math.PI * 2);
    ctx.stroke();
  }
}

function drawTree(ctx, w, h, color, nodeColor, NUM) {
  // Simplified Tree of Life layout; positions are fractional.
  const nodes = [
    { x: 0.5, y: 0.07 }, // Keter
    { x: 0.75, y: 0.18 }, // Chokmah
    { x: 0.25, y: 0.18 }, // Binah
    { x: 0.75, y: 0.35 }, // Chesed
    { x: 0.25, y: 0.35 }, // Geburah
    { x: 0.5, y: 0.5 },  // Tiphereth
    { x: 0.75, y: 0.65 }, // Netzach
    { x: 0.25, y: 0.65 }, // Hod
    { x: 0.5, y: 0.78 }, // Yesod
    { x: 0.5, y: 0.92 }  // Malkuth
  ];

  const edges = [
    [0,1],[0,2], [1,2], [1,3], [1,6],
    [2,4],[2,7], [3,4], [3,5], [4,5],
    [3,6],[4,7], [5,6], [5,7], [6,7],
    [6,8],[7,8], [5,8], [8,9],[5,9],
    [3,7],[4,6]
  ]; // 22 paths

  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  edges.forEach(([a, b]) => {
    ctx.beginPath();
    ctx.moveTo(nodes[a].x * w, nodes[a].y * h);
    ctx.lineTo(nodes[b].x * w, nodes[b].y * h);
    ctx.stroke();
  });

  ctx.fillStyle = nodeColor;
  const r = NUM.NINE / 3; // node radius tuned by 9
  nodes.forEach((n) => {
    ctx.beginPath();
    ctx.arc(n.x * w, n.y * h, r, 0, Math.PI * 2);
    ctx.fill();
  });
}

function drawFibonacci(ctx, w, h, color, NUM) {
  // Log spiral inspired by Fibonacci; drawn as polyline.
  const center = { x: w / 2, y: h / 2 };
  const steps = NUM.THIRTYTHREE; // 33 segments
  const phi = (1 + Math.sqrt(5)) / 2; // golden ratio
  const scale = (Math.min(w, h) / NUM.ONEFORTYFOUR) * NUM.THIRTYTHREE; // involves 144
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i < steps; i++) {
    const angle = (i / NUM.ELEVEN) * Math.PI * 2; // turn by 1/11 of a turn per step
    const radius = scale * Math.pow(phi, i / NUM.TWENTYTWO);
    const x = center.x + radius * Math.cos(angle);
    const y = center.y + radius * Math.sin(angle);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

function drawHelixLattice(ctx, w, h, colorA, colorB, NUM) {
  // DNA-like double helix rendered statically with lattice rungs.
  const midY = h / 2;
  const amplitude = h / NUM.SEVEN; // height tuned by 7
  const segments = NUM.NINETYNINE; // detail level 99
  const freq = NUM.NINE; // wave count along width
  const step = w / segments;

  ctx.lineWidth = 1;
  // strand A
  ctx.strokeStyle = colorA;
  ctx.beginPath();
  for (let i = 0; i <= segments; i++) {
    const x = i * step;
    const y = midY + amplitude * Math.sin((i / segments) * freq * Math.PI * 2);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // strand B (phase-shifted by PI)
  ctx.strokeStyle = colorB;
  ctx.beginPath();
  for (let i = 0; i <= segments; i++) {
    const x = i * step;
    const y = midY + amplitude * Math.sin((i / segments) * freq * Math.PI * 2 + Math.PI);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // lattice rungs every 11 segments
  ctx.strokeStyle = colorB;
  for (let i = 0; i <= segments; i += NUM.ELEVEN) {
    const x = i * step;
    const y1 = midY + amplitude * Math.sin((i / segments) * freq * Math.PI * 2);
    const y2 = midY + amplitude * Math.sin((i / segments) * freq * Math.PI * 2 + Math.PI);
    ctx.beginPath();
    ctx.moveTo(x, y1);
    ctx.lineTo(x, y2);
    ctx.stroke();
  }
}
