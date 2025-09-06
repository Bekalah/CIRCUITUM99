// Room plaque component for displaying contextual info
export class RoomPlaque {
  constructor(element) {
    this.el = typeof element === 'string' ? document.querySelector(element) : element;
  }
  show(text) {
    if (!this.el) return;
    this.el.textContent = text;
    this.el.style.display = 'block';
  }
  hide() {
    if (!this.el) return;
    this.el.style.display = 'none';
  }
}

export function attachRoomPlaque(selector) {
  return new RoomPlaque(selector);
}
