"""SAE ladder: who performs each part of the driving task at each level (J3016 allocation as summarised in
the paper's SAE scope table), with the commercial status given in that table (as of 13 August 2026).
No quantities are plotted; the figure encodes allocation and status only."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "figures", "charts") if os.path.isdir(os.path.join(ROOT, "figures", "charts")) else os.path.join(ROOT, "figures")

# level: (control, monitoring/OEDR, fallback, ODD, status text, status class)
S, H = "system", "human"
LV = [
    (0, ("Driver", H), ("Driver", H), ("Driver", H), ("none", None), "Saturated worldwide", "mass"),
    (1, ("System, 1 axis", S), ("Driver", H), ("Driver", H), ("bounded", S), "Mass-market commodity", "mass"),
    (2, ("System, 2 axes", S), ("Driver", H), ("Driver", H), ("bounded", S), "Only tier at mass-market scale", "mass"),
    (3, ("System", S), ("System", S), ("Driver on request", H), ("bounded", S), "Contracting; both German programmes withdrawn", "thin"),
    (4, ("System", S), ("System", S), ("System", S), ("bounded", S), "Only level in at-scale revenue service", "thin"),
    (5, ("System", S), ("System", S), ("System", S), ("unlimited", S), "None exists anywhere", "none"),
]
COLS = ["Sustained\ncontrol", "Monitoring\nthe scene (OEDR)", "Fallback", "Domain (ODD)"]
X0 = [0.55, 1.95, 3.35, 4.75]; CW = 1.32
STATUS = {"mass": (LIT, "white"), "thin": (LIT_MID, INK), "none": (OURS_BG, OURS_INK)}


def fig_ladder():
    fig = plt.figure(figsize=(W, 3.55)); ax = fig.add_axes([0.02, 0.02, 0.96, 0.82]); ax.axis("off")
    ax.set_xlim(0, 10.9); ax.set_ylim(-6.9, 0.9)
    for c, x in zip(COLS, X0):
        ax.text(x + CW / 2, 0.55, c, ha="center", va="center", fontsize=6.4, color=MUTED, linespacing=1.0)
    ax.text(6.55 + 2.0, 0.55, "Commercial status, August 2026", ha="center", va="center", fontsize=6.4, color=MUTED)
    for i, (lv, ctl, mon, fb, odd, stat, cls) in enumerate(LV):
        y = -i - 0.5 + 0.0
        ax.scatter([0.3], [y], s=250, color=LIT_DEEP if lv >= 3 else LIT, lw=0, zorder=3)
        ax.text(0.3, y - 0.02, str(lv), ha="center", va="center", fontsize=8, fontweight="bold", color="white", zorder=4)
        for x, (txt, who) in zip(X0, (ctl, mon, fb, odd)):
            if who is None:
                ax.add_patch(FancyBboxPatch((x + 0.02 * 0, y - 0.3), CW, 0.6, boxstyle="round,pad=0,rounding_size=0.08",
                                            fc="white", ec=LINE, lw=0.5, ls=(0, (2, 2))))
                ax.text(x + CW / 2, y, "no feature ODD", ha="center", va="center", fontsize=5.9, color=MUTED); continue
            sysb = who == S
            if txt == "unlimited":
                fc, ec, tc = OURS_BG, OURS, OURS_INK
            else:
                fc, ec, tc = (LIT_BG, LIT, LIT_DEEP) if sysb else ("#F1F3F6", GREY, MUTED)
            ax.add_patch(FancyBboxPatch((x, y - 0.3), CW, 0.6, boxstyle="round,pad=0,rounding_size=0.08", fc=fc, ec=ec, lw=0.6))
            ax.text(x + CW / 2, y, txt, ha="center", va="center", fontsize=6.3, color=tc, fontweight="bold" if sysb else "normal")
        fc, tc = STATUS[cls]
        ax.add_patch(FancyBboxPatch((6.25, y - 0.3), 4.55, 0.6, boxstyle="round,pad=0,rounding_size=0.08",
                                    fc=fc, ec="none" if cls != "none" else OURS, lw=0.6))
        ax.text(6.4, y, stat, ha="left", va="center", fontsize=6.3, color=tc, fontweight="bold" if cls == "none" else "normal")
    # what changes at each step: the paper's own reading of the transitions
    notes = [(2, 1, "L2→L3: OEDR moves to the system"), (3, 2, "L3→L4: fallback moves to the system"),
             (4, 3, "L4→L5: the ODD restriction is removed")]
    for r, k, t in notes:
        ax.annotate("", xy=(X0[k] + CW / 2, -r + 0.2), xytext=(X0[k] + CW / 2, -r + 0.7),
                    arrowprops=dict(arrowstyle="-", lw=0))
    yb = -6.25
    ax.text(0.0, yb, "What each step actually transfers:  L2→L3 the monitoring (OEDR);  L3→L4 the fallback;  L4→L5 the domain restriction, "
            "which changes the form of the safety argument rather than the capability.", fontsize=6.1, color=OURS_INK, fontweight="bold", va="top", wrap=True)
    # legend
    for q, (fc, ec, t) in enumerate([(LIT_BG, LIT, "performed by the system"), ("#F1F3F6", GREY, "performed by the human"), (OURS_BG, OURS, "unlimited domain")]):
        pass
    fig.text(0.02, 0.945, "Who performs what, level by level", fontsize=7.5, fontweight="bold", color=INK)
    fig.text(0.02, 0.905, "blue: the automated driving system; grey: the human driver", fontsize=6.3, color=MUTED)
    fig.savefig(os.path.join(OUT, "sae_ladder.pdf")); plt.close(fig)


if __name__ == "__main__":
    fig_ladder()
