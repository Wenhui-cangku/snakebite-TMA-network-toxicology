from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import networkx as nx
import numpy as np
import pandas as pd
from scipy.special import gammaln

try:
    sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
    from daimon_runtime import setup_plot
    setup_plot()
except ImportError:
    pass
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "svg.fonttype": "none",
    "axes.linewidth": 0.7,
})

REVISION = Path(__file__).resolve().parent
BASE = REVISION.parent.parent
OUT = REVISION / "figures_v3"
DATA = OUT / "data"
OUT.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

COLORS = {
    "navy": "#264653",
    "blue": "#457B9D",
    "teal": "#2A9D8F",
    "gold": "#E9C46A",
    "orange": "#F4A261",
    "red": "#C44E52",
    "purple": "#7A5195",
    "gray": "#8A939B",
    "light_gray": "#E9EDF0",
    "pale_blue": "#EAF1F5",
    "pale_teal": "#E8F4F1",
    "pale_gold": "#FBF4DF",
    "pale_red": "#F9ECEA",
    "direct_binding": "#4C72B0",
    "enzymatic_cleavage": "#C44E52",
    "inhibition": "#DD8452",
    "activation": "#55A868",
}

INPUTS = {
    "edges": BASE / "03_target_prediction" / "toxin_target_edges_audited.csv",
    "enrichment": BASE / "05_enrichment" / "reanalysis_v2" / "enrichment_summary_by_group.csv",
    "permutation": BASE / "05_enrichment" / "reanalysis_v2" / "permutation_results.csv",
    "loso": BASE / "05_enrichment" / "reanalysis_v2" / "loso_core_summary.csv",
    "sets": BASE / "05_enrichment" / "reanalysis_v2" / "sets_definition.csv",
    "network": BASE / "04_network" / "ppi_extended61_score700.tsv",
    "intersection": BASE / "04_network" / "intersection_sets.json",
    "geo_endothelium": BASE / "06_geo" / "limma_v2" / "GSE121297_RCaB_vs_Ctrl_limma_plainEB.csv",
    "geo_muscle": BASE / "06_geo" / "limma_v2" / "GSE248215_DR24h_vs_Ctrl_limma_plainEB.csv",
    "no_gc_strict": BASE / "05_enrichment" / "reanalysis_v2" / "enrichment_noGC_strict7.csv",
    "no_gc_union": BASE / "05_enrichment" / "reanalysis_v2" / "enrichment_noGC_union.csv",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_figure(fig: plt.Figure, number: int) -> None:
    for suffix in ("png", "svg"):
        fig.savefig(
            OUT / f"Figure_{number}.{suffix}",
            dpi=300 if suffix == "png" else None,
            bbox_inches="tight",
            pad_inches=0.06,
            facecolor="white",
        )
    plt.close(fig)


def add_box(ax, x, y, w, h, text, *, fc="white", ec=None, color="#17252A",
            fontsize=7.2, bold_first=False, radius=0.015, lw=1.0, zorder=3):
    ec = ec or COLORS["navy"]
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder,
    )
    ax.add_patch(patch)
    lines = text.split("\n")
    if bold_first and len(lines) > 1:
        ax.text(x + w / 2, y + h * 0.72, lines[0], ha="center", va="center",
                fontsize=fontsize + 0.3, fontweight="bold", color=color, zorder=zorder + 1)
        ax.text(x + w / 2, y + h * 0.34, "\n".join(lines[1:]), ha="center", va="center",
                fontsize=fontsize, color=color, linespacing=1.25, zorder=zorder + 1)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fontsize, color=color, linespacing=1.28, zorder=zorder + 1)
    return patch


def add_arrow(ax, start, end, *, color=None, style="solid", rad=0.0,
              mutation_scale=9, lw=1.25, zorder=2):
    color = color or COLORS["navy"]
    arrow = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=mutation_scale,
        linewidth=lw, color=color, linestyle=style,
        connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2, zorder=zorder,
    )
    ax.add_patch(arrow)
    return arrow


def scientific(value: float) -> str:
    if value == 0:
        return "0"
    exponent = math.floor(math.log10(abs(value)))
    mantissa = value / (10 ** exponent)
    return f"{mantissa:.1f}×10$^{{{exponent}}}$"


