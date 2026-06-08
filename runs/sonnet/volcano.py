#!/usr/bin/env python3
"""
Fig. 1D analog: volcano plots for
  1. tnSWI1 vs AR0382  (replicates paper Fig. 1D)
  2. AR0387 vs AR0382  (replicates paper Fig. S5A)

Input: DESeq2 output tabular files downloaded from Galaxy
  Columns (1-indexed, from deg_annotate output):
  GeneID | Base mean | log2(FC) | StdErr | Wald-Stats | P-value | P-adj |
  Chromosome | Start | End | Strand | Feature | Gene name

Usage:
  python volcano.py <deseq2_tsv> <title> <out_prefix>
  # e.g.
  python volcano.py tnswi1_vs_ar0382.tsv "tnSWI1 vs AR0382" tnswi1
"""

import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np

# ── V3 → V2 locus tag mapping (trivial: 5-digit → 6-digit zero-padding) ──────
# B9J08_01458 → B9J08_001458  (just add a leading zero after the underscore)
# Key genes of interest (V3 ID → paper name)
GENES_OF_INTEREST = {
    "B9J08_01458": "SCF1",
    "B9J08_04109": "IFF4109",
    "B9J08_03460": "SWI1",
    "B9J08_02818": "BCY1",
}

def v3_to_v2(gene_id):
    """Convert 5-digit V3 locus tag to 6-digit V2 format."""
    if gene_id.startswith("B9J08_") and len(gene_id) == 11:
        num = gene_id.split("_")[1]
        return f"B9J08_0{num}"
    return gene_id


def load_deseq2(path):
    df = pd.read_csv(path, sep="\t", comment="#")
    # Normalise column names (DESeq2 / deg_annotate output varies slightly)
    df.columns = [c.strip() for c in df.columns]
    # Expected: GeneID, Base mean, log2(FC), StdErr, Wald-Stats, P-value, P-adj, ...
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if "geneid" in lc or lc == "geneid":
            col_map[c] = "gene_id"
        elif "log2" in lc and "fc" in lc:
            col_map[c] = "log2fc"
        elif "p-adj" in lc or "padj" in lc:
            col_map[c] = "padj"
        elif "p-value" in lc or "pvalue" in lc:
            col_map[c] = "pvalue"
        elif "base mean" in lc or "basemean" in lc:
            col_map[c] = "basemean"
    df = df.rename(columns=col_map)
    df = df.dropna(subset=["log2fc", "padj"])
    df["neglog10padj"] = -np.log10(df["padj"].clip(lower=1e-300))
    df["v2_id"] = df["gene_id"].apply(v3_to_v2)
    df["label"] = df["gene_id"].map(GENES_OF_INTEREST).fillna("")
    return df


def volcano(df, title, out_prefix, padj_thresh=0.05, lfc_thresh=1.0, top_n=20):
    fig, ax = plt.subplots(figsize=(8, 7))

    # Colour coding
    def colour(row):
        if row["padj"] < padj_thresh and row["log2fc"] > lfc_thresh:
            return "#d73027"   # up
        if row["padj"] < padj_thresh and row["log2fc"] < -lfc_thresh:
            return "#4575b4"   # down
        return "#aaaaaa"       # ns

    df["colour"] = df.apply(colour, axis=1)

    # Background points
    ax.scatter(df["log2fc"], df["neglog10padj"],
               c=df["colour"], s=12, alpha=0.6, linewidths=0, rasterized=True)

    # Highlight genes of interest
    highlight = df[df["label"] != ""]
    ax.scatter(highlight["log2fc"], highlight["neglog10padj"],
               c=highlight["colour"], s=60, edgecolors="black", linewidths=0.8,
               zorder=5)

    # Threshold lines
    ax.axhline(-np.log10(padj_thresh), color="black", lw=0.8, ls="--", alpha=0.5)
    ax.axvline( lfc_thresh,  color="black", lw=0.8, ls="--", alpha=0.5)
    ax.axvline(-lfc_thresh,  color="black", lw=0.8, ls="--", alpha=0.5)

    # Label top significant genes + genes of interest
    sig = df[df["padj"] < padj_thresh].copy()
    top_genes = set(
        sig.nsmallest(top_n, "padj")["gene_id"].tolist() +
        list(GENES_OF_INTEREST.keys())
    )
    label_df = df[df["gene_id"].isin(top_genes) & (df["label"] != "" )]
    # Also label top genes without a fixed name
    label_df2 = sig.nsmallest(top_n, "padj")

    texts = []
    for _, row in pd.concat([label_df, label_df2]).drop_duplicates("gene_id").iterrows():
        name = row["label"] if row["label"] else row["v2_id"]
        t = ax.text(row["log2fc"], row["neglog10padj"], name,
                    fontsize=7, ha="center", va="bottom",
                    fontweight="bold" if row["label"] else "normal")
        texts.append(t)

    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color="gray", lw=0.5),
                expand=(1.2, 1.4))

    # Counts in legend
    n_up   = (df["colour"] == "#d73027").sum()
    n_down = (df["colour"] == "#4575b4").sum()
    ax.set_xlabel("log₂ Fold Change", fontsize=12)
    ax.set_ylabel("−log₁₀(adjusted p-value)", fontsize=12)
    ax.set_title(f"{title}\nUp: {n_up}   Down: {n_down}  (padj<{padj_thresh}, |LFC|>{lfc_thresh})",
                 fontsize=11)

    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    pdf_path = f"{out_prefix}_volcano.pdf"
    png_path = f"{out_prefix}_volcano.png"
    fig.savefig(pdf_path, dpi=150, bbox_inches="tight")
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {pdf_path}  {png_path}")
    print(f"  Up={n_up}  Down={n_down}  Total sig={(df['padj']<padj_thresh).sum()}")

    # Print top hits
    top = df[df["padj"] < padj_thresh].sort_values("log2fc")
    print("\nTop 10 downregulated:")
    print(top.head(10)[["gene_id", "v2_id", "log2fc", "padj"]].to_string(index=False))
    print("\nTop 10 upregulated:")
    print(top.tail(10).iloc[::-1][["gene_id", "v2_id", "log2fc", "padj"]].to_string(index=False))

    return df


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: volcano.py <deseq2_tsv> <title> <out_prefix>")
        sys.exit(1)
    path, title, out_prefix = sys.argv[1], sys.argv[2], sys.argv[3]
    df = load_deseq2(path)
    print(f"Loaded {len(df)} genes from {path}")
    volcano(df, title, out_prefix)
