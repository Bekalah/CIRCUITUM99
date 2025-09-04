// Simple fractal rendering engine
export function drawFractal(canvas) {
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let zx = 0, zy = 0;
      const cx = (x - width / 2) * 4 / width;
      const cy = (y - height / 2) * 4 / width;
      let iter = 0;
      while (zx*zx + zy*zy < 4 && iter < 64) {
        const xt = zx*zx - zy*zy + cx;
        zy = 2*zx*zy + cy;
        zx = xt;
        iter++;
      }
      const c = iter === 64 ? 0 : 255 - iter * 4;
      ctx.fillStyle = `rgb(${c}, ${c}, ${c})`;
      ctx.fillRect(x, y, 1, 1);
    }
  }
}