# ---------------------------------------------------------------------------
# Figure 1: study workflow
# ---------------------------------------------------------------------------
def figure_1():
    fig = plt.figure(figsize=(6.3, 6.35))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    ax.text(0.03, 0.97, "EVIDENCE INPUTS", fontsize=8, fontweight="bold",
            color=COLORS["blue"], va="top")
    top = [
        (0.03, "TOXIN LIBRARY\n63 sequences · 40 clusters\nCustom 90%-identity clustering\nRand index = 0.996"),
        (0.355, "DISEASE-GENE RESOURCE\n2,190 genes · 6 sources\nReproducible core\n1,042 genes"),
        (0.68, "MECHANISM CURATION\n33 primary-literature edges\n15 host targets\nProtein states preserved"),
    ]
    for x, text in top:
        add_box(ax, x, 0.74, 0.29, 0.19, text, fc=COLORS["pale_blue"],
                ec=COLORS["blue"], bold_first=True, fontsize=7.1)

    ax.text(0.03, 0.665, "CALIBRATION AND CONTEXT", fontsize=8, fontweight="bold",
            color=COLORS["teal"], va="top", zorder=6,
            bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    middle = [
        (0.03, "STRICT HOST-TARGET CORE\n10 curated targets within\nthe 1,042-gene core\nMechanism-typed map"),
        (0.355, "MATCHED ENRICHMENT\nG1–G7 backgrounds\n10,000 permutations\nSource + axis sensitivity"),
        (0.68, "BIOLOGICAL CONTEXT\nSTRING: 54 nodes / 321 edges\nlimma: 43 and 75 significant genes\nStructural models: context"),
    ]
    for x, text in middle:
        add_box(ax, x, 0.445, 0.29, 0.175, text, fc=COLORS["pale_teal"],
                ec=COLORS["teal"], bold_first=True, fontsize=7.0)
        add_arrow(ax, (x + 0.145, 0.735), (x + 0.145, 0.627), color=COLORS["gray"])

    ax.text(0.03, 0.36, "MECHANISTIC OUTPUT", fontsize=8, fontweight="bold",
            color=COLORS["navy"], va="top", zorder=6,
            bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    add_box(ax, 0.03, 0.105, 0.44, 0.205,
            "FACTOR X CONVERGENCE\nRecognition → activation → inhibition\n4 independent toxin entities\n6 literature-supported edges",
            fc=COLORS["navy"], ec=COLORS["navy"], color="white",
            bold_first=True, fontsize=7.5)
    add_box(ax, 0.53, 0.105, 0.44, 0.205,
            "TMA EXPERIMENTAL AGENDA\nVWF multimers + ADAMTS13 activity\nShear-dependent platelet adhesion\nComplement–endothelium assays",
            fc=COLORS["pale_gold"], ec="#B28A2E", bold_first=True, fontsize=7.25)
    add_arrow(ax, (0.175, 0.44), (0.22, 0.318), color=COLORS["teal"], rad=0.06)
    add_arrow(ax, (0.50, 0.44), (0.38, 0.318), color=COLORS["teal"], rad=-0.05)
    add_arrow(ax, (0.825, 0.44), (0.76, 0.318), color=COLORS["teal"], rad=-0.06)
    add_arrow(ax, (0.475, 0.207), (0.522, 0.207), color="#B28A2E", lw=1.4)
    ax.text(0.5, 0.035,
            "A source-resolved mechanism map links curated venom interactions to decisive vascular measurements.",
            ha="center", va="center", fontsize=7.1, color=COLORS["navy"])
    save_figure(fig, 1)


# ---------------------------------------------------------------------------
# Figure 2: mechanism-typed edges and factor X architecture
# ---------------------------------------------------------------------------
TOXIN_LABELS = {
    "T059": "RVV-X LC1", "T060": "RVV-X LC2", "T061": "RVV-X HC",
    "T027": "Daboxin P", "T041": "VRV-PL-VIIIa", "T034": "DrKIn-II",
    "T038": "RVV-V γ", "T037": "RVV-V α", "T028": "RVAF", "T029": "RVBF",
    "T026": "daborhagin-K", "T025": "russelysin†", "T052": "dabocetin α",
    "T033": "DrKIn-I", "T019": "BPTI-B1", "T042": "VR-1", "T036": "VR-1′",
}


def figure_2(edges: pd.DataFrame, strict_core: list[str]):
    primary = edges[edges["evidence_channel"] == "primary_literature"].copy()
    assert len(primary) == 33
    assert primary["target_symbol"].nunique() == 15
    assert primary["interaction_type"].value_counts().to_dict() == {
        "enzymatic_cleavage": 15, "inhibition": 10,
        "direct_binding": 6, "activation": 2,
    }
    assert primary["toxin_id"].nunique() == 17
    assert primary["independent_toxin_entity"].nunique() == 14

    fig = plt.figure(figsize=(6.3, 7.65))
    gs = fig.add_gridspec(2, 1, height_ratios=[5.25, 2.4], hspace=0.18,
                          left=0.02, right=0.98, top=0.97, bottom=0.105)
    ax = fig.add_subplot(gs[0])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("a  Mechanism-typed venom–host interactions", loc="left",
                 fontweight="bold", pad=4)

    toxin_order = [
        "T059", "T060", "T061", "T027", "T041", "T034", "T038", "T037",
        "T028", "T029", "T026", "T025", "T052", "T033", "T019", "T042", "T036",
    ]
    host_order = [
        "F10", "F9", "PROS1", "F11", "PLG", "PRSS1", "F5", "FGA", "FGB",
        "FN1", "COL4A1", "GP1BA", "PROC", "CTRB1", "KDR",
    ]
    assert set(toxin_order) == set(primary["toxin_id"])
    assert set(host_order) == set(primary["target_symbol"])
    toxin_y = {node: 0.94 - i * 0.88 / (len(toxin_order) - 1) for i, node in enumerate(toxin_order)}
    host_y = {node: 0.94 - i * 0.88 / (len(host_order) - 1) for i, node in enumerate(host_order)}

    pair_counts = {}
    for row in primary.itertuples():
        key = (row.toxin_id, row.target_symbol)
        pair_counts[key] = pair_counts.get(key, 0) + 1
        occurrence = pair_counts[key]
        rad = 0.07 * (1 if occurrence % 2 else -1)
        color = COLORS[row.interaction_type]
        arrow = FancyArrowPatch(
            (0.225, toxin_y[row.toxin_id]), (0.775, host_y[row.target_symbol]),
            arrowstyle="-|>", mutation_scale=5.5, linewidth=0.85,
            color=color, alpha=0.74, connectionstyle=f"arc3,rad={rad}",
            shrinkA=1, shrinkB=1, zorder=1,
        )
        ax.add_patch(arrow)

    for node in toxin_order:
        y = toxin_y[node]
        ax.scatter([0.205], [y], s=26, color=COLORS["navy"], edgecolor="white",
                   linewidth=0.5, zorder=3)
        ax.text(0.185, y, TOXIN_LABELS[node], ha="right", va="center", fontsize=6.25)
    for node in host_order:
        y = host_y[node]
        is_core = node in strict_core
        ax.scatter([0.795], [y], s=34, color=COLORS["teal"] if is_core else "white",
                   edgecolor=COLORS["teal"] if is_core else COLORS["gray"],
                   linewidth=0.8, zorder=3)
        ax.text(0.815, y, node, ha="left", va="center", fontsize=6.4,
                fontweight="bold" if is_core else "normal")
    ax.text(0.02, 0.995, "Toxin records", fontsize=6.5, color=COLORS["gray"], va="top")
    ax.text(0.98, 0.995, "Host targets", fontsize=6.5, color=COLORS["gray"],
            va="top", ha="right")

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis("off")
    ax2.set_title("b  Factor X: recognition–activation–inhibition", loc="left",
                  fontweight="bold", pad=4)
    ax2.text(0.99, 1.035, "4 independent toxin entities · 6 edges",
             transform=ax2.transAxes, ha="right", va="top", fontsize=7,
             color=COLORS["navy"], fontweight="bold")
    headers = [(0.03, "Toxin entity / component"), (0.36, "Target state"),
               (0.67, "Mechanism"), (0.90, "Edges")]
    for x, text in headers:
        ax2.text(x, 0.93, text, fontsize=6.7, fontweight="bold",
                 color=COLORS["gray"], ha="left", va="center")
    rows = [
        ("RVV-X complex — LC1", "FX zymogen (Gla)", "Recognition · direct binding", "direct_binding"),
        ("RVV-X complex — LC2", "FX zymogen (Gla)", "Recognition · direct binding", "direct_binding"),
        ("Daboxin P", "FX and FXa", "Recognition · direct binding", "direct_binding"),
        ("RVV-X complex — HC", "FX zymogen → FXa", "Activation · cleavage", "enzymatic_cleavage"),
        ("DrKIn-II", "FXa (active enzyme)", "Inhibition", "inhibition"),
        ("VRV-PL-VIIIa", "FXa (active enzyme)", "Inhibition", "inhibition"),
    ]
    for i, (entity, state, mechanism, kind) in enumerate(rows):
        y = 0.81 - i * 0.125
        if i % 2 == 0:
            ax2.add_patch(FancyBboxPatch((0.015, y - 0.052), 0.97, 0.105,
                                         boxstyle="round,pad=0.002,rounding_size=0.006",
                                         fc="#F5F7F8", ec="none", zorder=0))
        ax2.plot([0.022, 0.036], [y, y], color=COLORS[kind], lw=3, solid_capstyle="round")
        ax2.text(0.047, y, entity, fontsize=6.55, va="center")
        ax2.text(0.36, y, state, fontsize=6.55, va="center")
        ax2.text(0.67, y, mechanism, fontsize=6.55, va="center", color=COLORS[kind])
        ax2.text(0.925, y, "1", fontsize=6.8, va="center", ha="center", fontweight="bold")
    ax2.text(0.03, 0.035,
             "RVV-X subunits are one independent complex; FX and FXa remain distinct molecular states.",
             fontsize=6.5, color=COLORS["navy"], va="bottom")

    handles = [Line2D([0], [0], color=COLORS[k], lw=1.8,
                      label=k.replace("_", " ").replace("enzymatic cleavage", "Enzymatic cleavage").replace("direct binding", "Direct binding").replace("inhibition", "Inhibition").replace("activation", "Activation"))
               for k in ["enzymatic_cleavage", "inhibition", "direct_binding", "activation"]]
    handles += [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["teal"],
               markeredgecolor=COLORS["teal"], markersize=5, label="Strict-core target"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white",
               markeredgecolor=COLORS["gray"], markersize=5, label="Other curated target"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.033),
               ncol=3, frameon=False, handletextpad=0.5, columnspacing=1.0, fontsize=6.4)
    fig.text(0.02, 0.004,
             "† Duplicate accession retained in the 33-row audit; daborhagin-K is the independent entity.",
             fontsize=5.9, color=COLORS["gray"], va="bottom")
    save_figure(fig, 2)


# ---------------------------------------------------------------------------
# Figure 3: enrichment calibration and sensitivity
# ---------------------------------------------------------------------------
def log_comb(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def hypergeom_sf_matrix(K, M, n_vec, N):
    sf = np.zeros(K.shape, dtype=np.float64)
    log_cm = log_comb(M, N)
    for j in range(N + 1):
        with np.errstate(divide="ignore", invalid="ignore"):
            lp = log_comb(n_vec, j) + log_comb(M - n_vec, N - j) - log_cm
            pj = np.exp(lp)
        pj = np.where(np.isfinite(pj), pj, 0.0)
        sf += (K <= j) * pj[None, :]
    return np.minimum(sf, 1.0)


def load_gmt(path: Path):
    terms = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                terms[parts[0]] = {g.strip().upper() for g in parts[2:] if g.strip()}
    return terms


def regenerate_permutation_nulls(permutation_summary: pd.DataFrame):
    cache = DATA / "permutation_nulls_v3.npz"
    if cache.exists():
        loaded = np.load(cache)
        return {key: loaded[key] for key in loaded.files}

    gmt_dir = BASE / "05_enrichment" / "reanalysis_v2" / "gmt"
    flags = pd.read_csv(BASE / "05_enrichment" / "reanalysis_v2" / "core_evidence_flags.csv")
    bg = sorted(set(flags.loc[flags["in_core_doc"].astype(bool), "sym"].str.upper()))
    assert len(bg) == 1042
    bg_set = set(bg)
    index = {gene: i for i, gene in enumerate(bg)}
    strict10 = sorted(json.loads(INPUTS["intersection"].read_text(encoding="utf-8"))["core_strict"])
    union15 = sorted(set(strict10) | {"F2", "F3", "F7", "F8", "ALB"})
    groups = [
        ("G2_strictcore10", strict10),
        ("G4_union15", union15),
        ("G3_STRINGhubs5", ["F2", "F3", "F7", "F8", "ALB"]),
    ]

    names, sizes, members = [], [], []
    for library in ["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022"]:
        for name, genes in load_gmt(gmt_dir / f"{library}.gmt").items():
            overlap = genes & bg_set
            if len(overlap) >= 3:
                names.append(name)
                sizes.append(len(overlap))
                members.append(sorted(index[g] for g in overlap))
    sizes = np.asarray(sizes, dtype=float)
    coag_pattern = re.compile(r"coagulat|hemostasi|haemostasi|fibrin|platelet|thromb|blood clot|clotting", re.I)
    coag_mask = np.asarray([bool(coag_pattern.search(name)) for name in names])
    A = np.zeros((len(names), len(bg)), dtype=np.float32)
    for i, member in enumerate(members):
        A[i, member] = 1.0

    rng = np.random.default_rng(20261106)
    results = {}
    for group, genes in groups:
        N = len(genes)
        obs_vec = np.zeros(len(bg), dtype=np.float32)
        obs_vec[[index[g] for g in genes]] = 1.0
        p_obs = hypergeom_sf_matrix((A @ obs_vec)[None, :], len(bg), sizes, N)[0]
        min_obs = float(p_obs.min())
        min_coag_obs = float(p_obs[coag_mask].min())
        min_rand = np.empty(10000)
        min_coag_rand = np.empty(10000)
        done = 0
        while done < 10000:
            count = min(250, 10000 - done)
            perm_idx = np.argsort(rng.random((count, len(bg))), axis=1)[:, :N]
            X = np.zeros((count, len(bg)), dtype=np.float32)
            np.put_along_axis(X, perm_idx, 1.0, axis=1)
            p_values = hypergeom_sf_matrix(X @ A.T, len(bg), sizes, N)
            min_rand[done:done + count] = p_values.min(axis=1)
            min_coag_rand[done:done + count] = p_values[:, coag_mask].min(axis=1)
            done += count
        empirical = (1 + (min_rand <= min_obs).sum()) / 10001
        empirical_coag = (1 + (min_coag_rand <= min_coag_obs).sum()) / 10001
        archived = permutation_summary[permutation_summary["group"] == group].iloc[0]
        checks = [
            math.isclose(min_obs, archived["observed_min_p"], rel_tol=1e-10),
            math.isclose(min_coag_obs, archived["observed_min_coag_p"], rel_tol=1e-10),
            math.isclose(empirical, archived["permutation_empirical_p_global"], rel_tol=1e-10),
            math.isclose(empirical_coag, archived["permutation_empirical_p_coag"], rel_tol=1e-10),
            math.isclose(np.median(min_coag_rand), archived["random_coag_min_p_median"], rel_tol=1e-10),
        ]
        if not all(checks):
            raise RuntimeError(f"Permutation reproduction check failed for {group}: {checks}")
        results[f"{group}__global"] = min_rand
        results[f"{group}__coag"] = min_coag_rand
        print(f"Reproduced {group}: empirical coagulation P={empirical_coag:.6g}")
    np.savez_compressed(cache, **results)
    return results


def figure_3(enrichment: pd.DataFrame, permutation: pd.DataFrame,
             loso: pd.DataFrame, nulls: dict[str, np.ndarray]):
    fig, axes = plt.subplots(2, 2, figsize=(6.3, 6.8))
    fig.subplots_adjust(left=0.15, right=0.97, top=0.95, bottom=0.11,
                        wspace=0.52, hspace=0.68)

    ax = axes[0, 0]
    labels = ["G1 curated 15", "G2 strict 10", "G3 STRING 5", "G4 union 15",
              "G5 without ALB", "G6 −9 prior genes", "G7 −27 axis genes"]
    values = -np.log10(enrichment["top_p"].to_numpy())
    y = np.arange(7)[::-1]
    bar_colors = [COLORS["navy"], COLORS["teal"], COLORS["gold"], COLORS["teal"],
                  COLORS["blue"], COLORS["gray"], "#C5CBD0"]
    ax.barh(y, values, color=bar_colors, height=0.62)
    ax.set_yticks(y, labels)
    ax.set_xlabel("−log$_{10}$(leading hypergeometric P)")
    ax.set_title("a  Matched-background enrichment", loc="left", fontweight="bold")
    ax.set_xlim(0, 20.5)
    ax.grid(axis="x", color="#E4E8EA", lw=0.5)
    ax.set_axisbelow(True)
    for yi, value, count in zip(y, values, enrichment["n_BH<0.05"]):
        ax.text(value + 0.25, yi, f"{int(count)} BH terms", va="center", fontsize=6.2)
    ax.spines[["top", "right", "left"]].set_visible(False)

    ax = axes[0, 1]
    group_colors = {"G2_strictcore10": COLORS["teal"],
                    "G4_union15": COLORS["navy"],
                    "G3_STRINGhubs5": COLORS["orange"]}
    bins = np.linspace(0, 12, 61)
    for group, color in group_colors.items():
        values = -np.log10(nulls[f"{group}__coag"])
        hist, edges = np.histogram(values, bins=bins, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        ax.plot(centers, hist, color=color, lw=1.25,
                label=group.split("_")[0] + " null")
        ax.fill_between(centers, hist, color=color, alpha=0.10)
        archived = permutation[permutation["group"] == group].iloc[0]
        ax.axvline(-np.log10(archived["observed_min_coag_p"]), color=color,
                   lw=1.25, ls="--")
    ax.set_xlim(0, 12)
    ax.set_xlabel("−log$_{10}$(best coagulation P)")
    ax.set_ylabel("Density")
    ax.set_title("b  10,000-permutation nulls", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper right", fontsize=6.2)
    ax.text(0.98, 0.70,
            "Dashed: observed\nEmpirical P\nG2 = 1.0×10$^{-4}$\nG4 = 1.0×10$^{-4}$\nG3 = 2.0×10$^{-4}$",
            transform=ax.transAxes, ha="right", va="top", fontsize=6.2,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#D9DEE1", lw=0.5))
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1, 0]
    source_labels = ["None", "GeneCards", "Open Targets", "DISEASES", "DisGeNET", "CTD", "Prior axis"]
    x = np.arange(len(loso))
    ax.bar(x, loso["core_n"], color=[COLORS["navy"]] + [COLORS["blue"]] * 6,
           width=0.65, alpha=0.88)
    ax.set_xticks(x, source_labels, rotation=35, ha="right")
    ax.set_ylabel("Core genes (n)", color=COLORS["blue"])
    ax.tick_params(axis="y", colors=COLORS["blue"])
    ax.set_ylim(0, 1160)
    ax.set_title("c  Leave-one-source-out reconstruction", loc="left", fontweight="bold")
    ax2 = ax.twinx()
    ax2.plot(x, loso["strict_core_n"], color=COLORS["red"], marker="o", ms=4,
             lw=1.4)
    ax2.set_ylabel("Strict-core targets (n)", color=COLORS["red"])
    ax2.set_ylim(0, 11.5)
    ax2.set_yticks([0, 5, 10])
    ax2.tick_params(axis="y", colors=COLORS["red"])
    ax.spines["top"].set_visible(False); ax2.spines["top"].set_visible(False)
    ax.grid(axis="y", color="#E7EAEC", lw=0.5); ax.set_axisbelow(True)

    ax = axes[1, 1]
    g6 = enrichment[enrichment["group"] == "G6_strict7_noPrior9"].iloc[0]
    g7 = enrichment[enrichment["group"] == "G7_strict4_noForced27"].iloc[0]
    g2 = enrichment[enrichment["group"] == "G2_strictcore10"].iloc[0]
    stress_values = [-np.log10(g6["top_p"]), -np.log10(g7["top_p"])]
    ax.barh([1, 0], stress_values, color=[COLORS["gray"], "#C5CBD0"], height=0.46)
    ax.axvline(-np.log10(g2["top_p"]), color=COLORS["teal"], ls="--", lw=1.2,
               label="G2 strict-core reference")
    ax.set_yticks([1, 0], ["G6 (−9 prior)", "G7 (−27 axis)"], fontsize=6.5)
    ax.set_xlabel("−log$_{10}$(leading P)", labelpad=2)
    ax.set_xlim(0, 7.5)
    ax.set_title("d  Axis-gene stress tests", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper right", fontsize=6.0)
    ax.text(stress_values[0] + 0.12, 1, "2 BH terms", va="center", fontsize=6.4)
    ax.text(stress_values[1] + 0.12, 0, "0 BH terms", va="center", fontsize=6.4)
    ax.text(0.03, 0.035,
            "G6: Negative Regulation of Blood Coagulation\nG7: Blood Vessel Morphogenesis (not BH-significant)",
            transform=ax.transAxes, fontsize=5.7, va="bottom", color=COLORS["navy"])
    ax.grid(axis="x", color="#E7EAEC", lw=0.5); ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)

    save_figure(fig, 3)


# ---------------------------------------------------------------------------
# Figure 4: descriptive STRING-expanded network
# ---------------------------------------------------------------------------
def figure_4(network_path: Path, strict_core: list[str]):
    edges = pd.read_csv(network_path, sep="\t")
    graph = nx.Graph()
    for row in edges.itertuples():
        graph.add_edge(row.node1, row.node2, score=float(row.score))
    assert graph.number_of_nodes() == 54
    assert graph.number_of_edges() == 321
    hubs = {"F2", "F3", "F7", "F8", "ALB"}
    strict = set(strict_core)
    degrees = dict(graph.degree())

    fig = plt.figure(figsize=(6.3, 5.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.72, 1], left=0.02, right=0.98,
                          top=0.94, bottom=0.17, wspace=0.12)
    ax = fig.add_subplot(gs[0])
    ax.set_title("a  Functional-association context", loc="left", fontweight="bold")
    pos = nx.spring_layout(graph, seed=29, k=0.34, iterations=500, scale=1.0)
    nx.draw_networkx_edges(graph, pos, ax=ax, width=0.42, edge_color="#83919A", alpha=0.22)
    for category, nodes, color, edgecolor in [
        ("other", [n for n in graph if n not in strict and n not in hubs], "#D5DBDF", "#AAB4BA"),
        ("strict", [n for n in graph if n in strict], COLORS["teal"], "white"),
        ("hubs", [n for n in graph if n in hubs], COLORS["gold"], "#A98428"),
    ]:
        sizes = [18 + degrees[n] * 3.1 for n in nodes]
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_size=sizes,
                               node_color=color, edgecolors=edgecolor,
                               linewidths=0.55, ax=ax)

    labels = set(strict_core) | hubs | {"VWF"}
    label_offsets = {
        "F7": (-14, 9), "F5": (12, 10), "F10": (17, -1), "PROC": (17, -12),
        "F2": (15, 10), "F3": (15, -12), "F8": (14, 1), "F11": (15, 10),
        "PLG": (-18, 8), "FGA": (-15, -12), "ALB": (-17, 10), "VWF": (12, -12),
        "GP1BA": (13, -8), "KDR": (-12, -12), "COL4A1": (-12, -12), "PROS1": (14, 0),
    }
    for node in sorted(labels):
        ax.annotate(node, pos[node], xytext=label_offsets.get(node, (8, 8)),
                    textcoords="offset points", fontsize=5.7, ha="center", va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color="#9AA5AB", lw=0.35, shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.86))
    ax.margins(0.15)
    ax.axis("off")

    ax2 = fig.add_subplot(gs[1])
    top = sorted(degrees, key=degrees.get, reverse=True)[:14][::-1]
    values = [degrees[n] for n in top]
    colors = [COLORS["teal"] if n in strict else COLORS["gold"] if n in hubs else "#C5CED3" for n in top]
    ax2.barh(np.arange(len(top)), values, color=colors, height=0.66)
    ax2.set_yticks(np.arange(len(top)), top, fontsize=6.4)
    ax2.set_xlabel("Degree (descriptive)")
    ax2.set_title("b  Network degree", loc="left", fontweight="bold")
    ax2.grid(axis="x", color="#E7EAEC", lw=0.5); ax2.set_axisbelow(True)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.set_xlim(0, max(values) + 6)
    for i, value in enumerate(values):
        ax2.text(value + 0.5, i, str(value), va="center", fontsize=6.0)

    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["teal"],
               markersize=6, label="Strict-core target (10)"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["gold"],
               markeredgecolor="#A98428", markersize=6, label="STRING-specific hub (5)"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#D5DBDF",
               markeredgecolor="#AAB4BA", markersize=6, label="Other STRING node"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.072),
               frameon=False, ncol=3, fontsize=6.4, columnspacing=1.0)
    fig.text(0.5, 0.012,
             "54 nodes · 321 associations (score ≥ 0.7)\nAssociations may include text mining/co-expression; not physical toxin–host binding.",
             ha="center", va="bottom", fontsize=6.1, color=COLORS["gray"])
    save_figure(fig, 4)


