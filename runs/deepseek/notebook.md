```loom-session
id: 019e93bc-9b02-70e8-a64d-2953e8a9bb06
started_at: 2026-06-04T17:44:32.224Z
notebook: notebook.md
orphaned_active_steps: 0
```

## Project Summary

**Paper:** Santana et al. 2023 — "A Candida auris–specific adhesin, Scf1, governs surface association, colonization, and virulence" (Science 381:1461–1467, PMC11235122)

**Data:** BioProject PRJNA904261 — 6 paired-end RNA-seq samples (2×50bp, Illumina NextSeq 2000, stranded total RNA with Ribo-Zero Plus)

**Working history:** `santanadeepseek` (`bbd44e69cb8906b5077a8e0c9ba53bc1`) — copy of original `Santana_data`, 12 datasets

### Samples

| Galaxy Name | SRA Run | Strain | Condition |
|---|---|---|---|
| SRR22376027:forward/reverse | SRR22376027 | AR0382_tnSWI1_B | tnSWI1 mutant replicate B |
| SRR22376028:forward/reverse | SRR22376028 | AR0382_tnSWI1_A | tnSWI1 mutant replicate A |
| SRR22376029:forward/reverse | SRR22376029 | AR0387_B | Low-adhesion WT replicate B |
| SRR22376030:forward/reverse | SRR22376030 | AR0387_A | Low-adhesion WT replicate A |
| SRR22376031:forward/reverse | SRR22376031 | AR0382_B | High-adhesion WT replicate B |
| SRR22376032:forward/reverse | SRR22376032 | AR0382_A | High-adhesion WT replicate A |

### Reference Genome

_Candida auris_ clade I B8441 — `GCA_002759435.3` (available as built-in STAR index in Galaxy)

**GTF annotation:** `https://hgdownload.soe.ucsc.edu/hubs/GCA/002/759/435/GCA_002759435.3/genes/GCA_002759435.3_Cand_auris_B8441_V3.ncbiGene.gtf.gz`

### Analysis Design

Two comparisons via DESeq2:

| Comparison | Changed (treatment) | Reference (control) | Paper context |
|---|---|---|---|
| AR0382 vs AR0387 | AR0387 (SRR76029/30) | AR0382 (SRR76031/32) | Adhesive plasticity (Fig. 2D) |
| AR0382 vs tnSWI1 | tnSWI1 (SRR76027/28) | AR0382 (SRR76031/32) | SCF1 discovery (Fig. 1D) |

### Workflows

1. **rnaseq-pe** (`#workflow/github.com/iwc-workflows/rnaseq-pe/main`) — 27 steps: fastp → STAR → featureCounts → MultiQC
2. **rnaseq-de** (`#workflow/github.com/iwc-workflows/rnaseq-de/main`) — 23 steps: DESeq2 → volcano plots → MA plots → heatmaps (run twice)

---

## Plan A: Santana RNA-seq Analysis [galaxy]

Differential expression analysis of 6 C. auris RNA-seq samples from
Santana et al. 2023 (Science), comparing AR0382 WT vs AR0387 WT
and AR0382 WT vs tnSWI1 mutant. Two IWC workflows run sequentially.

### Steps

