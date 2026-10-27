"""Maturity heatmap: every method family in the Sense, Plan and Act maturity tables, graded M1-M4 at E1-E5.
Reads data/maturity.csv (extracted from the manuscript tables by extract_maturity.py); nothing is typed in here."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "figures", "charts") if os.path.isdir(os.path.join(ROOT, "figures", "charts")) else os.path.join(ROOT, "figures")
rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "maturity.csv"), encoding="utf-8")))
E = ["E1", "E2", "E3", "E4", "E5"]
# one blue ramp, dark = fielded; M4 (absent) is amber-tinted so the gap is what the eye finds
FILL = {"M1": "#153A68", "M2": "#2668B2", "M3": "#A0C1E6", "M4": "#FBE6BD"}
TEXT = {"M1": "white", "M2": "white", "M3": INK, "M4": OURS_INK}
STAGES = ["Sense", "Plan", "Act"]


def share(stage, e):
    r = [x for x in rows if x["stage"] == stage]
    return 100 * sum(x[e] in ("M1", "M2") for x in r) / len(r)


def fig_heat():
    n = len(rows) + 2 * 1.0
    fig = plt.figure(figsize=(W, 6.7))
    gs = fig.add_gridspec(len(STAGES), 2, width_ratios=[1.0, 0.0001], hspace=0.12,
                          height_ratios=[sum(x["stage"] == s for x in rows) for s in STAGES],
                          left=0.40, right=0.985, top=0.925, bottom=0.135)
    for k, s in enumerate(STAGES):
        ax = fig.add_subplot(gs[k, 0]); r = [x for x in rows if x["stage"] == s]
        for i, x in enumerate(r):
            for j, e in enumerate(E):
                g = x[e]
                ax.add_patch(plt.Rectangle((j, -i), 0.94, 0.86, color=FILL[g], lw=0))
                ax.text(j + 0.47, -i + 0.43, g, ha="center", va="center", fontsize=6.5, color=TEXT[g], fontweight="bold")
            ax.text(-0.12, -i + 0.43, x["family"], ha="right", va="center", fontsize=6.5, color=INK)
        ax.set_xlim(0, 5); ax.set_ylim(-len(r) + 0.95, 1.0); ax.axis("off")
        # the cliff: bracket between E3 and E4
        ax.plot([3 - 0.03] * 2, [-len(r) + 0.95, 0.9], color=OURS, lw=0.7, ls=(0, (3, 2)))
        ax.text(-3.0, 0.43 - 0.15, s.upper(), ha="left", va="bottom", fontsize=8, fontweight="bold", color=LIT_DEEP, transform=ax.transData) if False else None
        ax.text(-0.9, 1.0, s.upper(), transform=ax.transAxes, fontsize=8, fontweight="bold", color=LIT_DEEP, ha="right", va="bottom") if False else None
        ax.text(0, 1.02, s, transform=ax.transAxes, fontsize=8, fontweight="bold", color=LIT_DEEP, ha="right", va="bottom", clip_on=False) if False else None
        ax.text(-0.02, 1.0, s, transform=ax.transAxes, fontsize=8, fontweight="bold", color=LIT_DEEP, ha="right", va="bottom")
        pct = ", ".join(f"{e} {share(s, e):.0f}%" for e in ("E3", "E4"))
        ax.text(1.0, 1.0, f"fielded or proven (M1+M2): {pct}", transform=ax.transAxes, fontsize=6.5, color=MUTED, ha="right", va="bottom")
        if k == 0:
            for j, e in enumerate(E):
                ax.text(j + 0.47, 1.9, e, ha="center", va="bottom", fontsize=7, fontweight="bold", color=INK) if False else None
    # column header + legend
    ax0 = fig.axes[0]
    for j, e in enumerate(E):
        ax0.text(j + 0.47, 2.15, e, ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=INK)
    ax0.text(5, 3.5, "", fontsize=1)
    lx = 0.015
    labs = [("M1", "mature, fielded"), ("M2", "proven, not deployed"), ("M3", "prototype"), ("M4", "absent")]
    for q, (g, t) in enumerate(labs):
        x = lx + q * 0.245
        fig.patches.append(plt.Rectangle((x, 0.072), 0.022, 0.012, transform=fig.transFigure, color=FILL[g], lw=0))
        fig.text(x + 0.028, 0.078, f"{g} {t}", fontsize=6.5, va="center", color=INK)
    fig.text(0.015, 0.025, "Finding: in all three stages the share of families that are fielded or proven (M1+M2) falls from "
             f"{min(share(s, 'E3') for s in STAGES):.0f}–{max(share(s, 'E3') for s in STAGES):.0f}% at E3 to "
             f"{min(share(s, 'E4') for s in STAGES):.0f}–{max(share(s, 'E4') for s in STAGES):.0f}% at E4 (dashed line).".replace("% at E4", "%"+chr(10)+"at E4"),
             fontsize=6.6, color=OURS_INK, fontweight="bold")
    fig.savefig(os.path.join(OUT, "maturity_heatmap.pdf")); plt.close(fig)


if __name__ == "__main__":
    for s in STAGES:
        print(s, {e: round(share(s, e)) for e in E}, len([x for x in rows if x["stage"] == s]))
    fig_heat()