# ---------------------------------------------------------------------------
# Figure 5: expression context
# ---------------------------------------------------------------------------
def plot_volcano(ax, df: pd.DataFrame, title: str, label_genes: list[str], offsets: dict):
    df = df.copy()
    df["neglogBH"] = -np.log10(df["adj.P.Val"].clip(lower=1e-300))
    significant = df["adj.P.Val"] < 0.05
    ax.scatter(df.loc[~significant, "logFC"], df.loc[~significant, "neglogBH"],
               s=4, c="#BFC6CA", alpha=0.38, linewidths=0, rasterized=True)
    ax.scatter(df.loc[significant, "logFC"], df.loc[significant, "neglogBH"],
               s=7, c=COLORS["teal"], alpha=0.72, linewidths=0, rasterized=True)
    ax.axhline(-np.log10(0.05), color=COLORS["gray"], lw=0.7, ls="--")
    ax.axvline(0, color="#D7DCE0", lw=0.6)
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel("log$_2$ fold change")
    ax.set_ylabel("−log$_{10}$(BH-adjusted P)")
    ax.text(0.03, 0.97, f"{int(significant.sum())} BH-significant genes",
            transform=ax.transAxes, va="top", fontsize=6.8, color=COLORS["navy"],
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))
    for gene in label_genes:
        match = df[df["gene"] == gene]
        if match.empty:
            continue
        row = match.iloc[0]
        color = COLORS["teal"] if row["adj.P.Val"] < 0.05 else "#A98428"
        ax.scatter([row["logFC"]], [row["neglogBH"]], s=22, facecolor=color,
                   edgecolor="white", linewidth=0.5, zorder=4)
        dx, dy = offsets.get(gene, (5, 5))
        ax.annotate(gene, (row["logFC"], row["neglogBH"]), xytext=(dx, dy),
                    textcoords="offset points", fontsize=6.2, color=color,
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.5, shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none", alpha=0.8))
    ax.spines[["top", "right"]].set_visible(False)


def plot_gene_bars(ax, df: pd.DataFrame, genes: list[str], title: str):
    selected = df.set_index("gene").loc[genes].copy()
    values = selected["logFC"].to_numpy()
    y = np.arange(len(genes))[::-1]
    colors = [COLORS["blue"] if q < 0.05 else COLORS["gold"] for q in selected["adj.P.Val"]]
    ax.barh(y, values, color=colors, height=0.58)
    ax.set_yticks(y, genes, fontsize=6.5)
    ax.set_xlabel("log$_2$ fold change")
    ax.set_title(title, loc="left", fontweight="bold")
    ax.grid(axis="x", color="#E7EAEC", lw=0.5); ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    span = max(abs(values)) * 1.40
    ax.set_xlim(min(0, min(values) * 1.38), max(0, max(values) * 1.36))
    if min(values) < 0:
        ax.axvline(0, color=COLORS["gray"], lw=0.65)
    for yi, value, q in zip(y, values, selected["adj.P.Val"]):
        label = f"BH={q:.2e}" if q < 0.05 else f"BH={q:.3f}"
        offset = span * 0.018
        label_x = value + offset if value >= 0 else offset
        ax.text(label_x, yi, label,
                va="center", ha="left", fontsize=5.9,
                color=COLORS["navy"] if q < 0.05 else "#80651F")


def figure_5(endothelium: pd.DataFrame, muscle: pd.DataFrame):
    assert int((endothelium["adj.P.Val"] < 0.05).sum()) == 43
    assert int((muscle["adj.P.Val"] < 0.05).sum()) == 75
    fig, axes = plt.subplots(2, 2, figsize=(6.3, 6.45))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.09,
                        wspace=0.40, hspace=0.52)
    endothelial_genes = ["SELE", "CXCL5", "CXCL3", "CXCL6", "ICAM1", "VCAM1"]
    muscle_genes = ["CCL2", "TIMP1", "HMOX1", "VEGFA", "SERPINE1"]
    plot_volcano(axes[0, 0], endothelium, "a  GSE121297 · endothelial snaclec model",
                 endothelial_genes,
                 {"SELE": (5, 5), "CXCL5": (5, 4), "CXCL3": (5, -11),
                  "CXCL6": (5, 4), "ICAM1": (5, -11), "VCAM1": (5, -12)})
    plot_volcano(axes[0, 1], muscle, "b  GSE248215 · inflammatory-myotoxic model",
                 muscle_genes,
                 {"CCL2": (5, 5), "TIMP1": (5, -10), "HMOX1": (5, 4),
                  "VEGFA": (5, -11), "SERPINE1": (5, 4)})
    plot_gene_bars(axes[1, 0], endothelium, endothelial_genes,
                   "c  Endothelial-activation context")
    plot_gene_bars(axes[1, 1], muscle, muscle_genes,
                   "d  Inflammatory-myotoxic context")
    fig.text(0.5, 0.018,
             "Classical limma empirical-Bayes analysis. Gold denotes VCAM1 or other effect-size observations with BH ≥ 0.05.",
             ha="center", fontsize=6.2, color=COLORS["gray"])
    save_figure(fig, 5)


