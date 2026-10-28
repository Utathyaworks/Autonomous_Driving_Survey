/* Interactive views built from data.json. None of these plots appears in the paper. */
const EXP = {data: null, E: 3, metric: "dcr", sizeBy: "users", sel: null, timer: null};
const MC = {M1: "var(--m1)", M2: "var(--m2)", M3: "var(--m3)", M4: "var(--m4)"};
const fmt = n => n >= 1e6 ? (n / 1e6).toFixed(1) + " M" : n >= 1e3 ? Math.round(n / 1e3) + " k" : String(Math.round(n * 10) / 10);
const stageOf = s => mat().filter(r => r.stage === s);
const mat = () => EXP.data.maturity;
const fielded = r => r["E" + EXP.E] === "M1" || r["E" + EXP.E] === "M2";

function exploreHTML() {
  return `
<section class="fig" id="x1"><h3>1. Slide the road from motorway to lane-free</h3>
<p>Each dot is a method family from the survey. Move the entropy level and watch the grades change. Fielded or proven means M1 or M2.</p>
<div class="tools"><span class="count">Road entropy</span>
${[1, 2, 3, 4, 5].map(e => `<button class="chip" data-e="${e}" aria-pressed="${e === EXP.E}">E${e}</button>`).join("")}
<button class="chip" id="play">Play</button><span class="count" id="xsum"></span></div>
<div class="swarm" id="swarm"></div>
<div class="legend"><span><span class="dot" style="background:var(--m1)"></span>M1 mature, fielded</span><span><span class="dot" style="background:var(--m2)"></span>M2 proven, not deployed</span><span><span class="dot" style="background:var(--m3)"></span>M3 prototype</span><span><span class="dot" style="background:var(--m4)"></span>M4 absent</span></div>
<svg id="curve" viewBox="0 0 640 190" role="img" aria-label="Share of method families that are fielded or proven, by entropy level"></svg>
<p class="hint" id="tip">Hover a dot for the family and the basis of its hardest grade.</p></section>

<section class="fig" id="x2"><h3>2. Annotation per person, not per kilometre</h3>
<p>Ten largest economies. Tile area follows the number of daily road users (or is equal); colour follows annotated frames, on a log scale. Switch the lens and the ranking changes.</p>
<div class="tools"><span class="count">Colour by</span>
<button class="chip" data-m="dcr" aria-pressed="${EXP.metric === "dcr"}">frames per 1,000 road-km</button>
<button class="chip" data-m="perMillion" aria-pressed="${EXP.metric === "perMillion"}">frames per million daily users</button>
<span class="count">Size by</span>
<button class="chip" data-s="users" aria-pressed="${EXP.sizeBy === "users"}">daily users</button>
<button class="chip" data-s="equal" aria-pressed="${EXP.sizeBy === "equal"}">equal</button></div>
<svg id="carto" viewBox="0 0 720 330" role="img" aria-label="Cartogram of annotation coverage"></svg>
<p class="hint" id="ctip">Frame counts are approximate and restricted to perception datasets; a UK value below 1,000 is drawn at 500.</p></section>

<section class="fig" id="x3"><h3>3. Where each kind of benchmark was collected</h3>
<p>Datasets from the survey's two overview tables, by collection region and task family. Circle area is the number of datasets; click a cell to list them.</p>
<svg id="matrix" viewBox="0 0 760 420" role="img" aria-label="Datasets by region and task family"></svg>
<div id="mlist" class="hint">Click a cell.</div></section>`;
}

function bindExplore() {
  document.querySelectorAll("[data-e]").forEach(b => b.onclick = () => { stopPlay(); EXP.E = +b.dataset.e; refreshE(); });
  $("#play").onclick = () => {
    if (EXP.timer) { stopPlay(); return; }
    $("#play").textContent = "Stop"; EXP.E = 1; refreshE();
    EXP.timer = setInterval(() => { if (EXP.E >= 5) { stopPlay(); return; } EXP.E++; refreshE(); }, 1100);
  };
  document.querySelectorAll("[data-m]").forEach(b => b.onclick = () => { EXP.metric = b.dataset.m; refreshCarto(); });
  document.querySelectorAll("[data-s]").forEach(b => b.onclick = () => { EXP.sizeBy = b.dataset.s; refreshCarto(); });
  buildSwarm(); refreshE(); refreshCarto(); drawMatrix();
}
function stopPlay() { if (EXP.timer) { clearInterval(EXP.timer); EXP.timer = null; } const p = $("#play"); if (p) p.textContent = "Play"; }

