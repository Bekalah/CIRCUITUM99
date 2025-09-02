# CODEBOT_C99_BOOK_ENABLE.md

# PURPOSE: Enable Circuitum99 (the book) to consume the same perm-style tokens, CSS, filters, and bridge manifest used by Stone Grimoire and Cosmogenesis.

# EXPECTED PATHS (create if missing)
cosmogenesis_learning_engine/
  public/
    c99/
      css/               ← mirror of SG perm-style.css
      tokens/            ← mirror of SG perm-style.json
      filters/           ← shared SVG filter defs for obsidian/raku
  pages/                 ← if Next.js
  engines/               ← your interactive book engine runtime
  docs/
bridge/                  ← shared c99-bridge.json at super-repo root
stone_grimoire/          ← source of truth for tokens/css/filters

# 0) MIRROR FROM STONE GRIMOIRE (already handled by update-art.js)
# After you run:
#   node stone_grimoire/core/build/update-art.js
# The script mirrors:
#   stone_grimoire/assets/tokens/perm-style.json  → cosmogenesis_learning_engine/public/c99/tokens/perm-style.json
#   stone_grimoire/assets/css/perm-style.css      → cosmogenesis_learning_engine/public/c99/css/perm-style.css

# 1) ADD FILTER DEFS FOR DRAGONS/DAIMONS (copy once)
# write: cosmogenesis_learning_engine/public/c99/filters/_filters.html
<svg width=“0” height=“0” style=“position:absolute” aria-hidden=“true” focusable=“false”>
  <defs>
    <filter id=“obsidianSheen” x=“-20%” y=“-20%” width=“140%” height=“140%”>
      <feTurbulence type=“fractalNoise” baseFrequency=“0.9” numOctaves=“1” seed=“7” result=“noise”/>
      <feColorMatrix type=“matrix” values=“0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .8 0” in=“noise” result=“mask”/>
      <feSpecularLighting in=“mask” surfaceScale=“2” specularConstant=“.55” specularExponent=“20” lighting-color=“#d9e0e7” result=“spec”>
        <fePointLight x=“-80” y=“-120” z=“120”/>
      </feSpecularLighting>
      <feComposite in=“spec” in2=“mask” operator=“in” result=“specMasked”/>
      <feBlend in=“SourceGraphic” in2=“specMasked” mode=“screen”/>
    </filter>
    <filter id=“rakuCopperIridescence” x=“-20%” y=“-20%” width=“140%” height=“140%”>
      <feTurbulence type=“turbulence” baseFrequency=“0.005 0.02” numOctaves=“2” seed=“33” result=“n”/>
      <feColorMatrix in=“n” type=“matrix” values=“1 0 0 0 0  0 .65 0 0 0  0 0 .85 0 0  0 0 0 1 0” result=“nm”/>
      <feSpecularLighting in=“nm” surfaceScale=“3” specularConstant=“.4” specularExponent=“18” lighting-color=“#b87333” result=“copper”>
        <fePointLight x=“140” y=“-160” z=“220”/>
      </feSpecularLighting>
      <feBlend in=“SourceGraphic” in2=“copper” mode=“screen”/>
    </filter>
  </defs>
</svg>

# 2) INCLUDE STYLES + FILTERS IN THE BOOK’S LAYOUT
# If your book is static HTML:
#   Add this into the <head> of your book template (e.g., cosmogenesis_learning_engine/pages/_document.html or your base HTML)
<link rel=“stylesheet” href=“/c99/css/perm-style.css” />
<link rel=“preload” as=“fetch” href=“/bridge/c99-bridge.json” crossorigin=“anonymous” />
<!— include filters once near top of <body> —>
<div data-include=“/c99/filters/_filters.html” hidden></div>
<script>
  // Inline include helper (no frameworks): pulls in the SVG filters
  document.addEventListener(‘DOMContentLoaded’, async () => {
    const el = document.querySelector(‘[data-include]’);
    if(el){ const res = await fetch(el.getAttribute(‘data-include’)); el.outerHTML = await res.text(); }
  });
</script>

# 3) MINIMAL RUNTIME HOOKS
# write: cosmogenesis_learning_engine/public/c99/c99-bridge-loader.js
(function(global){
  const Loader = {
    async json(u){ const r = await fetch(u,{cache:’no-store’}); return r.json(); },
    async init(){
      // ND-safe guard
      const style = document.createElement(‘style’);
      style.textContent = “@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}”;
      document.head.appendChild(style);
      // Load tokens and apply CSS vars (optional; CSS already sets most)
      try{
        const tokens = await this.json(‘/c99/tokens/perm-style.json’);
        const p = tokens.palette || {};
        for(const [k,v] of Object.entries(p)){ document.documentElement.style.setProperty(`—${k}`, v); }
      }catch(e){}
      // Load shared manifest
      try{ global.C99_MANIFEST = await this.json(‘/bridge/c99-bridge.json’); }
      catch(e){ global.C99_MANIFEST = { assets:[], rooms:[], creatures:{} }; }
      document.dispatchEvent(new CustomEvent(‘c99:ready’));
    }
  };
  global.C99Loader = Loader;
})(window);

# In your pages (HTML):
<script src=“/c99/c99-bridge-loader.js” defer></script>

# 4) BOOK COMPONENTS (use same classes as SG for a unified look)
# Example dragon/daimon card you can drop into any chapter page:
<div class=“lava-brim obsidian-sculpt obsidian-glint obsidian-facets” style=“padding:16px;max-width:520px;margin:1rem 0” data-creature-id=“drake-obsidian”>
  <div class=“badge”>Obsidian Drake</div>
  <h2