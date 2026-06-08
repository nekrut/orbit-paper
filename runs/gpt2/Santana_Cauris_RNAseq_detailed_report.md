# Detailed Report: Santana *Candidozyma auris* RNA-seq Reanalysis

**Project:** Orbit/LLM test reanalysis of Santana *Candidozyma auris* RNA-seq data  
**Date generated:** 2026-06-03  
**Analysis cost:** **$23.46**

## Executive summary

This reanalysis examined six paired-end bulk RNA-seq samples from the Santana *Candidozyma auris* study, focusing on whether the reported adhesin-associated transcriptional phenotype is reproduced. The primary comparison was `AR0382_tnSWI1` versus `AR0382`; the optional comparison was `AR0387` versus `AR0382`.

The initial direct gene-name interpretation was misleading because paper/CGD gene identifiers do not map reliably to the current BRC/NCBI DE-table identifiers by simple zero-padding. After reciprocal DIAMOND protein matching, paper/CGD `SCF1` (`B9J08_001458`) maps exactly to current DE-table gene `B9J08_03708`, and paper/CGD `IFF4109` (`B9J08_004109`) maps exactly to `B9J08_04863`.

With this corrected protein-based mapping, the reanalysis **strongly reproduces SCF1 downregulation**. In the primary `AR0382_tnSWI1` comparison, SCF1 has log2FC = -6.817 and adjusted p-value reported as 0, with normalized counts falling from ~45–47k in AR0382 replicates to ~0.4k in `tnSWI1` replicates. The optional `AR0387` comparison also shows strong SCF1 downregulation, with log2FC = -7.346.

## Data and experimental contrasts

The working Galaxy history `Santana_gpt2` contained 12 paired-end FASTQ datasets representing six RNA-seq libraries:

| Biological group | Replicates | SRA runs |
| --- | --- | --- |
| Highly adhesive AR0382 | `AR0382_A`, `AR0382_B` | `SRR22376032`, `SRR22376031` |
| Poorly adhesive AR0387 | `AR0387_A`, `AR0387_B` | `SRR22376030`, `SRR22376029` |
| AR0382 transposon mutant in `SWI1` | `AR0382_tnSWI1_A`, `AR0382_tnSWI1_B` | `SRR22376028`, `SRR22376027` |

The primary biological question was whether disruption of `SWI1` in AR0382 is associated with altered adhesin expression, especially `SCF1`. The secondary comparison asked whether the poorly adhesive AR0387 isolate differs transcriptionally from AR0382 in the same direction.

## Workflow and reference choices

Reads were analyzed with IWC/Galaxy RNA-seq workflows using reverse-stranded settings, consistent with the Illumina stranded library preparation metadata. The selected reference was B8441 assembly `GCA_002759435.3` / `Cand_auris_B8441_V3`, using the BRC/UCSC GTF `GCA_002759435.3_Cand_auris_B8441_V3.ncbiGene.gtf.gz`.

The quantification workflow used paired FASTQ collection input, fastp/FastQC-style QC, STAR alignment, and featureCounts gene-level counting. Differential expression used IWC `rnaseq-de` / DESeq2 on the featureCounts output tables. The plan threshold for biologically notable DE genes was adjusted p-value < 0.05 and |log2FC| > 1.

## QC interpretation

The primary contrast is technically robust. STAR mapping was high for AR0382 and `tnSWI1` samples, with mapped percentages around 93% and uniquely mapped percentages around 92%. FeatureCounts assignment was also high, approximately 83–85% for these samples.

The optional AR0387 contrast is still useful but deserves more caution. `AR0387_A` mapped similarly well to the other samples, but `AR0387_B` had lower mapping: 79.54% mapped and 77.94% uniquely mapped, with featureCounts assignment around 76.57%. This does not invalidate the very large SCF1 effect, but it means secondary AR0387-specific conclusions should be treated as somewhat less technically clean than the `tnSWI1` result.

## Differential expression overview

### Primary contrast: `AR0382_tnSWI1` vs `AR0382`

DESeq2 tested 5,594 genes. Using adjusted p-value < 0.05, 1,234 genes were significant. Applying the additional |log2FC| > 1 threshold yielded 250 genes: 97 upregulated and 153 downregulated in `AR0382_tnSWI1` relative to AR0382.