/* ---- 1. swarm ---- */
function buildSwarm() {
  const cols = ["Sense", "Plan", "Act"], el = $("#swarm");
  el.innerHTML = cols.map(s => `<div class="col"><div class="colh" style="color:${COL[s]}">${s} <span class="count" id="n${s}"></span></div><div class="dots">${stageOf(s).map((r, i) => `<span class="fam" data-f="${s}|${i}" tabindex="0" aria-label="${esc(r.family)}"></span>`).join("")}</div></div>`).join("");
  el.querySelectorAll(".fam").forEach(d => {
    const [s, i] = d.dataset.f.split("|"), r = stageOf(s)[+i];
    const show = () => { $("#tip").innerHTML = `<b>${esc(r.family)}</b> (${s}): ${["E1", "E2", "E3", "E4", "E5"].map(e => `${e} ${r[e]}`).join(", ")}. <i>${esc(r.basis)}</i>`; };
    d.onmouseenter = show; d.onfocus = show;
  });
}
function refreshE() {
  document.querySelectorAll("[data-e]").forEach(b => b.setAttribute("aria-pressed", +b.dataset.e === EXP.E));
  document.querySelectorAll(".fam").forEach(d => { const [s, i] = d.dataset.f.split("|"), r = stageOf(s)[+i]; d.style.background = MC[r["E" + EXP.E]]; d.title = r.family + ": " + r["E" + EXP.E]; });
  let tot = 0, ok = 0;
  for (const s of ["Sense", "Plan", "Act"]) { const rows = stageOf(s), k = rows.filter(fielded).length; tot += rows.length; ok += k; $("#n" + s).textContent = `${k} of ${rows.length}`; }
  $("#xsum").textContent = `At E${EXP.E}: ${ok} of ${tot} families fielded or proven (${Math.round(100 * ok / tot)}%)`;
  drawCurve();
}
function drawCurve() {
  const W = 640, H = 190, L = 40, B = 28, T = 14, xs = e => L + (e - 1) * (W - L - 60) / 4, ys = v => T + (1 - v) * (H - T - B);
  let s = "";
  for (const v of [0, .25, .5, .75, 1]) s += `<line x1="${L}" x2="${W - 20}" y1="${ys(v)}" y2="${ys(v)}" stroke="var(--line)" stroke-width=".6"/><text x="${L - 6}" y="${ys(v) + 4}" text-anchor="end" font-size="10.5" fill="var(--muted)">${Math.round(v * 100)}%</text>`;
  [1, 2, 3, 4, 5].forEach(e => s += `<text x="${xs(e)}" y="${H - 8}" text-anchor="middle" font-size="11" fill="var(--muted)">E${e}</text>`);
  s += `<rect x="${xs(EXP.E) - 12}" y="${T}" width="24" height="${H - T - B}" fill="var(--tint)"/>`;
  for (const g of ["Sense", "Plan", "Act"]) {
    const rows = stageOf(g), pts = [1, 2, 3, 4, 5].map(e => [xs(e), ys(rows.filter(r => r["E" + e] === "M1" || r["E" + e] === "M2").length / rows.length)]);
    s += `<polyline fill="none" stroke="${COL[g]}" stroke-width="2" points="${pts.map(p => p.join(",")).join(" ")}"/>`;
    pts.forEach((p, i) => s += `<circle cx="${p[0]}" cy="${p[1]}" r="${i + 1 === EXP.E ? 5 : 3}" fill="${COL[g]}"/>`);
    s += `<text x="${pts[4][0] + 7}" y="${pts[4][1] + 4 + ({Sense: 12, Plan: 0, Act: -12}[g])}" font-size="11" fill="${COL[g]}">${g}</text>`;
  }
  $("#curve").innerHTML = s;
}

