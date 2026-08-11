# -*- coding: utf-8 -*-
import json, os, re

HERE = os.path.dirname(__file__)
people = json.load(open(os.path.join(HERE, "people.json")))
fonts = json.load(open(os.path.join(HERE, "fonts.json")))

FONDO_SVG_RAW = open("/Users/tomascardozo/main/big/brand/nuevo/FONDO.svg").read()
FONDO_INNER = re.search(r"<svg[^>]*>(.*)</svg>", FONDO_SVG_RAW, re.S).group(1)
FONDO_VIEWBOX = re.search(r'viewBox="([^"]+)"', FONDO_SVG_RAW).group(1)

# canonical BIG logo — always source the isotipo from this file
LOGO_SVG_RAW = open("/Users/tomascardozo/main/big/brand/nuevo/big-logo2.svg").read()
ISOTIPO_PATH = re.search(r'\sd="([^"]+)"', LOGO_SVG_RAW).group(1)
ISOTIPO_VIEWBOX = re.search(r'viewBox="([^"]+)"', LOGO_SVG_RAW).group(1)

CATEGORIES = ["Mujeres", "Hombres", "Lifestyle", "Beauty & Makeup", "Trends", "Fitness",
              "Humor & Sketches", "Entretenimiento", "Foodie", "Youtube", "Tecnología & Crypto"]

# maca_castro and ammichis excluded from every roster appearance (client request)
SECTIONS = [
    dict(
        slug="mujeres", name="Mujeres", split=("Muje", "res"),
        subtitle="Moda, humor y estilo de vida — las creadoras que más conectan con sus audiencias en cada plataforma.",
        collage=["juli_savioli", "pauli_veltrano", "sabri_ludmila"],
        order=["juli_savioli", "pia_scarnato", "dulce_pink", "renata_blasevich", "giuli_bellicoso",
               "pauli_veltrano", "agustina_cambra", "eve_vidal", "inez", "mumy",
               "giuli_lourdes", "mely_francano", "martu_morales", "nanu_yael", "sabri_ludmila", "yo_soy_brisa"],
    ),
    dict(
        slug="trends", name="Trends", split=("Tren", "ds"),
        subtitle="Contenido que se mueve rápido: humor, moda y cultura pop, directo al feed de audiencias que marcan tendencia.",
        collage=["pia_scarnato", "giuli_lourdes", "martu_morales"],
        order=["pia_scarnato", "dulce_pink", "giuli_bellicoso", "giuli_lourdes",
               "mely_francano", "martu_morales", "tiago_bergallo"],
    ),
]

def isotipo_svg(size=28, color="#FFFFFF", cls=""):
    return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="{ISOTIPO_VIEWBOX}" style="color:{color}"><path fill="currentColor" d="{ISOTIPO_PATH}"/></svg>'

def tabs_html():
    out = []
    for cat in CATEGORIES:
        out.append(f'<button class="tab" data-cat="{cat}">{cat}</button>')
    return "\n".join(out)

def card_html(pid, i):
    p = people[pid]
    tags = "".join(f'<span class="chip">{t}</span>' for t in p["tags"])
    return f'''
    <article class="card" style="--i:{i}">
      <div class="card-photo" style="background-image:url('{p["photo"]}')"></div>
      <div class="card-body">
        <h3 class="card-name">{p["name"]}</h3>
        <div class="chip-row">{tags}</div>
        <div class="stat-row">
          <div class="stat"><span class="stat-label">Instagram</span><span class="stat-value">{p["ig"]}</span></div>
          <div class="stat"><span class="stat-label">TikTok</span><span class="stat-value">{p["tt"]}</span></div>
        </div>
      </div>
    </article>'''

def collage_html(ids):
    return "".join(
        f'<div class="collage-tile ct-{i+1}" style="background-image:url(\'{people[cid]["photo"]}\')"></div>'
        for i, cid in enumerate(ids)
    )

