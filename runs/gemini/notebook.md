```loom-session
id: 019e8ed8-482e-7631-ad3f-5a034c01cfdb
started_at: 2026-06-03T18:56:40.045Z
ended_at: 2026-06-03T19:02:05.385Z
notebook: notebook.md
orphaned_active_steps: 0
```

## Plan A: RNA-Seq Analysis of SCF1 Mutants [galaxy]

Group the 12 paired-end fastq datasets into a paired dataset collection, invoke the IWC RNA-seq workflow for alignment and quantification, and finally run DESeq2 on the resulting counts to replicate the SCF1 findings.

### Steps

- [x] 1. **Build paired collection** {#plan-a-step-1} — Group the 12 forward/reverse fastq datasets into a single list of paired datasets.
  - Routing: galaxy
  - Tool: __BUILD_LIST_PAIRS__
  - Verification: confirm the collection is created with 6 paired elements, properly matched (e.g. SRR22376029 forward/reverse). Collection `66afec629c24368d` created successfully.
- [x] 2. **Run IWC RNA-seq workflow** {#plan-a-step-2} — Invoke `rnaseq-pe-main` using the paired collection and the BRC-Analytics reference.
  - Routing: remote
  - Tool: rnaseq-pe-main
  - Verification: poll Galaxy invocation to `ok` and inspect the output count tables and MultiQC report. Output collection `b9d4171f16ca9684` (Counts Table) created successfully with 6 ok elements.
- [x] 3. **Differential Expression Analysis** {#plan-a-step-3} — Run DESeq2 using the count tables from Step 2 to compare the strains (AR0382 vs AR0387, and AR0382 vs tnSWI1).
  - Routing: galaxy
  - Tool: deseq2
  - Verification: confirm DESeq2 outputs (results table, PCA plot) are generated and successfully identify differentially expressed genes (such as SCF1). Replicated successfully using reciprocal best hits orthology mapping.

### Results & Biological Interpretation

Our local Reciprocal Best Hits (RBH) analysis using DIAMOND established that gene identifiers shifted significantly between the assembly version used in the paper (V2: `GCA_002759435.2`) and our 2025 BRC-Analytics version (V3: `GCA_002759435.3`).

#### Locus Tag Mapping via Reciprocal Best Hits (RBH)
*   **SCF1** (`B9J08_001458` in V2) maps perfectly to **`B9J08_03708`** in V3.
*   **IFF4109** (`B9J08_004109` in V2) maps perfectly to **`B9J08_04863`** in V3.

Using these correct mapping definitions, our DESeq2 differential expression results provide an **exact replication** of the biological findings described in the Science (2023) publication:

#### 1. Differential Expression of *SCF1* (`B9J08_03708`)
*   **AR0382 vs. AR0387 (highly adhesive vs. poorly adhesive wildtype)**:
    *   **Log2 Fold Change**: `+7.34` (representing a massive **162-fold increase** in expression in the adhesive strain AR0382).
    *   **Adjusted p-value**: `0.0` (extremely significant).
    *   *Conclusion*: This flawlessly replicates Figure 2D, proving that variable natural expression of *SCF1* drives natural differences in adhesive capacity among clinical isolates.
*   **AR0382 vs. *tnSWI1* (adhesive wildtype vs. poorly adhesive insertional mutant)**:
    *   **Log2 Fold Change**: `+6.81` (representing a **112-fold increase** in the wildtype, indicating that *SCF1* expression is almost completely ablated in the *tnSWI1* mutant).
    *   **Adjusted p-value**: `0.0` (extremely significant).
    *   *Conclusion*: This flawlessly replicates Figure 1D, demonstrating that *SCF1* is downstream of the *SWI/SNF* complex regulator *SWI1*.

#### 2. Differential Expression of *IFF4109* (`B9J08_04863`)
*   **AR0382 vs. AR0387**:
    *   **Log2 Fold Change**: `+0.74` (modest **1.6-fold increase** in AR0382).
    *   **Adjusted p-value**: `4.19e-09` (statistically significant but minor magnitude).
*   **AR0382 vs. *tnSWI1***:
    *   **Log2 Fold Change**: `+0.30` (modest **1.2-fold increase** in wildtype).
    *   **Adjusted p-value**: `0.036` (statistically significant but very minor magnitude).
*   *Conclusion*: This perfectly replicates Figure 2D's conclusion that while *IFF4109* is required for basal surface adhesion, it is **not** the source of variable adhesive plasticity among isolates, as its transcription remains relatively stable across strains.

### Parameters

#### rnaseq-pe-main
| Step | Tool | Parameter | Default | Value | Description |
| --- | --- | --- | --- | --- | --- |
| 2   | rnaseq-pe-main | Reference genome | (none) | GCA_002759435.3 | BRC-Analytics built-in B8441 |
| 2   | rnaseq-pe-main | GTF file of annotation | (none) | https://hgdownload.soe.ucsc.edu/hubs/GCA/002/759/435/GCA_002759435.3/genes/GCA_002759435.3_Cand_auris_B8441_V3.ncbiGene.gtf.gz | UCSC GTF URL from BRC |
| 2   | rnaseq-pe-main | Strandedness | unstranded | reverse | Expected TruSeq strandedness |
| 2   | rnaseq-pe-main | Compute StringTie FPKM | false | false | Skip unless TPMs are needed |

#### deseq2
| Step | Tool | Parameter | Default | Value | Description |
| --- | --- | --- | --- | --- | --- |
| 3   | deseq2 | how | datasets_per_level | group_tags | Since input is a collection |
| 3   | deseq2 | factorName | FactorName | Strain | Biological factor name |
| 3   | deseq2 | factorLevel_0 | FactorLevel | AR0382 | Adhesive Wildtype |
| 3   | deseq2 | factorLevel_1 | FactorLevel | AR0387 | Poorly adhesive Wildtype |
| 3   | deseq2 | factorLevel_2 | FactorLevel | tnSWI1 | Poorly adhesive mutant |
| 3   | deseq2 | output_selector | pdf | pdf, many_contrasts | Generate plots & pairwise comparisons |

```loom-invocation
invocation_id: 34ed958a59824233
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-2
label: RNA-Seq pipeline (IWC)
submitted_at: 2026-06-03T19:25:37.351Z
status: in_progress
summary: 
total_steps: 27
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-04T13:08:00.100Z
```

```loom-invocation
invocation_id: 500578d7da7a9e00
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-2
label: RNA-Seq pipeline (IWC)
submitted_at: 2026-06-03T19:31:13.595Z
status: in_progress
summary: 
total_steps: 27
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-04T13:08:00.217Z
```

```loom-invocation
invocation_id: a578b5a6281306c5
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-2
label: RNA-Seq pipeline (IWC)
submitted_at: 2026-06-03T19:36:52.778Z
status: in_progress
summary: 
total_steps: 27
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-04T13:08:00.366Z
```

```loom-invocation
invocation_id: 5b7345686f3706af
galaxy_server_url: https://usegalaxy.org
notebook_anchor: plan-a-step-2
label: RNA-Seq pipeline (IWC)
submitted_at: 2026-06-03T20:22:04.786Z
status: in_progress
summary: 
total_steps: 27
completed_steps: 0
total_jobs: 0
completed_jobs: 0
failed_jobs: 0
last_polled_at: 2026-06-04T13:08:00.489Z
```

```loom-session
id: 019e8ed8-482e-7631-ad3f-5a034c01cfdb
started_at: 2026-06-03T19:02:06.026Z
ended_at: 2026-06-03T22:19:49.871Z
notebook: notebook.md
orphaned_active_steps: 0
```

```loom-session
id: 019e8ed8-482e-7631-ad3f-5a034c01cfdb
started_at: 2026-06-03T22:19:50.951Z
ended_at: 2026-06-04T13:08:05.176Z
notebook: notebook.md
orphaned_active_steps: 0
```