/* ---- 2. cartogram ---- */
function refreshCarto() {
  document.querySelectorAll("[data-m]").forEach(b => b.setAttribute("aria-pressed", b.dataset.m === EXP.metric));
  document.querySelectorAll("[data-s]").forEach(b => b.setAttribute("aria-pressed", b.dataset.s === EXP.sizeBy));
  const E = EXP.data.economies.slice().sort((a, b) => b.users - a.users), W = 720, H = 330;
  const vals = E.map(e => e[EXP.metric]).filter(v => v > 0), lo = Math.log10(Math.min(...vals)), hi = Math.log10(Math.max(...vals));
  const color = v => { if (v <= 0) return "var(--m4)"; const t = (Math.log10(v) - lo) / (hi - lo || 1); return `color-mix(in srgb, var(--m1) ${Math.round(18 + 82 * t)}%, var(--surface))`; };
  const side = e => EXP.sizeBy === "equal" ? 84 : Math.max(58, 8.4 * Math.sqrt(e.users));
  let x = 6, y = 6, rowH = 0, s = "";
  for (const e of E) {
    const w = side(e);
    if (x + w > W - 6) { x = 6; y += rowH + 8; rowH = 0; }
    const v = e[EXP.metric], dark = v > 0 && ((Math.log10(v) - lo) / (hi - lo || 1)) > .45;
    s += `<g><rect x="${x}" y="${y}" width="${w}" height="${w}" rx="6" fill="${color(v)}" stroke="var(--line)"><title>${e.name}: ${fmt(e.users * 1e6)} daily users, ${fmt(e.roadKm)} km, ${fmt(e.frames)} annotated frames</title></rect>
<text x="${x + 7}" y="${y + 17}" font-size="12.5" font-weight="700" fill="${dark ? "#fff" : "var(--ink)"}">${e.name}</text>
<text x="${x + 7}" y="${y + 32}" font-size="10.5" fill="${dark ? "#e6ecf4" : "var(--muted)"}">${e.users} M users</text>
<text x="${x + 7}" y="${y + w - 9}" font-size="12" font-weight="600" fill="${dark ? "#fff" : "var(--ink)"}">${v > 0 ? (e.ukBound && v < 100 ? "< " : "") + (v >= 10 ? Math.round(v).toLocaleString("en") : v.toFixed(1)) : "none"}</text></g>`;
    x += w + 8; rowH = Math.max(rowH, w);
  }
  $("#carto").setAttribute("viewBox", `0 0 ${W} ${y + rowH + 10}`);
  $("#carto").innerHTML = s;
  const top = E.slice().sort((a, b) => b[EXP.metric] - a[EXP.metric]).slice(0, 3).map(e => e.name).join(", ");
  $("#ctip").textContent = `Highest by this lens: ${top}. Frame counts are approximate and cover perception datasets only; the UK is drawn from a bound below 1,000 frames.`;
}

/* ---- 3. region x task matrix ---- */
const SHORT = {"Camera scene understanding": "Camera scenes", "Adverse conditions": "Adverse conditions", "3D detection and radar": "3D and radar", "Localisation": "Localisation", "Cooperative and infrastructure": "Cooperative", "Unstructured and Global South": "Unstructured", "Forecasting": "Forecasting", "Closed-loop control": "Closed-loop"};
function drawMatrix() {
  const D = EXP.data.datasets, regions = ["USA", "Germany", "China", "India", "South Korea", "Other Europe", "Canada", "Africa", "Middle East and Europe", "Multi-region or global", "Synthetic"];
  const fams = ["Camera scene understanding", "Adverse conditions", "3D detection and radar", "Localisation", "Cooperative and infrastructure", "Unstructured and Global South", "Forecasting", "Closed-loop control"];
  const W = 760, L = 170, T = 112, cw = (W - L - 10) / fams.length, rh = 28, H = T + regions.length * rh + 10;
  const cell = (r, f) => D.filter(d => d.region === r && d.family === f);
  let s = "";
  fams.forEach((f, j) => s += `<text transform="translate(${L + j * cw + cw / 2},${T - 8}) rotate(-35)" font-size="11" fill="var(--muted)">${SHORT[f]}</text>`);
  regions.forEach((r, i) => {
    s += `<text x="${L - 10}" y="${T + i * rh + rh / 2 + 4}" text-anchor="end" font-size="12" fill="var(--ink)">${r}</text><line x1="${L}" x2="${W - 10}" y1="${T + (i + 1) * rh}" y2="${T + (i + 1) * rh}" stroke="var(--line)" stroke-width=".5"/>`;
    fams.forEach((f, j) => {
      const c = cell(r, f).length, cx = L + j * cw + cw / 2, cy = T + i * rh + rh / 2;
      if (c) s += `<circle class="mc" data-r="${r}" data-f="${f}" cx="${cx}" cy="${cy}" r="${4 + 4.2 * Math.sqrt(c)}" fill="${r === "India" || r === "Africa" ? "var(--amber)" : "var(--blue)"}" fill-opacity=".85" style="cursor:pointer"><title>${r}, ${f}: ${c}</title></circle><text x="${cx}" y="${cy + 3.6}" text-anchor="middle" font-size="10" fill="#fff" pointer-events="none">${c}</text>`;
      else s += `<circle cx="${cx}" cy="${cy}" r="2" fill="var(--line)"/>`;
    });
  });
  const m = $("#matrix"); m.setAttribute("viewBox", `0 0 ${W} ${H}`); m.innerHTML = s;
  m.querySelectorAll(".mc").forEach(c => c.onclick = () => {
    const l = cell(c.dataset.r, c.dataset.f);
    $("#mlist").innerHTML = `<b>${esc(c.dataset.r)} &middot; ${esc(c.dataset.f)}</b>: ` + l.map(d => `${esc(d.name)} (${esc(d.year)}${d.scale && d.scale !== "---" ? ", " + esc(d.scale) : ""})`).join("; ");
  });
}

function loadExplore(cb) {
  if (EXP.data) return cb();
  fetch("data.json").then(r => r.json()).then(d => { EXP.data = d; cb(); }).catch(() => { $("#main").textContent = "Could not load data.json."; });
}