This indicates broad transcriptional remodeling after `SWI1` disruption. The strongest significant downregulated genes include `B9J08_03708` (protein-matched SCF1), `B9J08_00860`, `B9J08_04747`, `B9J08_03214`, and others. The presence of SCF1 among the strongest downregulated genes is central to reproducing the paper's interpretation.

### Optional contrast: `AR0387` vs `AR0382`

DESeq2 tested 5,594 genes. Using adjusted p-value < 0.05, 1,582 genes were significant. Applying |log2FC| > 1 yielded 195 genes: 89 upregulated and 106 downregulated in AR0387 relative to AR0382.

The optional contrast also shows strong downregulation of protein-matched SCF1 (`B9J08_03708`) in AR0387 relative to AR0382. This is consistent with the idea that lower adhesion phenotypes are associated with reduced SCF1 expression, although the AR0387 contrast is technically less clean because of the lower mapping metrics for `AR0387_B`.

## Why protein matching was required

A direct interpretation based only on similarly formatted gene names led to the wrong conclusion. The current BRC/NCBI GTF contains genes such as `B9J08_01458` and `B9J08_04109`, but these are not the same proteins as the paper/CGD genes `B9J08_001458` and `B9J08_004109`. Simple numeric resemblance or zero-padding is therefore unsafe.

To resolve this, the protein sequences from paper/CGD B8441 annotations were matched against the current NCBI/BRC B8441 V3 protein set using DIAMOND reciprocal best-hit matching. This established the correct correspondence at the amino-acid level.

## DIAMOND reciprocal matching results

DIAMOND version 2.1.22 was used locally. Databases were built from:

- CGD B8441 ORF translations: `C_auris_B8441_current_default_protein.fasta.gz` (5,445 proteins)
- NCBI/BRC B8441 V3 protein FASTA: `GCA_002759435.3_Cand_auris_B8441_V3_protein.faa.gz` (5,424 proteins)

Unmasked DIAMOND was used for the final reciprocal table because the large adhesin IFF4109 contains repetitive/low-complexity sequence; default masking underreported full-length coverage despite exact matching.

| Paper/CGD gene | Current DE-table gene | Reciprocal best? | Identity | Query coverage | Subject coverage | Bitscore |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `SCF1 / B9J08_001458` | `B9J08_03708` | True | 100% | 100% | 100% | 1231 |
| `IFF4109 / B9J08_004109` | `B9J08_04863` | True | 100% | 100% | 100% | 5076 |


Both key genes are reciprocal best hits with 100% identity and 100% coverage in both directions. This verifies that current DE-table gene `B9J08_03708` is the correct current identifier for paper/CGD SCF1, and `B9J08_04863` is the correct current identifier for paper/CGD IFF4109.

## Corrected key-gene DE results

| Contrast | Protein/gene label | Current DE-table gene | Base mean | log2FC | adjusted p-value | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `AR0382_tnSWI1_vs_AR0382` | `SCF1 / B9J08_001458` | `B9J08_03708` | 23172.37 | -6.817 | 0 | strong downregulation |
| `AR0382_tnSWI1_vs_AR0382` | `IFF4109 / B9J08_004109` | `B9J08_04863` | 898.95 | -0.303 | 0.0392561505045137 | modest downregulation |
| `AR0387_vs_AR0382` | `SCF1 / B9J08_001458` | `B9J08_03708` | 19427.75 | -7.346 | 0 | strong downregulation |
| `AR0387_vs_AR0382` | `IFF4109 / B9J08_004109` | `B9J08_04863` | 667.35 | -0.745 | 5.18972213945492e-08 | modest downregulation |


### Primary SCF1 result

For `AR0382_tnSWI1` vs `AR0382`, protein-matched SCF1 (`B9J08_03708`) shows log2FC = -6.817 and adjusted p-value = 0. Normalized counts are approximately 46,989 and 44,890 in the AR0382 replicates, compared with 384 and 427 in the `tnSWI1` replicates. This is a dramatic decrease and clearly reproduces the expected downregulation.

### Optional AR0387 SCF1 result

For `AR0387` vs `AR0382`, protein-matched SCF1 (`B9J08_03708`) shows log2FC = -7.346 and adjusted p-value = 0. Normalized counts are approximately 39,473 and 37,761 in AR0382, compared with 231 and 245 in AR0387. This independently supports SCF1 downregulation in the lower-adhesion context.

### IFF4109 result