# ---------------------------------------------------------------------------
# Figure 6: evidence-graded VICC-to-TMA hypothesis map
# ---------------------------------------------------------------------------
def figure_6():
    fig = plt.figure(figsize=(6.3, 7.2))
    ax = fig.add_axes([0, 0.055, 1, 0.945])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    for x, text in [(0.03, "MOLECULAR INITIATING INTERACTIONS"),
                    (0.365, "HOST-RESPONSE MODULES"),
                    (0.72, "CANDIDATE OUTCOMES")]:
        ax.text(x, 0.985, text, fontsize=7.1, fontweight="bold", color=COLORS["gray"], va="top")

    add_box(ax, 0.03, 0.745, 0.27, 0.17,
            "FACTOR X MODULE\nRVV-X recognition + activation\nDaboxin P binding\nPLA2 / Kunitz FXa inhibition",
            fc=COLORS["navy"], ec=COLORS["navy"], color="white", bold_first=True, fontsize=6.7)
    add_box(ax, 0.03, 0.545, 0.27, 0.145,
            "COAGULATION / FIBRINOLYSIS\nFV and FXI · protein C / plasmin\nFibrinogen and matrix substrates",
            fc=COLORS["pale_blue"], ec=COLORS["blue"], bold_first=True, fontsize=6.6)
    add_box(ax, 0.03, 0.355, 0.27, 0.14,
            "PLATELET / VASCULAR RECEPTORS\nDabocetin–GPIbα · Rusvikunin–GPIIb/IIIa\nVR-1–VEGFR2/KDR",
            fc=COLORS["pale_blue"], ec=COLORS["blue"], bold_first=True, fontsize=6.25)
    add_box(ax, 0.03, 0.185, 0.27, 0.115,
            "CROSS-SPECIES ANCHORS\nOther-viperid VWF/complement studies\nElapid / cobra venom factor mechanisms",
            fc=COLORS["pale_gold"], ec="#B28A2E", bold_first=True, fontsize=6.2)

    add_box(ax, 0.365, 0.715, 0.28, 0.20,
            "VICC CORE\nCoagulation-factor consumption\nFibrinolysis perturbation\nProcoagulant + anticoagulant activities",
            fc=COLORS["pale_teal"], ec=COLORS["teal"], bold_first=True, fontsize=6.9)
    add_box(ax, 0.365, 0.455, 0.28, 0.19,
            "PLATELET + ENDOTHELIAL RESPONSES\nReceptor modulation · VWF-string hypotheses\nSELE / ICAM1 · CCL2 / TIMP1 / SERPINE1\nExpression-context support",
            fc=COLORS["pale_teal"], ec=COLORS["teal"], bold_first=True, fontsize=6.35)
    add_box(ax, 0.365, 0.195, 0.28, 0.19,
            "COMPLEMENT BRANCHES\nDaboia in vivo C3 depletion\nPre-antivenom anaphylatoxin generation\nDirect Daboia toxin cleavage: untested",
            fc=COLORS["pale_gold"], ec="#B28A2E", bold_first=True, fontsize=6.35)

    add_box(ax, 0.72, 0.565, 0.25, 0.24,
            "THROMBOTIC MICROANGIOPATHY\nThrombocytopenia\nMicroangiopathic hemolytic anemia\nMicrovascular organ injury\n\nTMA-stratified testing required",
            fc=COLORS["pale_red"], ec=COLORS["red"], bold_first=True, fontsize=6.6)
    add_box(ax, 0.72, 0.235, 0.25, 0.23,
            "ACUTE KIDNEY INJURY\nParallel routes:\nHemodynamic disturbance\nInflammatory endothelial injury\nPigment / myotoxic injury\nDirect renal toxicity",
            fc="#F2F4F5", ec=COLORS["gray"], bold_first=True, fontsize=6.35)

    # Curated molecular interactions.
    add_arrow(ax, (0.302, 0.83), (0.36, 0.83), color=COLORS["navy"], style="solid")
    add_arrow(ax, (0.302, 0.62), (0.36, 0.76), color=COLORS["navy"], style="solid", rad=-0.08)
    add_arrow(ax, (0.302, 0.425), (0.36, 0.54), color=COLORS["navy"], style="solid", rad=-0.05)
    # Cross-species surrogate evidence.
    add_arrow(ax, (0.302, 0.242), (0.36, 0.28), color="#B28A2E", style="dashdot")
    add_arrow(ax, (0.302, 0.25), (0.36, 0.50), color="#B28A2E", style="dashdot", rad=-0.18)
    # Untested transition mechanisms.
    add_arrow(ax, (0.647, 0.805), (0.715, 0.71), color=COLORS["gray"], style="dotted", lw=1.5)
    add_arrow(ax, (0.647, 0.55), (0.715, 0.65), color=COLORS["gray"], style="dotted", lw=1.5)
    add_arrow(ax, (0.647, 0.29), (0.715, 0.60), color=COLORS["gray"], style="dotted", rad=0.10, lw=1.5)
    # Host-downstream AKI routes are annotation-based; the remaining transitions are untested.
    add_arrow(ax, (0.647, 0.74), (0.715, 0.42), color=COLORS["gray"], style="dashed", rad=0.12, lw=1.35)
    add_arrow(ax, (0.647, 0.49), (0.715, 0.39), color=COLORS["gray"], style="dotted", lw=1.35)

    add_box(ax, 0.03, 0.025, 0.94, 0.105,
            "DECISIVE MEASUREMENTS\nVWF antigen + multimers + ADAMTS13 activity   |   Endothelial VWF strings + shear-based platelet adhesion\nPurified-toxin complement cleavage + pathway-selective inhibition + endothelial deposition   |   TMA-stratified clinical sampling",
            fc="white", ec=COLORS["teal"], color=COLORS["navy"], bold_first=True, fontsize=6.25, lw=1.35)

    handles = [
        Line2D([0], [0], color=COLORS["navy"], lw=1.5, ls="solid", label="Primary literature"),
        Line2D([0], [0], color=COLORS["gray"], lw=1.5, ls="dashed", label="Annotation-based"),
        Line2D([0], [0], color="#B28A2E", lw=1.5, ls="dashdot", label="Cross-species surrogate"),
        Line2D([0], [0], color=COLORS["gray"], lw=1.5, ls="dotted", label="Untested link"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.004),
               ncol=4, frameon=False, fontsize=6.4, columnspacing=1.0)
    save_figure(fig, 6)


