# -*- coding: utf-8 -*-
"""Figure 2a Venn diagram redraw (manual layout, labels kept clear of text)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = Path(__file__).resolve().parents[1] / "04_network" / "figure2a_venn.png"
fig, ax = plt.subplots(figsize=(8.2, 5.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 6.9); ax.axis("off"); ax.set_aspect("equal")

# large circle: disease core set; small circle: toxin targets (intersecting the large circle on the left)
big = Circle((6.1, 3.3), 2.55, fc="#1A56C4", ec="#12408F", alpha=0.30, lw=1.5)
small = Circle((3.15, 3.3), 1.05, fc="#7B1FA2", ec="#5A1480", alpha=0.35, lw=1.5)
ax.add_patch(big); ax.add_patch(small)
# intersection lens = exact geometric intersection of purple ∩ blue (fill = large circle clipped by the small circle)
inter = Circle((6.1, 3.3), 2.55, fc="#1E7E34", ec="none", alpha=0.55, lw=0)
inter.set_clip_path(Circle((3.15, 3.3), 1.05, transform=ax.transData))
ax.add_patch(inter)

ax.text(2.62, 3.3, "5", ha="center", va="center", fontsize=15, weight="bold", color="#5A1480")
ax.text(3.87, 3.3, "10", ha="center", va="center", fontsize=13, weight="bold", color="#0E3D1F")
ax.text(6.6, 3.3, "1032", ha="center", va="center", fontsize=15, weight="bold", color="#12408F")

# leader-line annotations (right label moved down to avoid the title)
ax.annotate("Toxin predicted targets (L1+L2)\nn = 15", xy=(2.75, 4.15), xytext=(0.7, 5.35),
            fontsize=9.5, color="#5A1480", weight="bold",
            arrowprops=dict(arrowstyle="-", color="#5A1480", lw=0.9))
ax.annotate("Disease gene core set (six sources)\nn = 1042", xy=(7.9, 5.1), xytext=(7.55, 5.30),
            fontsize=9.5, color="#12408F", weight="bold",
            arrowprops=dict(arrowstyle="-", color="#12408F", lw=0.9))
ax.annotate("Candidate core target set n = 10", xy=(3.9, 2.62), xytext=(5.6, 1.15),
            fontsize=9.5, color="#0E3D1F", weight="bold",
            arrowprops=dict(arrowstyle="-", color="#145A32", lw=0.9))

ax.text(5, 6.65, "Figure 2  Toxin targets ∩ disease gene core set", ha="center",
        fontsize=11.5, weight="bold")
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