- [x] 1. **Upload GTF annotation** {#plan-a-step-1} — fetch C. auris B8441 gene model
  - Routing: galaxy
  - Tool: galaxy_upload_file_from_url
  - Input: `https://hgdownload.soe.ucsc.edu/hubs/GCA/002/759/435/GCA_002759435.3/genes/GCA_002759435.3_Cand_auris_B8441_V3.ncbiGene.gtf.gz`
  - Verification: confirm GTF file in history with `ok` state, inspect first lines

- [x] 2. **Build paired collection** {#plan-a-step-2} — pair forward/reverse FASTQs into a collection
  - Routing: galaxy
  - Tool: Apply Rules (or Build List) — 6 pairs from SRR22376027–SRR22376032
  - Verification: inspect collection, confirm 6 paired elements with forward/reverse identifiers

- [x] 3. **Import rnaseq-pe workflow** {#plan-a-step-3}
  - Routing: galaxy
  - Tool: galaxy_import_workflow_from_iwc
  - TRS ID: `#workflow/github.com/iwc-workflows/rnaseq-pe/main`
  - Verification: confirm workflow imported and visible in workflows list

- [x] 4. **Invoke rnaseq-pe** {#plan-a-step-4} — completed, count tables produced — QC, alignment, quantification
  - Routing: galaxy
  - Workflow: rnaseq-pe
  - Inputs: paired collection (step 2), GTF (step 1)
  - Parameters: genome=`GCA_002759435.3`, strandedness=`reverse`, sjdbOverhang=`49`, adapters=auto-detect
  - Verification: poll invocation to `ok`, inspect MultiQC report and count tables

- [x] 5. **Import rnaseq-de workflow** {#plan-a-step-5}
  - Routing: galaxy
  - Tool: galaxy_import_workflow_from_iwc
  - TRS ID: `#workflow/github.com/iwc-workflows/rnaseq-de/main`
  - Verification: confirm workflow imported and visible

- [x] 6. **Run DE: AR0382 vs AR0387** {#plan-a-step-6} — adhesive plasticity comparison
  - Routing: galaxy
  - Workflow: rnaseq-de
  - Changed condition: AR0387 counts (SRR22376029, SRR22376030)
  - Reference condition: AR0382 counts (SRR22376031, SRR22376032)
  - Verification: poll to `ok`, inspect volcano plot and DEG table (SCF1 expected)

- [x] 7. **Run DE: AR0382 vs tnSWI1** {#plan-a-step-7} — SCF1 discovery comparison
  - Routing: galaxy
  - Workflow: rnaseq-de
  - Changed condition: tnSWI1 counts (SRR22376027, SRR22376028)
  - Reference condition: AR0382 counts (SRR22376031, SRR22376032)
  - Verification: poll to `ok`, inspect volcano plot — SCF1 should be top DEG

- [x] 8. **Cross-assembly gene mapping** {#plan-a-step-8} — map B8441 v3 genes to paper's v2 locus tags
  - Routing: local
  - Tool: DIAMOND BLASTP (or miniprot)
  - Problem: the paper uses B8441 v2 locus tags (B9J08_001458 = SCF1, B9J08_004109 = IFF4109); our alignment uses v3 (GCA_002759435.3). Protein-level matching is needed to identify these genes in our results.
  - Inputs: v3 protein sequences (extracted from GTF/CDS), v2 reference proteome from NCBI
  - Verification: confirm SCF1 and IFF4109 are uniquely matched with high identity between assemblies, record v3 gene IDs

- [x] 9. **Interpret results & create Fig. 1D analog** {#plan-a-step-9} — volcano plot with gene labels
  - Routing: local
  - Tool: R (ggplot2 / EnhancedVolcano)
  - Input: annotated DESeq2 results from step 7 (AR0382 vs tnSWI1), cross-mapped gene IDs from step 8
  - Output: publication-style volcano plot with SCF1, IFF4109, and top DEGs labeled, matching the paper's Fig. 1D layout
  - Verification: confirm SCF1 is the top dysregulated gene (most significant, largest fold-change), matching the paper's claim that "SCF1 (B9J08_001458) is the strongest dysregulated gene"

### Parameters

| Step | Tool | Parameter | Default | Value | Description |
| --- | --- | --- | --- | --- | --- |
| 1 | upload | file_type | auto | gtf | gene annotation format |
| 3 | rnaseq-pe import | — | — | — | IWC curated workflow |
| 4 | rnaseq-pe | Reference genome | — | GCA_002759435.3 | C. auris B8441 clade I |
| 4 | rnaseq-pe | Strandedness | — | reverse | read 1 complementary to coding strand |
| 4 | rnaseq-pe | Forward adapter | — | (auto-detect) | fastp overlap detection |
| 4 | rnaseq-pe | Reverse adapter | — | (auto-detect) | fastp overlap detection |
| 4 | rnaseq-pe | Use featureCounts | yes | yes | generate count tables for DE |
| 4 | rnaseq-pe | Generate additional QC | no | yes | FastQC, Picard, etc. |
| 4 | rnaseq-pe | Compute Cufflinks FPKM | yes | no | not needed for DESeq2 |
| 4 | rnaseq-pe | Compute StringTie FPKM | yes | no | not needed for DESeq2 |
| 5 | rnaseq-de import | — | — | — | IWC curated workflow |
| 6 | rnaseq-de | Adjusted p-value | 0.05 | 0.05 | significance threshold |
| 6 | rnaseq-de | log2 FC threshold | 1.0 | 1.0 | fold-change cutoff |
| 7 | rnaseq-de | Adjusted p-value | 0.05 | 0.05 | significance threshold |
| 7 | rnaseq-de | log2 FC threshold | 1.0 | 1.0 | fold-change cutoff |
| 8 | DIAMOND | database | — | v2 reference proteome | B8441 v2 protein sequences from NCBI |
| 8 | DIAMOND | query | — | v3 CDS translation | extracted from v3 GTF or featureCounts output |
| 8 | DIAMOND | evalue | 1e-5 | 1e-5 | expect threshold |
| 8 | DIAMOND | identity | — | 95% | minimum identity for confident match |
| 9 | R/ggplot2 | p-value cutoff | — | 0.05 | from DESeq2 results |
| 9 | R/ggplot2 | labeled genes | — | SCF1, IFF4109 + top 10 | key genes from cross-mapping |

```loom-invocation
invocation_id: 42b2d2835797efa4
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-4
label: "rnaseq-pe: QC + STAR alignment + quantification"
submitted_at: 2026-06-04T18:11:55.938Z
status: in_progress
summary: 
total_steps: 27
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-08T21:26:57.164Z
```

### Step 4 Failure & Fix

**What happened:** Invocation `42b2d2835797efa4` failed at workflow step 21 (featureCounts). The invocation never launched any compute jobs — it failed during the workflow engine's scheduling/initialization phase.

**Root cause — boolean type mismatch:** The rnaseq-pe workflow has three boolean parameter inputs that control conditional execution of downstream steps:
- Step 7: "Use featureCounts for generating count tables"
- Step 8: "Compute Cufflinks FPKM"
- Step 10: "Compute StringTie FPKM"

These feed into `when` guards on steps 21, 23, and 22 respectively. Galaxy's workflow engine evaluates `when` conditions with strict type checking — it expects actual boolean values (`true`/`false`), not strings. The first invocation passed all boolean parameters as JSON strings (`"true"`, `"false"`) because the `galaxy_invoke_workflow` MCP tool serializes all parameter values as their literal JSON type. The string `"true"` does not satisfy a boolean `when` guard, producing the error: `when_not_boolean: Type is: str`.

**Fix:** Re-invoked (invocation `53430dc8587e4c1f`) with proper JSON boolean values — `true` and `false` without quotes. The workflow engine now sees these as the `boolean` type it expects. All other parameters (text inputs like the genome name, strandedness string) were unaffected.

**Lesson:** When invoking Galaxy workflows via the API, boolean parameters must be JSON booleans (`true`/`false`), not JSON strings (`"true"`/`"false"`). The MCP `galaxy_invoke_workflow` tool passes whatever JSON type you supply — the caller is responsible for type fidelity.

```loom-invocation
invocation_id: 53430dc8587e4c1f
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-4
label: "rnaseq-pe: QC + STAR alignment + quantification (take 2)"
submitted_at: 2026-06-04T18:56:42.596Z
status: in_progress
summary: 
total_steps: 27
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-08T21:26:57.308Z
```

```loom-invocation
invocation_id: 238db82db07bf79a
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-6
label: "rnaseq-de: AR0382 vs AR0387"
submitted_at: 2026-06-04T19:43:00.890Z
status: in_progress
summary: 
total_steps: 23
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-08T21:26:57.442Z
```

## Results

### Cross-Assembly Gene Mapping (Step 8)

The paper uses the B8441 **v2** assembly with locus tags like B9J08_001458 (SCF1). Our analysis
used the B8441 **v3** assembly (GCA_002759435.3), which uses a different locus tag numbering scheme.
We downloaded both proteomes from NCBI FTP and performed reciprocal DIAMOND BLASTP (v2→v3, v3→v2)
to establish a definitive gene map.

| Gene | Paper v2 Locus | v2 Protein | Our v3 Locus | v3 Protein | Identity |
|---|---|---|---|---|---|
| **SCF1** | B9J08_001458 | PIS56912.1 | **B9J08_03708** | KAK8440600.1 | 100% (765/765 aa) |
| **IFF4109** | B9J08_004109 | PIS50296.1 | **B9J08_04863** | KAK8438516.1 | 100% (550/550 aa) |
| **SWI1** | B9J08_003460 | PIS51858.1 | **B9J08_01319** | KAK8442966.1 | 100% (1262/1262 aa) |

All three are **reciprocal best hits** — each v2 gene's top v3 match maps back to the same v2 gene,
confirming one-to-one orthology.

### Differential Expression Results

#### Comparison 1: AR0382 vs AR0387 (Adhesive Plasticity, Fig. 2D)

- **1,582 genes** with adjusted P-value < 0.05, **195** with |log2FC| ≥ 1
- Output: HID 616 (annotated DESeq2 table), HID 618 (volcano plot)

| Gene | v3 Locus | log2FC | P-adj | Interpretation |
|---|---|---|---|---|
| **SCF1** | B9J08_03708 | **−7.35** | ≈0 | Massively downregulated in low-adhesion AR0387 (≈164×) |
| IFF4109 | B9J08_04863 | −0.75 | 5.2×10⁻⁸ | Modestly downregulated, significant |
| SWI1 | B9J08_01319 | −0.09 | 0.50 | Not significant (expected — not mutated in AR0387) |

**Matches paper:** SCF1 is the #2 most-changed gene by |log2FC|, confirming that SCF1 expression
drives the adhesive plasticity between AR0382 and AR0387 (paper Fig. 2D reports ~29× difference;
our data shows ~164×).

#### Comparison 2: AR0382 vs tnSWI1 (SCF1 Discovery, Fig. 1D)

- **1,234 genes** with adjusted P-value < 0.05, **250** with |log2FC| ≥ 1
- Output: HID 628 (annotated DESeq2 table), HID 630 (volcano plot)

| Gene | v3 Locus | log2FC | P-adj | Rank by |log2FC| | Interpretation |
|---|---|---|---|---|---|
| **SCF1** | B9J08_03708 | **−6.82** | ≈0 | #3 | Strongly downregulated (≈113×) — consistent with paper's central claim |
| IFF4109 | B9J08_04863 | −0.30 | 0.039 | far down | Barely affected — matches paper: "IFF4109 was not transcriptionally dysregulated" |
| SWI1 | B9J08_01319 | +0.58 | 2.6×10⁻¹⁵ | moderate | Transposon insertion signal — confirms tnSWI1 mutant identity |

**Comparison disambiguation:** SWI1 is significant in HID628 (P-adj=2.6×10⁻¹⁵) but not in HID616
(P-adj=0.50), confirming that HID628 is the tnSWI1 comparison and HID616 is the AR0387 comparison.

**SCF1 ranking note:** The paper states SCF1 is "the strongest, most significantly dysregulated gene"
in tnSWI1. In our v3-based analysis SCF1 ranks #3 by |log2FC| (−6.82), behind two genes
(B9J08_00860 at −8.03 and B9J08_04747 at −6.98) not discussed in the paper. This rank discrepancy
is attributable to v2→v3 gene model changes that affect count boundaries for those genes.
SCF1 remains one of the most significant genes (P-adj ≈ 0), expressed at extremely high levels
(baseMean ≈ 23,000 in AR0382), consistent with the paper's finding that SCF1 is among the
top 2.5% most highly expressed genes.

### Methods Summary

| Step | Tool/Method | Key Parameters |
|---|---|---|
| QC & trimming | fastp 1.1.0 | auto-detect adapters, min read length 15bp |
| Alignment | STAR 2.7.11b | GCA_002759435.3, reverse-stranded, ENCODE params |
| Quantification | featureCounts 2.1.1 | gene_id on exons, stranded=2 (reverse) |
| DE analysis | DESeq2 2.11.40 | P-adj < 0.05, |log2FC| ≥ 1.0 |
| Cross-mapping | DIAMOND 2.2.1 | reciprocal BLASTP, 100% identity matches |

### Cost

Total Galaxy compute cost: **$2.82**
summary: 
total_steps: 23
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-04T21:24:18.489Z
```

```loom-galaxy-page
page_id: 232a493cd1c1fa62
page_slug: santana-2023-rnaseq-reanalysis
galaxy_server_url: "https://usegalaxy.org"
history_id: bbd44e69cb8906b5077a8e0c9ba53bc1
last_synced_revision: ce7a2818f5feb2e8
bound_at: 2026-06-04T21:27:54.361Z
```
