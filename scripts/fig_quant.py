"""Quantitative-analysis chart. All values are the figures the cited authors state, as quoted in Sec. 3.3."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import numpy as np, matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")


def fig_results():
    fig = plt.figure(figsize=(W, 2.7))
    gs = fig.add_gridspec(1, 3, width_ratios=[0.8, 1.0, 1.25], wspace=0.5, left=0.075, right=0.985, top=0.77, bottom=0.25)
    a, b, c = (fig.add_subplot(g) for g in gs)
    # (a) nuScenes detection score: camera-only vs LiDAR-based, as quoted
    names = ["BEVFormer\ncamera only", "CenterPoint\nLiDAR"]; v = [56.9, 65.5]
    a.bar(range(2), v, color=[LIT_MID, LIT], width=0.55, lw=0)
    for i, x in enumerate(v): a.text(i, x + 1, f"{x}", ha="center", fontsize=7, fontweight="bold")
    a.set_xticks(range(2), names, fontsize=6.2); a.set_ylim(40, 72); a.set_ylabel("NDS (nuScenes)")
    a.annotate("", xy=(0.5, 65.5), xytext=(0.5, 56.9), arrowprops=dict(arrowstyle="<->", lw=0.6, color=OURS))
    a.text(0.5, 67.2, "+8.6", color=OURS_INK, fontsize=6.6, fontweight="bold", ha="center")
    panel(a, "a", "Price of inferring depth")
    # (b) ByteTrack on MOT17 test: metric spread
    m = ["MOTA", "IDF1", "HOTA"]; mv = [80.3, 77.3, 63.1]
    b.barh(range(3)[::-1], mv, color=[LIT, LIT, OURS], height=0.55, lw=0)
    for yi, x in zip(range(3)[::-1], mv): b.text(x + 1, yi, f"{x}", va="center", fontsize=7, fontweight="bold")
    b.set_yticks(range(3)[::-1], m); b.set_xlim(40, 92); b.set_xlabel("score (MOT17 test)")
    b.grid(axis="x", color=LINE, lw=0.35); b.set_axisbelow(True)
    panel(b, "b", "One tracker, three scores")
    # (c) Waymo rate reductions with intervals (forest)
    rows = [("Any-injury-reported crashes", 96, 87, 99), ("Airbag-deployment crashes", 91, 76, 98)]
    for i, (lab, pt, lo, hi) in enumerate(rows):
        y = 1 - i
        c.plot([lo, hi], [y, y], color=LIT, lw=1.3, solid_capstyle="butt")
        c.plot([pt], [y], "o", color=LIT, ms=4.5)
        c.text(60, y + 0.32, lab, fontsize=6.4, color=MUTED, va="bottom")
        c.text(pt, y - 0.34, f"{pt}%  ({lo}–{hi})", ha="center", fontsize=6.5, fontweight="bold", color=LIT_DEEP, va="top")
    c.set_yticks([]); c.spines["left"].set_visible(False); c.set_ylim(-0.95, 1.8)
    c.set_xlim(60, 102); c.set_xlabel("reduction vs human benchmark (%)")
    c.grid(axis="x", color=LINE, lw=0.35); c.set_axisbelow(True)
    c.text(60, 1.78, "vehicle-to-vehicle intersection crashes", fontsize=6.0, color=MUTED, va="bottom") if False else None
    panel(c, "c", "Fleet safety, 56.7 M miles")
    fig.text(0.075, 0.02, "Read: depth costs more to infer than to measure (a); HOTA exposes what MOTA hides (b);\nthe strongest safety record is measured where road death is rarest (c).", fontsize=6.4, color=OURS_INK, fontweight="bold")
    fig.savefig(os.path.join(OUT, "quant_results.pdf")); plt.close(fig)

if __name__ == "__main__":
    fig_quant = fig_results()
