"""Introduction chart. (b) is computed from the survey-taxonomy table (unique survey citations per category);
(a) uses the WHO and road-fatality shares quoted in the Global South paragraph. Nothing else is plotted."""
import os, sys, re, csv
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import numpy as np, matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "figures", "charts") if os.path.isdir(os.path.join(ROOT, "figures", "charts")) else os.path.join(ROOT, "figures")
CSV = os.path.join(ROOT, "data", "survey_taxonomy.csv")
SRC = os.path.join(ROOT, "sections", "section 1 - Introduction.tex")


def extract():
    t = open(SRC, encoding="utf-8").read()
    i = t.index("label{tab:survey_taxonomy}")
    body = t[i:t.index("\\end{tabularx}", i)]
    rows = []
    for r in re.split(r"\\\\", body):
        m = re.search(r"\\textbf\{([^}]*)\}\s*&(.*)", r, re.S)
        if not m:
            continue
        name = m.group(1).replace("\\&", "&")
        keys = {k.strip() for c in re.findall(r"\\cite\{([^}]*)\}", m.group(2)) for k in c.split(",")}
        if name.startswith("Research Category"):
            continue
        rows.append((name, len(keys)))
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["category", "surveys"]); w.writerows(rows)
    return rows


def load():
    if os.path.exists(SRC):
        return extract()
    return [(r["category"], int(r["surveys"])) for r in csv.DictReader(open(CSV, encoding="utf-8"))]


def fig_intro():
    rows = load()
    fig = plt.figure(figsize=(W, 3.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[0.8, 1.35], wspace=0.62, left=0.07, right=0.985, top=0.80, bottom=0.17)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
    # (a) burden against vehicles, and the three WHO regions quoted
    items = [("Road deaths in\nlow- and middle-\nincome countries", 92, OURS), ("Vehicles in those\ncountries", 60, LIT_MID)]
    a.bar([0, 1], [92, 60], color=[LIT, LIT_MID], width=0.58, lw=0)
    a.text(0, 94, "92%", ha="center", fontsize=7.5, fontweight="bold"); a.text(1, 62, "about 60%", ha="center", fontsize=6.6)
    a.set_xticks([0, 1], ["road\ndeaths", "vehicles"], fontsize=6.4); a.set_ylim(0, 108); a.set_ylabel("share of world total (%)")
    a.text(0.5, 101, "low- and middle-income countries", ha="center", fontsize=6.2, color=MUTED)
    a.set_ylim(0, 112)
    a.grid(axis="y", color=LINE, lw=0.35); a.set_axisbelow(True)
    for x, v, n in [(0, 28, "S-E Asia 28%"), ]:
        pass
    panel(a, "a", "Burden", "WHO / road-traffic figures quoted in the text")
    # (b) surveys per category
    rows = sorted(rows, key=lambda r: r[1])
    names = [r[0] for r in rows]; vals = [r[1] for r in rows]
    y = np.arange(len(rows))
    cols = [OURS if v <= 2 else LIT for v in vals]
    b.barh(y, vals, color=cols, height=0.62, lw=0)
    for yi, v in zip(y, vals):
        b.text(v + 0.12, yi, str(v), va="center", fontsize=6.2, color=OURS_INK if v <= 2 else MUTED)
    b.set_yticks(y, names, fontsize=6); b.set_xlim(0, max(vals) + 1.2)
    b.set_xlabel("distinct surveys cited in the taxonomy table")
    b.grid(axis="x", color=LINE, lw=0.35); b.set_axisbelow(True)
    panel(b, "b", "Attention", "surveys per research category; amber = two or fewer")
    fig.text(0.07, 0.015, "Finding: 92% of road deaths fall in low- and middle-income countries; the surveyed literature thins out exactly where\n"
             "that burden sits (Global South, mixed traffic, deployment logistics are absent from the taxonomy altogether).",
             fontsize=6.3, color=OURS_INK, fontweight="bold")
    fig.savefig(os.path.join(OUT, "intro_burden.pdf")); plt.close(fig)
    return rows


if __name__ == "__main__":
    print(fig_intro())
