"""Shared figure style: matches infostyle.tex (blue = others' work, amber = our analysis)."""
import os
import matplotlib as mpl
from matplotlib import font_manager as fm

_FD = os.path.expanduser("~/AppData/Local/Programs/MiKTeX/fonts/opentype/public/libertine")
for f in ():
    p = os.path.join(_FD, f)
    if os.path.exists(p):
        fm.fontManager.addfont(p)

LIT = "#2668B2"; LIT_DEEP = "#153A68"; LIT_BG = "#EBF3FC"; LIT_MID = "#A0C1E6"
OURS = "#C47C00"; OURS_BG = "#FEF5E2"; OURS_INK = "#8A5400"
INK = "#1C2634"; MUTED = "#606C7C"; LINE = "#C8D2E0"; GREY = "#B4BCC8"
PILLAR = {"Sense": LIT, "Plan": "#3E8E7E", "Act": "#7A5C9E"}   # three well-separated hues

mpl.rcParams.update({
    "font.family": ["Segoe UI", "Calibri", "DejaVu Sans"],
    "font.size": 7, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.5, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2.2, "ytick.major.size": 2.2,
    "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300,
    "figure.dpi": 150, "axes.unicode_minus": False,
})
W = 5.5  # inches: acmsmall text width


def panel(ax, letter, title, sub=None):
    ax.text(0, 1.13, f"({letter})", transform=ax.transAxes, fontsize=7.5, fontweight="bold", color=LIT_DEEP, va="bottom")
    ax.annotate(title, xy=(0, 1.13), xycoords="axes fraction", xytext=(15, 0), textcoords="offset points", fontsize=7.5, fontweight="bold", color=INK, va="bottom")
    if sub:
        ax.text(0, 1.04, sub, transform=ax.transAxes, fontsize=6.3, color=MUTED, va="bottom")
