# -*- coding: utf-8 -*-
"""Graphical abstract for CBI submission (v46, 2026-10-02).
Repo-portable version: run from anywhere; output goes to 09_manuscript/submission/.
Horizontal single-panel summary derived from Fig.1 workflow (same colour language).
Output: Graphical_Abstract_CBI.png/.tif in 09_manuscript/submission/.
Elsevier spec: min 531 x 1328 px (h x w), legible at small size -> big fonts, few words.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / '09_manuscript/submission'
OUT.mkdir(parents=True, exist_ok=True)

# canvas: 13.28 x 5.31 in @300dpi -> 3984 x 1593 px (> 2x Elsevier minimum)
FIGW, FIGH, DPI = 13.28, 5.31, 300
fig = plt.figure(figsize=(FIGW, FIGH), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 132.8); ax.set_ylim(0, 53.1); ax.axis('off')

C_GRAY = ('#f4f6f8', '#8a9aa8')   # inputs
C_BLUE = ('#eaf3fb', '#2e6f9e')   # network
C_ORAN = ('#fdf3e7', '#d07a2d')   # evidence
C_GREN = ('#eef7ee', '#3e8e4f')   # output
C_RED  = '#b3372f'

def band(x0, x1, fc, label, lc):
    ax.add_patch(FancyBboxPatch((x0, 1.5), x1 - x0, 50.1,
                 boxstyle='round,pad=0.4,rounding_size=1.2',
                 fc=fc, ec='none', zorder=0))
    ax.text((x0 + x1) / 2, 49.2, label, ha='center', va='center',
            fontsize=13.5, fontweight='bold', color=lc, zorder=1)

def box(x, y, w, h, title, lines, fc, ec, tfs=13, lfs=11.5, tcolor='#1a1a1a',
        title_dy=None, zorder=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle='round,pad=0.3,rounding_size=1.0',
                 fc='white', ec=ec, lw=2.2, zorder=zorder))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle='round,pad=0.3,rounding_size=1.0',
                 fc=fc, ec='none', alpha=0.55, zorder=zorder - 0.1))
    cy = y + h / 2
    n = len(lines)
    if title_dy is None:
        title_dy = (h / 2) - 3.6
    ax.text(x + w / 2, y + h - 3.4 if n else cy, title, ha='center', va='center',
            fontsize=tfs, fontweight='bold', color=tcolor, zorder=zorder + 1)
    if n:
        for i, ln in enumerate(lines):
            ax.text(x + w / 2, y + h - 7.6 - i * 4.4, ln, ha='center', va='center',
                    fontsize=lfs, color='#333333', zorder=zorder + 1)

def arrow(x0, y0, x1, y1, color='#5a6a78', lw=3.4, zorder=2):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                 arrowstyle='-|>', mutation_scale=26, lw=lw,
                 color=color, zorder=zorder))

# ---------------- bands ----------------
band(2.5, 30.5, C_GRAY[0], 'INPUTS', C_GRAY[1])
band(33.5, 66.5, C_BLUE[0], 'MULTI-LAYER NETWORK', C_BLUE[1])
band(69.5, 103.5, C_ORAN[0], 'KEY EVIDENCE', C_ORAN[1])
band(106.5, 130.3, C_GREN[0], 'OUTPUT', C_GREN[1])

# ---------------- col 1: inputs ----------------
# snake glyph (subtle sine silhouette)
xs = np.linspace(7.2, 25.8, 200)
ys = 41.2 + 2.1 * np.sin((xs - 7.2) / 18.6 * 3.2 * np.pi)
ax.plot(xs, ys, color='#5d7a5d', lw=7, solid_capstyle='round', alpha=0.9, zorder=4)
ax.plot([25.4, 27.0], [ys[-1], ys[-1] + 0.6], color='#5d7a5d', lw=7,
        solid_capstyle='round', zorder=4)  # head
ax.plot([27.3, 28.6], [ys[-1] + 0.7, ys[-1] + 0.4], color=C_RED, lw=1.8, zorder=4)  # tongue
box(5.0, 19.5, 23.0, 18.0, "Russell's viper venom",
    ['Daboia russelii / D. siamensis', '63 toxins  ·  5 families',
     'UniProtKB + VenomZone'], *C_GRAY)
box(5.0, 3.5, 23.0, 13.0, 'TMA disease genes',
    ['6 sources  ·  2,190 total', '1,042 core genes'], *C_GRAY)

# ---------------- col 2: network ----------------
box(37.0, 13.0, 26.0, 28.0, 'Evidence-tiered integration',
    ['447 toxin–target edges', '(15 literature-curated direct)',
     '54-node PPI network', 'strict-core 10 ∩ hub 10',
     'MCC · Degree · EPC'], *C_BLUE)

# ---------------- col 3: key evidence ----------------
# highlight card (coagulation axis)
ax.add_patch(FancyBboxPatch((72.0, 33.0), 28.0, 11.5,
             boxstyle='round,pad=0.3,rounding_size=1.0',
             fc='#fdecea', ec=C_RED, lw=2.6, zorder=3))
ax.text(86.0, 41.6, 'Coagulation / fibrinolysis axis', ha='center', va='center',
        fontsize=13, fontweight='bold', color=C_RED, zorder=4)
ax.text(86.0, 37.0, 'KEGG:04610   $P$ = 3.9 × 10$^{-18}$', ha='center', va='center',
        fontsize=13.5, fontweight='bold', color='#1a1a1a', zorder=4)
box(72.0, 19.2, 28.0, 12.8, 'Docking on 3 platforms + NMA',
    ['RVV-X → factor-X activation', 'svVEGF–VEGFR2 interaction'], *C_ORAN, tfs=12, lfs=10.5)
box(72.0, 5.0, 28.0, 12.8, 'Cross-species transcriptomes',
    ['endothelial 2nd pillar; complement', 'not supported (honest negative)'],
    *C_ORAN, tfs=11.5, lfs=10.5)

# ---------------- col 4: output ----------------
box(109.0, 26.5, 19.0, 17.5, 'Mechanistic model',
    ['venom toxins →', 'coagulation/platelet', 'axis → TMA'], *C_GREN, tfs=12.5, lfs=11)
box(109.0, 6.0, 19.0, 17.0, 'Repurposing leads',
    ['batimastat', 'marimastat', 'varespladib'], *C_GREN, tfs=12.5, lfs=11.5)

# ---------------- arrows ----------------
arrow(28.3, 27.5, 36.4, 27.0)                 # toxins -> network
arrow(28.3, 10.2, 36.4, 24.0)                 # genes  -> network
arrow(63.3, 26.5, 70.2, 26.5)                 # network -> evidence
arrow(100.3, 36.5, 108.5, 35.0)               # evidence -> model
arrow(100.3, 13.0, 108.5, 14.5)               # evidence -> leads

# footer
ax.text(66.4, 0.2, 'Open and reproducible pipeline — code & data archived on GitHub + Zenodo',
        ha='center', va='bottom', fontsize=10.5, color='#6a7885', style='italic')

png = OUT / 'Graphical_Abstract_CBI.png'
tif = OUT / 'Graphical_Abstract_CBI.tif'
fig.savefig(png, dpi=DPI, facecolor='white')
fig.savefig(tif, dpi=DPI, facecolor='white', pil_kwargs={'compression': 'tiff_lzw'})
plt.close(fig)

from PIL import Image
im = Image.open(png)
print('saved:', png)
print('pixel size (w x h):', im.size, '-> Elsevier min (h x w) = 531 x 1328 OK:',
      im.size[1] >= 531 and im.size[0] >= 1328)