def category_section(cat):
    slug = cat["slug"]
    head, tail = cat["split"]
    cards = "".join(card_html(pid, i) for i, pid in enumerate(cat["order"]))
    return f'''
  <section class="category" data-cat="{cat["name"]}" id="cat-{slug}">
    <div class="cat-cover">
      <div class="section-inner">
        <div>
          <div class="kicker"><span class="dot"></span>BIG Agency · Roster 2026</div>
          <h1>{head}<span class="lima">{tail}</span></h1>
          <p>{cat["subtitle"]}</p>
        </div>
        <div class="cat-collage">
          {collage_html(cat["collage"])}
        </div>
      </div>
    </div>
    <div class="cat-rail">
      <div class="rail-head">
        <div class="rail-eyebrow">{len(cat["order"])} creadores en nuestro equipo</div>
        <h2>{cat["name"]}</h2>
      </div>
      <div class="rail-wrap">
        <button class="rail-arrow prev">‹</button>
        <button class="rail-arrow next">›</button>
        <div class="rail">
          {cards}
        </div>
      </div>
      <div class="progress-track">
        <div class="progress-bar"><div class="progress-fill"></div></div>
      </div>
    </div>
  </section>'''

font_faces = "\n".join(f'''
@font-face {{
  font-family: 'Inter';
  font-weight: {w};
  font-style: normal;
  src: url(data:font/woff2;base64,{fonts[name]}) format('woff2');
  font-display: swap;
}}''' for name, w in [("Regular", 400), ("Medium", 500), ("Bold", 700), ("Black", 900)])

def fondo_svg():
    return f'<svg viewBox="{FONDO_VIEWBOX}" preserveAspectRatio="xMidYMid slice">{FONDO_INNER}</svg>'

sections_html = "\n".join(category_section(cat) for cat in SECTIONS)
first_slug = SECTIONS[0]["slug"]

