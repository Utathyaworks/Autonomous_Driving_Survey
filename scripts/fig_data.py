"""Data-section charts. Every number below is transcribed from Tables 1-4 of the paper
(road networks, benchmark overview, DCR) and recomputed here; none comes from elsewhere."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")

# ---- Table: road networks (1000 km, expressway 1000 km, % paved, urban km/h, commuters M/day u,r,e)
road = {
 "USA":      (6685, 77.6, 67.5, 24, (120, 48, 72)),
 "China":    (5196, 177.3, 94.2, 28, (320, 192, 128)),
 "Germany":  (645, 13.2, 99.5, 22, (34, 11, 12)),
 "Japan":    (1218, 9.7, 97.9, 18, (51, 11, 11)),
 "India":    (6371, 4.1, 55.1, 16, (210, 189, 21)),
 "UK":       (418, 3.7, 99.9, 15, (33, 7, 7)),
 "France":   (1093, 12.2, 99.4, 18, (30, 10, 11)),
 "Brazil":   (1757, 2.5, 12.9, 20, (62, 31, 10)),
 "Canada":   (1042, 17.0, 39.9, 22, (16, 5, 6)),
 "S. Korea": (114, 5.1, 99.9, 20, (28, 5, 5)),
}
# ---- Table: DCR inputs (annotated frames, thousands)
frames = {"S. Korea": 230, "Germany": 125, "USA": 641, "China": 281, "France": 25,
          "India": 94, "Canada": 7, "UK": 1, "Japan": 0, "Brazil": 0}
dcr = {c: frames[c] * 1000 / (road[c][0] / 1000 * 1000) if False else frames[c] * 1000 / road[c][0] for c in road}
# DCR = annotated frames / (road km / 1000) = frames*1000 / (road_thousand_km*1000/1000) -> frames/(thousand km)
# frames in thousands -> frames = f*1e3 ; road in thousand km -> per 1000 km = frames / road_thousand_km
dcr = {c: frames[c] * 1e3 / road[c][0] for c in road}
users = {c: sum(road[c][4]) for c in road}
HI = {"India", "China", "Brazil", "Japan"}      # the inversion the text argues about


def fig_inversion():
    order = sorted(road, key=lambda c: -users[c])
    fig = plt.figure(figsize=(W, 2.55))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.10, left=0.115, right=0.985, top=0.80, bottom=0.29)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1], sharey=a)
    y = np.arange(len(order))[::-1]
    # (a) demand
    a.barh(y, [users[c] for c in order], color=[LIT if c in HI else LIT_MID for c in order], height=0.62, lw=0)
    for yi, c in zip(y, order):
        a.text(users[c] + 8, yi, f"{users[c]:.0f}", va="center", fontsize=6.5, color=INK if c in HI else MUTED)
    a.set_yticks(y, order); a.set_xlim(0, 760); a.invert_xaxis() if False else None
    a.set_xlabel("daily road users (millions per day)")
    for t in a.get_yticklabels():
        if t.get_text() in HI: t.set_fontweight("bold"); t.set_color(INK)
    panel(a, "a", "Who drives", "road users per day, urban + rural + expressway")
    # (b) coverage, log scale; zeros drawn as a marker on the axis
    pos = [dcr[c] for c in order]
    for yi, c in zip(y, order):
        v = dcr[c]
        col = OURS if c in HI else "#E3B866"
        if v > 0:
            b.barh(yi, v, color=col, height=0.62, lw=0)
            lab = f"{v:,.0f}" if v >= 2 else "<2"
            b.text(v * 1.18, yi, lab, va="center", fontsize=6.5, color=OURS_INK if c in HI else MUTED)
        else:
            b.plot([1], [yi], marker="x", ms=3.6, mew=0.9, color=OURS)
            b.text(1.35, yi, "0 (none public)", va="center", fontsize=6.5, color=OURS_INK)
    b.set_xscale("log"); b.set_xlim(1, 6000)
    b.set_xlabel("annotated frames per 1,000 road-km (DCR, log scale)")
    plt.setp(b.get_yticklabels(), visible=False); b.tick_params(axis="y", length=0)
    panel(b, "b", "Who is annotated", "Dataset Coverage Ratio, Eq. (1)")
    for ax in (a, b):
        ax.grid(axis="x", color=LINE, lw=0.35); ax.set_axisbelow(True); ax.spines["left"].set_visible(False) if ax is b else None
    # finding callout
    fig.text(0.115, 0.015, "Finding: India carries 420 M road users a day on 15 annotated frames per 1,000 km;\n"
             "Japan and Brazil have no public annotated data.", fontsize=6.6, color=OURS_INK, fontweight="bold")
    fig.savefig(os.path.join(OUT, "data_inversion.pdf")); plt.close(fig)


def fig_roads():
    keys = [("Total roads", 0, "thousand km", False), ("Expressways", 1, "thousand km", False),
            ("Paved share", 2, "% of network", False), ("Urban speed", 3, "km/h", False)]
    fig, axs = plt.subplots(1, 4, figsize=(W, 2.45), sharey=True)
    order = sorted(road, key=lambda c: -road[c][0])
    y = np.arange(len(order))[::-1]
    for k, (ax, (t, i, u, _)) in enumerate(zip(axs, keys)):
        vals = [road[c][i] for c in order]
        ax.barh(y, vals, color=[LIT if c in HI else LIT_MID for c in order], height=0.62, lw=0)
        for yi, v, c in zip(y, vals, order):
            ax.text(v + max(vals) * 0.02, yi, f"{v:,.1f}" if i in (1, 2) else f"{v:,.0f}", va="center", fontsize=6, color=INK if c in HI else MUTED)
        ax.set_xlim(0, max(vals) * 1.28)
        ax.set_xlabel(u, fontsize=6.5)
        ax.grid(axis="x", color=LINE, lw=0.35); ax.set_axisbelow(True)
        panel(ax, "abcd"[k], t.split()[0] if False else t)
        ax.title.set_text("")
        if k: ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    axs[0].set_yticks(y, order)
    for t in axs[0].get_yticklabels():
        if t.get_text() in HI: t.set_fontweight("bold"); t.set_color(INK)
    fig.subplots_adjust(left=0.10, right=0.995, top=0.82, bottom=0.17, wspace=0.12)
    fig.savefig(os.path.join(OUT, "data_roads.pdf")); plt.close(fig)


# ---- benchmark landscape: (name, year, size, unit, pillar, global-south)
D = [
 ("CamVid", 2009, 701, "i", "Sense", 0), ("KITTI", 2012, 15000, "i", "Sense", 0), ("KAIST-Multi", 2015, 95000, "i", "Sense", 0),
 ("Cityscapes", 2016, 5000, "i", "Sense", 0), ("SYNTHIA", 2016, 9400, "i", "Sense", 0), ("Mapillary", 2017, 25000, "i", "Sense", 0),
 ("ApolloScape", 2018, 140000, "i", "Sense", 0), ("NightOwls", 2018, 279000, "i", "Sense", 0), ("WildDash", 2018, 4256, "i", "Sense", 0),
 ("IDD", 2019, 10004, "i", "Sense", 1), ("SemanticKITTI", 2019, 43551, "i", "Sense", 0), ("Waymo Open", 2019, 390000, "i", "Sense", 0),
 ("Dark Zurich", 2019, 8779, "i", "Sense", 0), ("RUGD", 2019, 7545, "i", "Sense", 0), ("D²-City", 2019, 700000, "i", "Sense", 0),
 ("A2D2", 2020, 41277, "i", "Sense", 0), ("CADCD", 2020, 7000, "i", "Sense", 0), ("DAWN", 2020, 1029, "i", "Sense", 0),
 ("ONCE", 2021, 1000000, "i", "Sense", 0), ("ACDC", 2021, 4006, "i", "Sense", 0), ("RELLIS", 2021, 13556, "i", "Sense", 0),
 ("PandaSet", 2021, 16000, "i", "Sense", 0), ("SHIFT", 2022, 2500000, "i", "Sense", 0), ("DAIR-V2X", 2022, 71254, "i", "Sense", 0),
 ("VoD", 2022, 8693, "i", "Sense", 0), ("K-Radar", 2022, 35000, "i", "Sense", 0), ("RADIal", 2022, 25000, "i", "Sense", 0),
 ("Rope3D", 2022, 50000, "i", "Sense", 0), ("SAAD", 2022, 5000, "i", "Sense", 1), ("IDD-3D", 2023, 12000, "i", "Sense", 1),
 ("DriveIndia", 2025, 66986, "i", "Sense", 1),
 ("OPV2V", 2022, 11464, "s", "Sense", 0),
 ("Argoverse", 2019, 333000, "s", "Plan", 0), ("INTERACTION", 2019, 100000, "s", "Plan", 0), ("Lyft L5", 2020, 170000, "s", "Plan", 0),
 ("WOMD", 2021, 103000, "s", "Plan", 0), ("Argoverse 2", 2023, 250000, "s", "Plan", 0), ("NAVSIM", 2024, 100000, "s", "Act", 0),
]
LAB = {  # name -> (dx points, dy points, ha)
 "Waymo Open": (5, 1, "left"), "ONCE": (-4, 3, "right"), "SHIFT": (-4, 3, "right"), "D²-City": (4, 2, "left"),
 "NightOwls": (-4, 3, "right"), "ApolloScape": (-4, -7, "right"), "Argoverse": (6, -7, "left"), "Argoverse 2": (-4, 3, "right"),
 "Lyft L5": (4, 2, "left"), "IDD": (0, -9, "center"), "SAAD": (4, -3, "left"), "IDD-3D": (4, -2, "left"),
 "DriveIndia": (-4, 3, "right"), "CamVid": (4, -2, "left"), "DAWN": (4, -2, "left"), "KITTI": (-3, -8, "left"),
 "Cityscapes": (-2, -9, "center"), "NAVSIM": (4, 3, "left"), "KAIST-Multi": (-4, 3, "right"),
}


def fig_landscape():
    fig, ax = plt.subplots(figsize=(W, 3.0))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.86, bottom=0.12)
    jitter = {}
    for n, yr, s, u, p, gs in D:
        mk = "o" if u == "i" else "s"
        ax.scatter(yr, s, s=17 if not gs else 26, marker=mk, color=PILLAR[p], alpha=0.95 if gs else 0.62,
                   edgecolor=OURS if gs else "white", linewidth=1.1 if gs else 0.4, zorder=3)
        if n in LAB:
            dx, dy, ha = LAB[n]
            ax.annotate(n, (yr, s), xytext=(dx, dy), textcoords="offset points", fontsize=6.2, ha=ha,
                        color=OURS_INK if gs else INK, fontweight="bold" if gs else "normal", zorder=4)
    ax.set_yscale("log"); ax.set_ylim(400, 6e6); ax.set_xlim(2008.5, 2025.8)
    ax.set_yticks([1e3, 1e4, 1e5, 1e6]); ax.set_yticklabels(["1k", "10k", "100k", "1M"])
    ax.set_ylabel("annotated frames, images or scenarios (log)")
    ax.grid(axis="y", color=LINE, lw=0.35); ax.set_axisbelow(True)
    # shaded reference band: where the four Global-South datasets sit
    ax.axhspan(400, 13000, xmin=0, xmax=1, color=OURS_BG, zorder=0)
    ax.text(2008.7, 440, "up to 13k annotated units", fontsize=6, color=OURS_INK, va="bottom")
    h = [Line2D([], [], marker="o", ls="", color=PILLAR["Sense"], label="Sense", ms=4.2),
         Line2D([], [], marker="o", ls="", color=PILLAR["Plan"], label="Plan", ms=4.2),
         Line2D([], [], marker="o", ls="", color=PILLAR["Act"], label="Act", ms=4.2),
         Line2D([], [], marker="s", ls="", color=GREY, label="counted in scenarios", ms=4),
         Line2D([], [], marker="o", ls="", color=PILLAR["Sense"], mec=OURS, mew=1.1, label="South Asia / Africa", ms=5)]
    ax.legend(handles=h, ncol=5, loc="lower left", bbox_to_anchor=(0.0, 1.0), frameon=False, fontsize=6.3,
              handletextpad=0.2, columnspacing=1.2, borderaxespad=0.1)
    fig.savefig(os.path.join(OUT, "data_landscape.pdf")); plt.close(fig)
    return len(D)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("DCR check:", {c: round(v) for c, v in dcr.items()})
    print("users:", users)
    fig_inversion(); fig_roads(); n = fig_landscape(); print("datasets plotted:", n)