Protein-matched IFF4109 (`B9J08_04863`) is also lower in both comparisons, but its effect is more modest than SCF1. In the primary `tnSWI1` contrast, IFF4109 has log2FC = -0.303 and adjusted p-value = 0.0393, which is statistically significant but below the |log2FC| > 1 effect-size threshold. In the optional AR0387 contrast, IFF4109 has log2FC = -0.745 and adjusted p-value = 5.19e-08, still below the |log2FC| > 1 threshold.


## Figures

![Protein-matched volcano plot: AR0382_tnSWI1 vs AR0382](fig_volcano_tnSWI1_vs_AR0382_protein_matched.png)

**Figure 1.** Protein-matched volcano plot for the primary `AR0382_tnSWI1` vs `AR0382` contrast. SCF1 (`B9J08_03708`) and IFF4109 (`B9J08_04863`) are highlighted.

![Protein-matched volcano plot: AR0387 vs AR0382](fig_volcano_AR0387_vs_AR0382_protein_matched.png)

**Figure 2.** Protein-matched volcano plot for the optional `AR0387` vs `AR0382` contrast. SCF1 is again strongly downregulated.

## Interpretation

The corrected analysis supports the central biological interpretation from the Santana study: SCF1 is a major adhesin-associated transcriptional target whose expression is dramatically reduced in contexts associated with reduced adhesion. The most important correction is that SCF1 must be interpreted through protein-matched current gene ID `B9J08_03708`, not by apparent numeric similarity to `B9J08_01458`.

In the primary experiment, `SWI1` disruption in AR0382 causes a large transcriptional shift and a particularly strong collapse of SCF1 expression. The magnitude of the effect is far beyond a marginal statistical result: the log2 fold change is approximately -6.8, corresponding to roughly a 100-fold reduction, and normalized counts drop from tens of thousands to only hundreds. This is consistent with the model that SWI1 or SWI1-dependent regulatory programs support expression of SCF1 and thus surface association/adhesion phenotypes.

The optional AR0387 comparison strengthens the interpretation because SCF1 is also strongly lower in AR0387 relative to AR0382. This suggests that low SCF1 expression is not unique to the transposon mutant, but may be a shared transcriptional feature of low-adhesion contexts. However, the AR0387 contrast should be framed as supporting evidence rather than the primary result because one AR0387 replicate has lower mapping and assignment metrics.

IFF4109 is a relevant adhesin-associated gene, but it is not the main transcriptional signal in this reanalysis. Once correctly protein-matched, IFF4109 is modestly downregulated in both contrasts, whereas SCF1 is dramatically downregulated. Therefore, the strongest conclusion is SCF1-centered rather than IFF4109-centered.

## Limitations and cautions

1. **Identifier mismatch was the dominant analysis pitfall.** Current and paper-era B8441 annotations use different `B9J08_*` identifiers for the same proteins. Protein matching is required for accurate interpretation.
2. **AR0387_B has lower mapping.** The optional AR0387 contrast remains useful, but primary claims should rely most heavily on the cleaner `AR0382_tnSWI1` contrast.
3. **Functional interpretation is expression-based.** The RNA-seq data support SCF1 transcriptional downregulation, but functional adhesion conclusions still depend on the experimental phenotyping from the paper.
4. **Adjusted p-value of 0 reflects numerical underflow/reporting.** It should be interpreted as extremely significant, not literally zero probability.

## Final conclusion

After DIAMOND reciprocal protein matching, the reanalysis **does reproduce strong SCF1 downregulation**. Paper/CGD SCF1 (`B9J08_001458`) is current DE-table gene `B9J08_03708`, which is one of the strongest downregulated genes in `AR0382_tnSWI1` vs `AR0382` and is also strongly downregulated in `AR0387` vs `AR0382`. The corrected result aligns with the paper's conclusion that SCF1 is a major adhesin-associated factor linked to surface association, colonization, and virulence phenotypes.

## Generated artifacts

- `de_tnSWI1_vs_AR0382_annotated.tsv`
- `de_AR0387_vs_AR0382_annotated.tsv`
- `protein_matching/diamond_reciprocal_key_matches_unmasked.tsv`
- `protein_matched_key_gene_DE.tsv`
- `fig1d_analog_protein_matched_tnSWI1_vs_AR0382.svg`
- `Santana_Cauris_RNAseq_detailed_report.pdf`

## Cost

Total analysis/report cost inserted as requested: **$23.46**.