html = f'''<title>BIG Roster 2026 — Prototipo</title>
<style>
{font_faces}

:root {{
  --azul: #33419A;
  --azul-2: #4C5AB8;
  --naranja: #FF761E;
  --lima: #E8F29C;
  --negro: #0D0D14;
  --blanco: #FFFFFF;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: 'Inter', -apple-system, sans-serif;
  background: var(--azul);
  color: var(--blanco);
  overflow-x: hidden;
  letter-spacing: -0.01em;
}}

.page-flow {{ position: relative; }}
.bg-fondo {{
  position: absolute; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
}}
.bg-fondo svg {{
  position: absolute; top: -5%; left: -5%; width: 110%; height: 110%; display: block;
}}
.bg-fondo .cls-1 {{ fill: rgba(0,0,0,.1); }}

/* ---------- NAV ---------- */
.nav {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 32px;
}}
.nav-brand {{ display: flex; align-items: center; gap: 10px; flex-shrink: 0; cursor: pointer; border: none; background: none; }}
.nav-brand .word {{ font-family: inherit; font-weight: 800; font-size: 15px; letter-spacing: -0.02em; color: var(--blanco); }}
.nav-brand .word b {{ color: var(--lima); font-weight: 900; }}
.tabs {{
  position: relative; display: flex; gap: 4px;
  overflow-x: auto; scrollbar-width: none; max-width: 74vw;
}}
.tabs::-webkit-scrollbar {{ display: none; }}
.tab-pill {{
  position: absolute; top: 4px; height: calc(100% - 8px);
  border-radius: 999px; background: var(--naranja);
  opacity: 0;
  transition: transform .45s cubic-bezier(.16,1,.3,1), width .45s cubic-bezier(.16,1,.3,1), opacity .3s ease;
  z-index: 0;
}}
.tab-pill.show {{ opacity: 1; }}
.tab {{
  position: relative; z-index: 1;
  background: none; border: none; cursor: pointer;
  font-family: inherit; font-size: 12.5px; font-weight: 600;
  letter-spacing: .02em; text-transform: uppercase;
  color: rgba(255,255,255,.42);
  padding: 9px 16px; white-space: nowrap;
  transition: color .35s ease;
}}
.tab:hover {{ color: rgba(255,255,255,.85); }}
.tab.active {{ color: var(--lima); font-weight: 800; }}

/* ---------- SECTION HEADS (shared) ---------- */
.section-inner {{ position: relative; z-index: 1; width: 100%; max-width: 1400px; margin: 0 auto; padding: 0 32px; }}
.kicker {{
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 12.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  color: rgba(255,255,255,.65); margin-bottom: 22px;
}}
.kicker .dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--lima); }}

/* ---------- PORTADA (general cover) ---------- */
.portada {{
  position: relative; min-height: 100vh; overflow: hidden;
  display: flex; align-items: center; padding: 140px 0 100px;
}}
.portada .section-inner {{ max-width: 900px; }}
.portada-logo {{ margin-bottom: 34px; opacity: 0; animation: riseIn .7s cubic-bezier(.16,1,.3,1) .05s forwards; }}
.portada h1 {{
  font-weight: 900; line-height: .9; letter-spacing: -0.045em;
  font-size: clamp(56px, 8vw, 128px);
  opacity: 0; transform: translateY(24px);
  animation: riseIn .8s cubic-bezier(.16,1,.3,1) .18s forwards;
}}
.portada h1 .lima {{ color: var(--lima); display: block; }}
.portada p {{
  margin-top: 26px; max-width: 520px; font-size: 20px; font-weight: 500;
  line-height: 1.5; color: rgba(255,255,255,.78);
  opacity: 0; transform: translateY(18px);
  animation: riseIn .7s cubic-bezier(.16,1,.3,1) .34s forwards;
}}
@keyframes riseIn {{ to {{ opacity: 1; transform: translateY(0); }} }}

.scroll-cue {{
  position: absolute; bottom: 36px; left: 32px; z-index: 2;
  display: flex; align-items: center; gap: 10px;
  font-size: 12px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase;
  color: rgba(255,255,255,.55); cursor: pointer; border: none; background: none; font-family: inherit;
}}
.scroll-cue .chev {{ display: block; animation: bounce 1.8s ease-in-out infinite; }}
@keyframes bounce {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(5px); }} }}

/* ---------- CATEGORY: cover ---------- */
.cat-cover {{
  position: relative; min-height: 92vh; overflow: hidden;
  display: flex; align-items: center; padding: 120px 0 80px;
}}
.cat-cover .section-inner {{
  display: grid; grid-template-columns: 1.15fr 1fr; gap: 40px; align-items: center;
}}
.cat-cover h1 {{
  font-weight: 900; line-height: .92; letter-spacing: -0.045em;
  font-size: clamp(64px, 9vw, 148px);
  opacity: 0; transform: translateY(24px);
  animation: riseIn .8s cubic-bezier(.16,1,.3,1) .22s forwards;
}}
.cat-cover h1 .lima {{ color: var(--lima); }}
.cat-cover .kicker {{ opacity: 0; transform: translateY(14px); animation: riseIn .7s cubic-bezier(.16,1,.3,1) .1s forwards; }}
.cat-cover p {{
  margin-top: 26px; max-width: 460px; font-size: 19px; font-weight: 500;
  line-height: 1.45; color: rgba(255,255,255,.8);
  opacity: 0; transform: translateY(18px);
  animation: riseIn .7s cubic-bezier(.16,1,.3,1) .38s forwards;
}}
.cat-collage {{
  position: relative; height: 560px;
  opacity: 0; animation: riseIn .9s cubic-bezier(.16,1,.3,1) .5s forwards;
}}
.collage-tile {{
  position: absolute; border-radius: 32px; background-size: cover; background-position: center;
  animation: float 7s ease-in-out infinite;
}}
.ct-1 {{ width: 46%; height: 46%; left: 0; top: 4%; animation-delay: 0s; }}
.ct-2 {{ width: 46%; height: 34%; left: 0; bottom: 2%; animation-delay: .6s; }}
.ct-3 {{ width: 44%; height: 88%; right: 0; top: 8%; animation-delay: 1.2s; }}
@keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-14px); }} }}

/* ---------- CATEGORY: rail ---------- */
.cat-rail {{ position: relative; overflow: hidden; padding: 40px 0 120px; }}
.rail-head {{
  position: relative; z-index: 1;
  max-width: 1400px; margin: 0 auto 48px; padding: 0 32px;
  opacity: 0; transform: translateY(20px); transition: opacity .7s cubic-bezier(.16,1,.3,1), transform .7s cubic-bezier(.16,1,.3,1);
}}
.rail-head.inview {{ opacity: 1; transform: translateY(0); }}
.rail-eyebrow {{ color: var(--lima); font-weight: 700; font-size: 13px; letter-spacing: .06em; text-transform: uppercase; }}
.rail-head h2 {{ font-size: clamp(28px, 4vw, 40px); font-weight: 800; letter-spacing: -0.02em; margin-top: 10px; }}
.rail-head p {{ margin-top: 12px; color: rgba(255,255,255,.6); font-size: 16px; max-width: 560px; }}

.rail-wrap {{ position: relative; z-index: 1; max-width: 1400px; margin: 0 auto; }}
.rail {{
  display: flex; gap: 26px; overflow-x: auto; scroll-snap-type: x proximity;
  padding: 10px 32px 28px; cursor: grab; user-select: none;
  scrollbar-width: none;
}}
.rail::-webkit-scrollbar {{ display: none; }}
.rail.dragging {{ cursor: grabbing; scroll-snap-type: none; }}

.card {{
  flex: 0 0 250px; scroll-snap-align: start;
  transition: transform .35s cubic-bezier(.16,1,.3,1);
}}
.card-photo {{
  width: 250px; height: 250px; border-radius: 25px;
  background-size: cover; background-position: center top;
  pointer-events: none;
}}
.card-body {{
  background: #EEE; border-radius: 20px; padding: 20px;
  margin-top: -34px; position: relative; z-index: 1;
  display: flex; flex-direction: column; gap: 14px;
  pointer-events: none;
}}
.card-name {{ color: var(--azul); font-size: 26px; font-weight: 700; letter-spacing: -0.035em; line-height: 1.08; }}
.chip-row {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.chip {{
  background: var(--blanco); color: var(--azul); font-size: 11px; font-weight: 600;
  padding: 5px 10px; border-radius: 8px; letter-spacing: -0.01em;
}}
.stat-row {{ display: flex; gap: 8px; }}
.stat {{ flex: 1; background: var(--naranja); border-radius: 12px; padding: 10px 12px; }}
.stat-label {{ display: block; color: var(--lima); font-size: 10.5px; font-weight: 500; letter-spacing: -0.01em; }}
.stat-value {{ display: block; color: var(--lima); font-size: 18px; font-weight: 700; letter-spacing: -0.03em; margin-top: 1px; }}

.rail-arrow {{
  position: absolute; top: 42%; transform: translateY(-50%);
  width: 46px; height: 46px; border-radius: 50%; border: none; cursor: pointer;
  background: rgba(255,255,255,.14); color: var(--blanco);
  display: flex; align-items: center; justify-content: center; font-size: 18px;
  transition: background .25s ease, transform .25s ease;
  z-index: 3;
}}
.rail-arrow:hover {{ background: var(--lima); color: var(--negro); transform: translateY(-50%) scale(1.08); }}
.rail-arrow.prev {{ left: 4px; }}
.rail-arrow.next {{ right: 4px; }}

.progress-track {{ max-width: 1400px; margin: 8px auto 0; padding: 0 32px; }}
.progress-bar {{ height: 3px; background: rgba(255,255,255,.14); border-radius: 3px; overflow: hidden; }}
.progress-fill {{ height: 100%; width: 25%; background: var(--lima); border-radius: 3px; transition: width .1s linear; }}

.toast {{
  position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%) translateY(20px);
  background: var(--blanco); color: var(--negro); font-size: 13px; font-weight: 600;
  padding: 12px 20px; border-radius: 999px; box-shadow: 0 14px 30px rgba(13,13,20,.4);
  opacity: 0; pointer-events: none; transition: opacity .3s ease, transform .3s ease;
  z-index: 200;
}}
.toast.show {{ opacity: 1; transform: translateX(-50%) translateY(0); }}

footer {{
  padding: 46px 32px; display: flex; align-items: center; justify-content: space-between;
  color: rgba(255,255,255,.4); font-size: 12.5px; border-top: 1px solid rgba(255,255,255,.1);
}}

@media (max-width: 860px) {{
  .cat-cover .section-inner {{ grid-template-columns: 1fr; }}
  .cat-collage {{ height: 320px; order: -1; }}
  .tabs {{ max-width: 56vw; }}
}}
</style>

<div class="page-flow" id="pageFlow">
  <div class="bg-fondo" aria-hidden="true">{fondo_svg()}</div>

  <nav class="nav">
    <button class="nav-brand" id="navBrand">
      {isotipo_svg(24, "#FFFFFF")}
      <span class="word">BIG <b>Roster 2026</b></span>
    </button>
    <div class="tabs" id="tabs">
      <div class="tab-pill" id="tabPill"></div>
      {tabs_html()}
    </div>
  </nav>

  <section class="portada" id="portada">
    <div class="section-inner">
      {isotipo_svg(52, "#FFFFFF", "portada-logo")}
      <h1>Roster<span class="lima">de Talentos</span></h1>
      <p>Creadores y creadoras que conectan marcas con audiencias reales, en cada categoría y en cada red.</p>
    </div>
    <button class="scroll-cue" onclick="document.getElementById('cat-{first_slug}').scrollIntoView({{behavior:'smooth'}})">
      Explorar por categoría <span class="chev">↓</span>
    </button>
  </section>
{sections_html}

  <footer>
    <span>BIG Agency · Prototipo de sistema — 2026</span>
    <span>Roster</span>
  </footer>
</div>

<div class="toast" id="toast">Esta vista todavía no está armada</div>

<script>
// --- nav pill: active state driven by scrollspy over .category sections ---
const tabsEl = document.getElementById('tabs');
const pill = document.getElementById('tabPill');
const tabEls = Array.from(document.querySelectorAll('.tab'));
let currentActive = null;

function movePill(el) {{
  if (!el) {{ pill.classList.remove('show'); return; }}
  const r = el.getBoundingClientRect();
  const navR = tabsEl.getBoundingClientRect();
  pill.style.width = r.width + 'px';
  pill.style.transform = `translateX(${{r.left - navR.left + tabsEl.scrollLeft}}px)`;
  pill.classList.add('show');
}}

function setActive(cat) {{
  currentActive = cat;
  tabEls.forEach(t => t.classList.toggle('active', t.dataset.cat === cat));
  const el = cat ? tabEls.find(t => t.dataset.cat === cat) : null;
  movePill(el);
}}

const toast = document.getElementById('toast');
let toastTimer;
tabEls.forEach(t => {{
  t.addEventListener('mouseenter', () => movePill(t));
  t.addEventListener('click', () => {{
    const target = document.getElementById('cat-' + t.dataset.cat.toLowerCase().replace(/[^a-z0-9]+/g, '-'));
    if (target) {{ target.scrollIntoView({{ behavior: 'smooth' }}); return; }}
    toast.textContent = `"${{t.dataset.cat}}" todavía no está armada en este prototipo`;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2400);
  }});
}});
tabsEl.addEventListener('mouseleave', () => movePill(currentActive ? tabEls.find(t => t.dataset.cat === currentActive) : null));
document.getElementById('navBrand').addEventListener('click', () => document.getElementById('portada').scrollIntoView({{ behavior: 'smooth' }}));

const catObserver = new IntersectionObserver((entries) => {{
  entries.forEach(e => {{ if (e.isIntersecting) setActive(e.target.dataset.cat); }});
}}, {{ rootMargin: '-45% 0px -45% 0px', threshold: 0 }});
document.querySelectorAll('.category').forEach(el => catObserver.observe(el));

const portadaObserver = new IntersectionObserver((entries) => {{
  entries.forEach(e => {{ if (e.isIntersecting) setActive(null); }});
}}, {{ rootMargin: '-45% 0px -45% 0px', threshold: 0 }});
portadaObserver.observe(document.getElementById('portada'));

window.addEventListener('resize', () => movePill(currentActive ? tabEls.find(t => t.dataset.cat === currentActive) : null));

// --- reveal on scroll (section headings only) ---
const io = new IntersectionObserver((entries) => {{
  entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('inview'); }});
}}, {{ threshold: .2 }});
document.querySelectorAll('.rail-head').forEach(el => io.observe(el));

// --- carousel: drag to scroll + progress + focus scale (one instance per category) ---
document.querySelectorAll('.cat-rail').forEach(catRail => {{
  const rail = catRail.querySelector('.rail');
  const cardsEls = Array.from(rail.querySelectorAll('.card'));
  const progressFill = catRail.querySelector('.progress-fill');
  const prevBtn = catRail.querySelector('.rail-arrow.prev');
  const nextBtn = catRail.querySelector('.rail-arrow.next');

  let isDown = false, startX = 0, startScroll = 0, moved = false;
  rail.addEventListener('pointerdown', (e) => {{
    isDown = true; moved = false;
    rail.classList.add('dragging');
    startX = e.clientX; startScroll = rail.scrollLeft;
    rail.setPointerCapture(e.pointerId);
  }});
  rail.addEventListener('pointermove', (e) => {{
    if (!isDown) return;
    const dx = e.clientX - startX;
    if (Math.abs(dx) > 4) moved = true;
    rail.scrollLeft = startScroll - dx;
  }});
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev =>
    rail.addEventListener(ev, () => {{ isDown = false; rail.classList.remove('dragging'); }})
  );
  rail.addEventListener('click', (e) => {{ if (moved) e.preventDefault(); }}, true);

  function updateProgress() {{
    const max = rail.scrollWidth - rail.clientWidth;
    const pct = max > 0 ? (rail.scrollLeft / max) * 100 : 0;
    progressFill.style.width = pct + '%';
  }}

  function updateFocus() {{
    const railRect = rail.getBoundingClientRect();
    const center = railRect.left + railRect.width / 2;
    cardsEls.forEach(c => {{
      const r = c.getBoundingClientRect();
      const cCenter = r.left + r.width / 2;
      const dist = Math.abs(center - cCenter);
      const p = Math.max(0, 1 - dist / (railRect.width * .8));
      const scale = .96 + p * .04;
      c.style.transform = `scale(${{scale}})`;
    }});
  }}

  let ticking = false;
  rail.addEventListener('scroll', () => {{
    updateProgress();
    if (!ticking) {{
      requestAnimationFrame(() => {{ updateFocus(); ticking = false; }});
      ticking = true;
    }}
  }});

  prevBtn.addEventListener('click', () => rail.scrollBy({{ left: -276, behavior: 'smooth' }}));
  nextBtn.addEventListener('click', () => rail.scrollBy({{ left: 276, behavior: 'smooth' }}));

  updateProgress();
  updateFocus();
  window.addEventListener('resize', updateFocus);
}});
</script>
'''

out_path = os.path.join(HERE, "roster_trends_prototype.html")
with open(out_path, "w") as f:
    f.write(html)
print("wrote", out_path, len(html)/1024, "KB")
