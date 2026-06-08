#!/usr/bin/env python3
"""
Produce Fig. 1D and Fig. S5A analogs from DESeq2 results.
V3 → V2 gene ID mapping loaded from v3_to_v2_mapping.tsv.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from adjustText import adjust_text
import numpy as np
import os

# ── Constants ────────────────────────────────────────────────────────────────
PADJ_THRESH = 0.05
LFC_THRESH   = 1.0
TOP_N        = 20          # unlabelled significant genes to label
DIR = os.path.dirname(os.path.abspath(__file__))

# V2 gene IDs of interest → display names
V2_NAMED = {
    "B9J08_001458": "SCF1",
    "B9J08_003460": "SWI1",
    "B9J08_004109": "IFF4109",
    "B9J08_002818": "BCY1",
}

# ── Load V3→V2 mapping ───────────────────────────────────────────────────────
mapping = pd.read_csv(f"{DIR}/v3_to_v2_mapping.tsv", sep="\t")
v3_to_v2 = dict(zip(mapping["v3_locus"], mapping["v2_locus"]))

def load_deseq2(path):
    df = pd.read_csv(path, sep="\t", header=None,
                     names=["gene_id","basemean","log2fc","stderr","stat","pval","padj"])
    df = df.dropna(subset=["log2fc","padj"])
    df["v2_id"]    = df["gene_id"].map(v3_to_v2)
    df["gene_name"] = df["v2_id"].map(V2_NAMED)
    df["neglog10p"] = -np.log10(df["padj"].clip(lower=1e-300))
    return df

def colour(row, padj_t, lfc_t):
    if row["padj"] < padj_t and row["log2fc"] >  lfc_t: return "#d73027"
    if row["padj"] < padj_t and row["log2fc"] < -lfc_t: return "#4575b4"
    return "#cccccc"

def make_volcano(df, title, out_prefix):
    df = df.copy()
    df["colour"] = df.apply(lambda r: colour(r, PADJ_THRESH, LFC_THRESH), axis=1)

    n_up   = (df["colour"] == "#d73027").sum()
    n_down = (df["colour"] == "#4575b4").sum()

    fig, ax = plt.subplots(figsize=(7, 6.5))

    # All points
    ax.scatter(df["log2fc"], df["neglog10p"],
               c=df["colour"], s=14, alpha=0.65, linewidths=0, rasterized=True)

    # Named genes highlighted
    named = df[df["gene_name"].notna()]
    ax.scatter(named["log2fc"], named["neglog10p"],
               c=named["colour"], s=70,
               edgecolors="black", linewidths=0.9, zorder=6)

    # Threshold lines
    ax.axhline(-np.log10(PADJ_THRESH), color="#555555", lw=0.8, ls="--", alpha=0.6)
    ax.axvline( LFC_THRESH,  color="#555555", lw=0.8, ls="--", alpha=0.6)
    ax.axvline(-LFC_THRESH,  color="#555555", lw=0.8, ls="--", alpha=0.6)

    # Labels: named genes + top significant by padj
    sig = df[df["padj"] < PADJ_THRESH].copy()
    top_ids = set(sig.nsmallest(TOP_N, "padj")["gene_id"])
    top_ids |= set(named["gene_id"])
    label_df = df[df["gene_id"].isin(top_ids)].copy()

    texts = []
    for _, row in label_df.iterrows():
        name = row["gene_name"] if pd.notna(row.get("gene_name")) else row.get("v2_id", row["gene_id"])
        if pd.isna(name) or name == "nan":
            name = row["gene_id"]
        bold = pd.notna(row.get("gene_name"))
        t = ax.text(row["log2fc"], row["neglog10p"], name,
                    fontsize=7.5, ha="center", va="bottom",
                    fontweight="bold" if bold else "normal",
                    color="black")
        texts.append(t)

    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color="#888888", lw=0.5),
                expand=(1.3, 1.5), force_text=(0.3, 0.5))

    ax.set_xlabel("log₂ Fold Change", fontsize=12)
    ax.set_ylabel("−log₁₀(adjusted p-value)", fontsize=12)
    ax.set_title(f"{title}\n"
                 f"↑ Up: {n_up}   ↓ Down: {n_down}   "
                 f"(padj < {PADJ_THRESH}, |log₂FC| > {LFC_THRESH})",
                 fontsize=10.5)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()

    for ext in ("pdf","png"):
        out = f"{DIR}/{out_prefix}_volcano.{ext}"
        fig.savefig(out, dpi=180, bbox_inches="tight")
        print(f"Saved: {out}")
    plt.close()

    print(f"  Total sig: {(df['padj']<PADJ_THRESH).sum()}")
    print("  Top 10 downregulated (padj<0.05):")
    top_down = sig.sort_values("log2fc").head(10)[["gene_id","v2_id","gene_name","log2fc","padj"]]
    print(top_down.to_string(index=False))
    print("  Top 10 upregulated:")
    top_up = sig.sort_values("log2fc", ascending=False).head(10)[["gene_id","v2_id","gene_name","log2fc","padj"]]
    print(top_up.to_string(index=False))
    return df


if __name__ == "__main__":
    print("=" * 60)
    print("Fig. 1D analog: tnSWI1 vs AR0382")
    print("=" * 60)
    df1 = load_deseq2(f"{DIR}/deseq2_tnSWI1_vs_AR0382.tsv")
    make_volcano(df1, "tnSWI1 vs AR0382  (C. auris B8441 V3)", "fig1D_tnSWI1_vs_AR0382")

    print()
    print("=" * 60)
    print("Fig. S5A analog: AR0387 vs AR0382")
    print("=" * 60)
    df2 = load_deseq2(f"{DIR}/deseq2_AR0387_vs_AR0382.tsv")
    make_volcano(df2, "AR0387 vs AR0382  (C. auris B8441 V3)", "figS5A_AR0387_vs_AR0382")
