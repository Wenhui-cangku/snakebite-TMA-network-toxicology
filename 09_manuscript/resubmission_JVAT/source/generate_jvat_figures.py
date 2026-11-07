from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = SOURCE_DIR.parent
REVISION_DIR = PACKAGE_DIR.parent / "revision"
ORIGINAL_SCRIPT = REVISION_DIR / "generate_v3_figures.py"

spec = importlib.util.spec_from_file_location("v3_figures", ORIGINAL_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot import {ORIGINAL_SCRIPT}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.OUT = PACKAGE_DIR / "figures"
base.DATA = base.OUT / "data"
base.OUT.mkdir(parents=True, exist_ok=True)
base.DATA.mkdir(parents=True, exist_ok=True)

cache_source = REVISION_DIR / "figures_v3" / "data" / "permutation_nulls_v3.npz"
cache_target = base.DATA / cache_source.name
if not cache_target.exists():
    shutil.copy2(cache_source, cache_target)
if base.sha256(cache_source) != base.sha256(cache_target):
    raise RuntimeError("Permutation cache copy failed its SHA256 check")


def jvat_figure_1():
    """Rebuild the v3 workflow with the recomputed pairwise Rand index."""
    plt = base.plt
    colors = base.COLORS

    fig = plt.figure(figsize=(6.3, 6.35))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.03, 0.97, "EVIDENCE INPUTS", fontsize=8, fontweight="bold",
            color=colors["blue"], va="top")
    top = [
        (0.03, "TOXIN LIBRARY\n63 sequences · 40 clusters\nCustom 90%-identity clustering\nRand index = 0.996"),
        (0.355, "DISEASE-GENE RESOURCE\n2,190 genes · 6 sources\nReproducible core\n1,042 genes"),
        (0.68, "MECHANISM CURATION\n33 primary-literature edges\n15 host targets\nProtein states preserved"),
    ]
    for x, text in top:
        base.add_box(ax, x, 0.74, 0.29, 0.19, text, fc=colors["pale_blue"],
                     ec=colors["blue"], bold_first=True, fontsize=7.1)

    ax.text(0.03, 0.665, "CALIBRATION AND CONTEXT", fontsize=8, fontweight="bold",
            color=colors["teal"], va="top", zorder=6,
            bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    middle = [
        (0.03, "STRICT HOST-TARGET CORE\n10 curated targets within\nthe 1,042-gene core\nMechanism-typed map"),
        (0.355, "MATCHED ENRICHMENT\nG1–G7 backgrounds\n10,000 permutations\nSource + axis sensitivity"),
        (0.68, "BIOLOGICAL CONTEXT\nSTRING: 54 nodes / 321 edges\nlimma: 43 and 75 significant genes\nStructural models: context"),
    ]
    for x, text in middle:
        base.add_box(ax, x, 0.445, 0.29, 0.175, text, fc=colors["pale_teal"],
                     ec=colors["teal"], bold_first=True, fontsize=7.0)
        base.add_arrow(ax, (x + 0.145, 0.735), (x + 0.145, 0.627), color=colors["gray"])

    ax.text(0.03, 0.36, "MECHANISTIC OUTPUT", fontsize=8, fontweight="bold",
            color=colors["navy"], va="top", zorder=6,
            bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    base.add_box(ax, 0.03, 0.105, 0.44, 0.205,
                 "FACTOR X CONVERGENCE\nRecognition → activation → inhibition\n4 independent toxin entities\n6 literature-supported edges",
                 fc=colors["navy"], ec=colors["navy"], color="white",
                 bold_first=True, fontsize=7.5)
    base.add_box(ax, 0.53, 0.105, 0.44, 0.205,
                 "TMA EXPERIMENTAL AGENDA\nVWF multimers + ADAMTS13 activity\nShear-dependent platelet adhesion\nComplement–endothelium assays",
                 fc=colors["pale_gold"], ec="#B28A2E", bold_first=True, fontsize=7.25)
    base.add_arrow(ax, (0.175, 0.44), (0.22, 0.318), color=colors["teal"], rad=0.06)
    base.add_arrow(ax, (0.50, 0.44), (0.38, 0.318), color=colors["teal"], rad=-0.05)
    base.add_arrow(ax, (0.825, 0.44), (0.76, 0.318), color=colors["teal"], rad=-0.06)
    base.add_arrow(ax, (0.475, 0.207), (0.522, 0.207), color="#B28A2E", lw=1.4)
    ax.text(0.5, 0.035,
            "A source-resolved mechanism map links curated venom interactions to decisive vascular measurements.",
            ha="center", va="center", fontsize=7.1, color=colors["navy"])
    base.save_figure(fig, 1)


base.figure_1 = jvat_figure_1


def jvat_figure_3(enrichment, permutation, loso, nulls):
    np = base.np
    plt = base.plt
    colors = base.COLORS

    fig, axes = plt.subplots(2, 2, figsize=(6.3, 6.8))
    fig.subplots_adjust(left=0.22, right=0.97, top=0.95, bottom=0.11,
                        wspace=0.58, hspace=0.68)

    group_order = [
        "G2_strictcore10",
        "G3_STRINGhubs5",
        "G4_union15",
        "G5_union14_noALB",
        "G6_strict7_noPrior9",
        "G7_strict4_noForced27",
        "G1_L2curated15",
    ]
    by_group = enrichment.set_index("group").loc[group_order]
    labels = [
        "G2 PRIMARY · strict 10",
        "G3 sensitivity · STRING 5",
        "G4 sensitivity · union 15",
        "G5 sensitivity · without ALB",
        "G6 sensitivity · −9 prior",
        "G7 sensitivity · −27 axis",
        "G1 supporting · curated 15",
    ]
    values = -np.log10(by_group["top_p"].to_numpy())
    y = np.arange(7)[::-1]
    bar_colors = [colors["teal"], colors["gold"], colors["navy"],
                  colors["blue"], colors["gray"], "#C5CBD0", "#9AA5AB"]

    ax = axes[0, 0]
    ax.barh(y, values, color=bar_colors, height=0.62)
    ax.set_yticks(y, labels, fontsize=6.25)
    for tick in ax.get_yticklabels():
        if tick.get_text().startswith("G2 PRIMARY"):
            tick.set_fontweight("bold")
            tick.set_color(colors["navy"])
    ax.set_xlabel("−log$_{10}$(leading hypergeometric P)")
    ax.set_title("a  Strict-core primary analysis and sensitivities",
                 loc="left", fontweight="bold", fontsize=8.3)
    ax.set_xlim(0, 20.5)
    ax.grid(axis="x", color="#E4E8EA", lw=0.5)
    ax.set_axisbelow(True)
    for yi, value, count in zip(y, values, by_group["n_BH<0.05"]):
        ax.text(value + 0.25, yi, f"{int(count)} BH terms", va="center", fontsize=6.2)
    ax.spines[["top", "right", "left"]].set_visible(False)

    ax = axes[0, 1]
    group_styles = {
        "G2_strictcore10": (colors["teal"], "G2 primary null"),
        "G3_STRINGhubs5": (colors["orange"], "G3 sensitivity null"),
        "G4_union15": (colors["navy"], "G4 sensitivity null"),
    }
    bins = np.linspace(0, 12, 61)
    for group, (color, legend_label) in group_styles.items():
        values = -np.log10(nulls[f"{group}__coag"])
        hist, edges = np.histogram(values, bins=bins, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        ax.plot(centers, hist, color=color, lw=1.25, label=legend_label)
        ax.fill_between(centers, hist, color=color, alpha=0.10)
        archived = permutation[permutation["group"] == group].iloc[0]
        ax.axvline(-np.log10(archived["observed_min_coag_p"]), color=color,
                   lw=1.25, ls="--")
    ax.set_xlim(0, 12)
    ax.set_xlabel("−log$_{10}$(best coagulation P)")
    ax.set_ylabel("Density")
    ax.set_title("b  10,000-permutation nulls", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper right", fontsize=5.9)
    ax.text(0.98, 0.66,
            "Dashed: observed\nCoagulation empirical P\nG2 primary = 1.0×10$^{-4}$\nG4 sensitivity = 1.0×10$^{-4}$\nG3 sensitivity = 2.0×10$^{-4}$",
            transform=ax.transAxes, ha="right", va="top", fontsize=5.9,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#D9DEE1", lw=0.5))
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1, 0]
    source_labels = ["None", "GeneCards", "Open Targets", "DISEASES", "DisGeNET", "CTD", "Prior axis"]
    x = np.arange(len(loso))
    ax.bar(x, loso["core_n"], color=[colors["navy"]] + [colors["blue"]] * 6,
           width=0.65, alpha=0.88)
    ax.set_xticks(x, source_labels, rotation=35, ha="right")
    ax.set_ylabel("Core genes (n)", color=colors["blue"])
    ax.tick_params(axis="y", colors=colors["blue"])
    ax.set_ylim(0, 1160)
    ax.set_title("c  Source-sensitivity reconstruction", loc="left", fontweight="bold")
    ax2 = ax.twinx()
    ax2.plot(x, loso["strict_core_n"], color=colors["red"], marker="o", ms=4, lw=1.4)
    ax2.set_ylabel("Strict-core targets (n)", color=colors["red"])
    ax2.set_ylim(0, 11.5)
    ax2.set_yticks([0, 5, 10])
    ax2.tick_params(axis="y", colors=colors["red"])
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax.grid(axis="y", color="#E7EAEC", lw=0.5)
    ax.set_axisbelow(True)

    ax = axes[1, 1]
    g6 = enrichment[enrichment["group"] == "G6_strict7_noPrior9"].iloc[0]
    g7 = enrichment[enrichment["group"] == "G7_strict4_noForced27"].iloc[0]
    g2 = enrichment[enrichment["group"] == "G2_strictcore10"].iloc[0]
    stress_values = [-np.log10(g6["top_p"]), -np.log10(g7["top_p"])]
    ax.barh([1, 0], stress_values, color=[colors["gray"], "#C5CBD0"], height=0.46)
    ax.axvline(-np.log10(g2["top_p"]), color=colors["teal"], ls="--", lw=1.2,
               label="G2 primary reference")
    ax.set_yticks([1, 0], ["G6 (−9 prior)", "G7 (−27 axis)"], fontsize=6.5)
    ax.set_xlabel("−log$_{10}$(leading P)", labelpad=2)
    ax.set_xlim(0, 7.5)
    ax.set_title("d  Axis-gene sensitivity tests", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper right", fontsize=6.0)
    ax.text(stress_values[0] + 0.12, 1, "2 BH terms", va="center", fontsize=6.4)
    ax.text(stress_values[1] + 0.12, 0, "0 BH terms", va="center", fontsize=6.4)
    ax.text(0.03, 0.035,
            "G6: Negative Regulation of Blood Coagulation\nG7: Blood Vessel Morphogenesis (not BH-significant)",
            transform=ax.transAxes, fontsize=5.7, va="bottom", color=colors["navy"])
    ax.grid(axis="x", color="#E7EAEC", lw=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)

    base.save_figure(fig, 3)


base.figure_3 = jvat_figure_3
base.main()