def main():
    edges = pd.read_csv(INPUTS["edges"])
    strict_core = json.loads(INPUTS["intersection"].read_text(encoding="utf-8"))["core_strict"]
    enrichment = pd.read_csv(INPUTS["enrichment"])
    permutation = pd.read_csv(INPUTS["permutation"])
    loso = pd.read_csv(INPUTS["loso"])
    endothelium = pd.read_csv(INPUTS["geo_endothelium"])
    muscle = pd.read_csv(INPUTS["geo_muscle"])

    figure_1()
    print("Figure 1 saved")
    figure_2(edges, strict_core)
    print("Figure 2 saved")
    nulls = regenerate_permutation_nulls(permutation)
    figure_3(enrichment, permutation, loso, nulls)
    print("Figure 3 saved")
    figure_4(INPUTS["network"], strict_core)
    print("Figure 4 saved")
    figure_5(endothelium, muscle)
    print("Figure 5 saved")
    figure_6()
    print("Figure 6 saved")

    primary = edges[edges["evidence_channel"] == "primary_literature"]
    audit = {
        "status": "PASS",
        "source_files": {name: {"path": path.resolve().relative_to(BASE.resolve()).as_posix(), "sha256": sha256(path)} for name, path in INPUTS.items()},
        "figure_1": {"toxin_sequences": 63, "toxin_clusters": 40, "disease_genes": 2190, "core_genes": 1042},
        "figure_2": {
            "primary_edges": len(primary),
            "host_targets": primary["target_symbol"].nunique(),
            "toxin_records": primary["toxin_id"].nunique(),
            "independent_toxin_entities": primary["independent_toxin_entity"].nunique(),
            "interaction_counts": primary["interaction_type"].value_counts().to_dict(),
            "factor_x_edges": int((primary["target_symbol"] == "F10").sum()),
            "factor_x_independent_entities": primary.loc[primary["target_symbol"] == "F10", "independent_toxin_entity"].nunique(),
        },
        "figure_3": {
            "permutation_seed": 20261106,
            "permutations_per_group": 10000,
            "archived_summary_reproduced": True,
            "groups": ["G2_strictcore10", "G4_union15", "G3_STRINGhubs5"],
        },
        "figure_4": {"nodes": 54, "edges": 321, "minimum_score": 0.7},
        "figure_5": {
            "GSE121297_BH_significant": int((endothelium["adj.P.Val"] < 0.05).sum()),
            "GSE248215_BH_significant": int((muscle["adj.P.Val"] < 0.05).sum()),
        },
        "outputs": [(OUT / f"Figure_{i}.{suffix}").resolve().relative_to(BASE.resolve()).as_posix() for i in range(1, 7) for suffix in ("png", "svg")],
    }
    (OUT / "figure_data_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output_directory": str(OUT), "figures": 6}, ensure_ascii=False))


if __name__ == "__main__":
    main()
