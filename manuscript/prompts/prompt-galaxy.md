# Orbit prompt: prepare molecular-clock benchmarks in Galaxy

Use this entire file as the preparation prompt in Orbit. It replaces the execution instructions and example validator in `prompt.md`; it does not depend on that validator. The companion `prompt-galaxy-analysis.md` is for the subsequent analysis.

## Objective and scope

Prepare a verified, reusable Galaxy input package for ChronAeon Date, LOOCV, nonlinear clocks, AutoClock, diagnostic figures, and a later compendium build. Perform data acquisition, extraction, validation, transformation, and packaging as Galaxy operations/jobs. Orbit/Loom orchestrates the work and maintains the notebook.

Use these explicit defaults unless the researcher changes them:

```yaml
scope: reference_42
# Alternatives: discover, reference_plus_discovery
galaxy_server: https://usegalaxy.org
project_directory: /Users/anton/git/beast-chrom
history_name: ChronAeon - benchmark input preparation
discovery_target_ready_cohorts: 20
discovery_max_candidates: 100
run_full_analysis: false
include_surveillance_challenges: false
```

`reference_42` means the exact study list from a pinned `veg/chronaeon` benchmark snapshot. `discover` preserves the original harvester's purpose: find additional published empirical BEAST datasets. `reference_plus_discovery` prepares both sets separately; it never replaces missing reference studies with newly discovered ones. The discovery limits above apply only when discovery is selected. Report an incomplete discovery target honestly after inspecting the candidate limit.

This request authorizes preparation, necessary Galaxy tools/workflows, and small Galaxy validation runs. Stop after delivering the verified handoff. Do not automatically launch the full scientific benchmark, surveillance challenges, BEAST MCMC, or public website deployment.

Local activity is limited to reading sources, authoring small scripts/tool definitions/manifests, and orchestrating Galaxy. Do not process scientific datasets locally and then present their uploaded results as a Galaxy analysis. Do not install or run the scientific engine on the laptop for this task. Do not restart Orbit.

## Working behavior

- Confirm the active Galaxy server and account; use the configured credentials without exposing them. A 403 is an access failure, not evidence of an absent artifact. Do not silently substitute another account or server.
- Maintain `notebook.md` as the durable record. Record decisions, actual Galaxy identifiers, source versions, and verification evidence. Track actual workflow invocations using Loom's typed notebook records; do not maintain a competing plan database.
- Reuse a matching preparation history and verified inputs on resume. Check for already uploaded files and in-flight jobs before resubmitting anything.
- Give an initial update and meaningful milestone updates in chat. While waiting, rely on Orbit's background tracking and yield when no work is ready. Do not run a rapid model-driven metadata polling loop.
- Verify completed outputs and investigate failures automatically. Continue independent valid work; do not advance a cohort past a failed prerequisite. Distinguish an expected validation rejection from an infrastructure/tool failure.
- Use concise, descriptive, clickable Galaxy links in chat and notebook prose. Never invent Galaxy IDs or claim an artifact is complete before inspecting it.
- Prefer installed Galaxy tools; author versioned UDTs only for missing functionality. Read the Galaxy collection and UDT skills available to this Orbit runtime. Do not assume subagent tools exist.

## 1. Establish sources and a bounded inventory

For the reference set, pin the benchmark repository and retain the exact 42 study IDs in `expected_studies.tsv`. The snapshot inspected while drafting this prompt was:

- Benchmark repository: `https://github.com/veg/chronaeon`, commit `f77903b928c545000b54a848e9ebb33db5ee62bf`.
- Engine repository: `https://github.com/veg/HyphAeon`, commit `73237b7cebc916a60d5e79d1137d60e4fa73c6c0`.

Use these as explicit initial pins, not as evidence that these engine and benchmark revisions generated every published reference value. Inspect manifests/logs for historical engine provenance and record any unresolved mismatch. Do not silently follow changing `main` branches. Preserve `AGENT.MD`, the source manifest, required builder/curation/assets, licenses, and relevant dependency metadata as provenance inputs. Download only required artifacts rather than unrelated repository histories or surveillance data.

Inspect each study's available `beast.xml.gz`, `beast_config.xml.gz`, source archive references, and provenance. Resolve aliases by content and evidence. Do not treat two names for identical XML as two cohorts. Keep nonidentical configurations separate until the benchmark's intended configuration is established.

For discovery, search paper-linked GitHub, Zenodo, Dryad, Figshare, and other author deposits. Search for BEAST 1 clock elements (`strictClockBranchRates`, `discretizedBranchRates`, `randomLocalClockModel`) and BEAST 2 specifications (`StrictClockModel`, `UCRelaxedClockModel`, `RandomLocalClockModel`) with sampling dates. Exclude simulations, tutorials, software fixtures, and unrelated data from the empirical benchmark. Prefer immutable releases/record versions and author-deposited originals. Resolve the publication DOI and the precise dataset/configuration it supports.

Create a tabular source inventory with at least:

```text
study_id  cohort_set  publication_doi  source_record_url  download_url  source_revision  original_filename  archive_member  artifact_role  expected_checksum  checksum_algorithm  access_status  license
```

Use valid quoted TSV/CSV, not whitespace-separated values. Missing checksum/license information is explicitly null/unknown. Preserve retrieval timestamps and observed byte counts in the resulting provenance. Signed URLs or credentials do not belong in portable manifests.

Important known discrepancy: the Zenodo API for DOI `10.5281/zenodo.22908446` listed only the paper PDF during this prompt's preparation, not the claimed 5 GB data archive. Verify the actual record before using it; do not invent an archive URL or count the paper as the input package.

## 2. Import to Galaxy and preserve originals

Batch-fetch verified immutable URLs into the preparation history using Galaxy's supported fetch/upload interface. Use a source manifest to associate inputs with study IDs. Fetch each unique archive once, then extract required members in Galaxy; do not download the same multi-study archive repeatedly.

Preserve original downloaded bytes. Check the upload interface's decompression and text-conversion behavior: an original `.gz` must not silently become uncompressed XML while retaining the compressed-file checksum. Disable transformations through supported options or retain a verified binary/archive copy. Record separate compressed and decompressed hashes when applicable. Verify Galaxy-side bytes with a checksum job; upload success alone is insufficient.

Use native Galaxy extraction and collection tools where available. If a source requires browser authentication, do not pass secrets to a UDT. Record the access limitation and the supported import path. Keep provenance for rejected candidates; do not delete existing history contents.

Preserve the source XML unchanged, including embedded trees and BEAST settings. Later tree-free execution must avoid using trees; that does not justify editing the archived XML. Do not submit BEAST itself during preparation.

## 3. Implement a strict validator/extractor as a Galaxy step

Discover an installed equivalent first. If necessary, author a UDT that accepts original XML/archives plus explicit study metadata and emits validation JSON and verified derivative datasets. Resolve a real container and record its digest; never guess an image tag. Its environment must contain all required libraries. Do not rely on internet package installation from compute jobs. If no usable runtime is available, report the concrete missing capability and preserve completed preparation work.

The original `validate_beast_xml.py` example is inadequate and must not be used unchanged. Implement these checks with a consistent, versioned validation policy:

**Parsing and alignment identity**

- Support gzip and uncompressed XML, BEAST 1 and 2, namespaces, sequence text/attributes, and relevant taxon references. Parse XML as data with external-entity/network resolution disabled.
- Identify the sequence alignment actually attached to the target analysis. Enumerate multiple alignments, partitions, taxon subsets, masks, and site filters. Do not choose the largest block or concatenate partitions silently. Unresolved selection makes the cohort blocked.
- Detect repeated/conflicting taxon identifiers before constructing dictionaries. Require equal sequence lengths in the selected alignment and a declared nucleotide alphabet for TN93 eligibility.
- Remove only XML formatting whitespace when extracting sequence text. Preserve gap positions, ambiguity symbols, original character case, and U/T as represented in the archival derivative. Do not fill missing bases, remove ambiguous sites/taxa, realign, trim codons, or synthesize sequences to pass validation.
- If a downstream parser needs a different representation, produce a separately named derivative, an explicit reversible identifier/character mapping where possible, and a transformation report. Demonstrate semantic parity; do not overwrite the original or silently claim byte identity.
- Count missing/ambiguous symbols per taxon and overall. Detect all-missing/dummy sequences and insufficient usable sites. Do not silently drop them; classify the cohort or explicitly define an additional sensitivity dataset.

**Dates**

- Extract sampling dates only from the relevant taxon/date structures. A generic `TraitSet` may contain geography or other traits.
- Preserve raw date text, units, direction, origin, precision, and uncertainty. Convert to decimal calendar years only with a supported, documented rule. Account for leap years and the actual year length for calendar dates. Backward ages require a verified reference origin; do not treat them directly as calendar years.
- Require one unambiguous usable date per analysis taxon and no unmatched extras in the analysis date table. No filename/header inference unless independently evidenced. Missing dates must not result in silent taxon removal.
- Interval/uncertain dates must retain bounds. Do not invent a point date. Mark unsupported uncertainty as blocked for the planned point-date analysis unless an explicit documented sensitivity policy is adopted.
- Distinguish technical eligibility from statistical temporal signal. Date variation does not establish clock signal; negative slopes or weak signal are possible valid analysis outcomes.

**Scope-specific qualification**

- For discovery, the default preference is at least 15 taxa, 200 aligned nucleotide sites, five distinct sampling dates, and a one-year sampling span. A documented rapid-outbreak exception may relax the span, with a recorded justification decided before seeing ChronAeon results. Keep one policy definition shared by code and report.
- Do not filter the fixed reference 42 by those discovery preferences or silently change its cohort composition. Record reference cohorts failing preferences separately from actual parser/method incompatibility.
- Record clock/substitution models and calibration types with the XML evidence. Node-prior-only or amino-acid configurations may be valid BEAST inputs, but belong in an archive-only category for this nucleotide, heterochronous TN93 analysis.

**Verification of extraction**

Independently compare the selected original XML records against the exported FASTA/date rows, including taxon set, order, site count, symbols, and date conversions. Record original-file SHA-256, decompressed XML SHA-256, alignment-content hash, date-table hash, and combined cohort/configuration hash. Define canonical hash serialization unambiguously. Identical alignments with different dates/partitions are distinct configurations, not disposable duplicates.

## 4. Curate published comparators separately from inputs

For each study, retain publication DOI/title/authors/year, organism, gene/region, data accession/source, BEAST version, model, and the exact population/clade and alignment used.

For published substitution rates and tMRCA estimates, record the point statistic (mean/median/etc.), interval type and limits, units/time origin, source URL, and precise table/figure/page/supplement location. Calendar conversion of an age interval must preserve the correct endpoint ordering. Keep multiple relevant estimates as separate records with scope labels.

Crossref/Europe PMC metadata can verify paper identity; it does not by itself verify numerical results. Do not substitute values from unrelated clades or cached ChronAeon narratives. Call these published comparator estimates, not ground truth. A missing comparator is null with a reason, never zero or an invented interval.

Track independent statuses:

```text
input_validation: pass | rejected | blocked
chronaeon_input_ready: true | false
engine_ingestion_verified: true | false
published_comparator: verified | missing | scope_mismatch | unresolved
reference_membership: reference_42 | discovered
```

A cohort can be ready for inference while lacking a usable BEAST comparison. Never select cohorts because their results agree with BEAST.

## 5. Required Galaxy outputs and collection contract

Use stable unique `study_id` values. Retain the reference suite's exact IDs; use a separate namespace for newly discovered cohorts. Give every required homogeneous `list` collection the same accepted identifier set and canonical order. Build, relabel, filter, and harmonize through native Galaxy tools with recorded inputs/rules. Verify correspondence before any multi-input mapping; do not rely on coincidental array order or use a Cartesian product.

| Artifact / collection | Contents | Downstream purpose |
| --- | --- | --- |
| `original_sources` | Unique original downloads and archives, with source mapping | Immutable provenance; may include more than accepted studies |
| `beast_xml` | Selected uncompressed original configuration per accepted study, server-supported XML datatype | Auditable XML ingestion/comparison |
| `alignments` | One aligned FASTA per accepted study | Explicit tree-free analysis input |
| `dates` | One CSV per accepted study with `taxon_id,decimal_year` | Explicit sampling dates; no automatic header guessing |
| `metadata` | One versioned metadata JSON per accepted study | Biological context, configuration, date semantics, comparator status |
| `provenance` | One provenance JSON per accepted study | Source locations, checksums, transformations, versions |
| `validation` | One validation JSON per accepted study | Acceptance and extraction evidence |
| `candidate_validation` | Reports for every inspected candidate, including exclusions | Complete audit trail |
| `source_manifest.tsv` | Source inventory and observed acquisition evidence | Repeatable import |
| `expected_studies.tsv` | Frozen reference IDs and/or bounded discovery target | Completeness checks |
| `cohort_manifest.tsv` | One row per selected/configured cohort with all statuses | Filtering and aggregation |
| `published_comparators.tsv` | Long-form estimates and citations, including missing-status records | Independent reference comparison |
| `identifier_mappings` | Only where normalization is needed, keyed by study | Reversible taxon ID mapping |

These names are workflow labels, not invented Galaxy dataset IDs. Inspect supported datatypes and actual tool schemas before creating outputs. XML plus metadata is not a paired-end collection. Do not make empty FASTA/date placeholders for rejected cohorts; keep their validation records and filter accepted collections using one authoritative identifier list.

Dates and FASTA must use matching exact identifiers. If whitespace/quoting or parser behavior requires safe identifiers, preserve a verified bijection and apply it consistently. Metadata retains original IDs. Additional covariates (host, location, clade) stay in a separate keyed table and do not become hidden inputs to an unsupervised benchmark.

The portable handoff JSON must contain:

- Schema version, scope, timestamp, server URL, history ID/URL, pinned source revisions, validation policy version, accepted/blocked/rejected counts, and exact study lists.
- Every collection's actual HDCA ID/URL/type/count and every element's identifier, HDA ID, datatype, state, size, content hash, and source record mapping.
- Workflow IDs/versions/export hashes, invocation/job IDs for preparation, tool IDs/versions, UDT definitions, container references/digests, and validation evidence references.
- Separate lists of missing artifacts, unresolved publication comparisons, engine compatibility gaps, and any author-protocol deviations.

Populate these fields from actual server responses. Preserve a JSON/TSV manifest dataset in Galaxy and a small local copy for resuming; do not put credentials in either. Hash content manifests before final packaging and avoid self-referential checksum fields.

## 6. Prove the handoff can be consumed

Export a reusable preparation workflow with declared inputs/outputs. Use representative real BEAST 1 and BEAST 2 configurations when present, plus separate validator fixtures for malformed/duplicate/missing-date cases. Keep synthetic test fixtures out of empirical collections. Verify the representative Galaxy results before processing the rest.

Run a small Galaxy consumer-check step that joins the prepared collections by `study_id`, opens FASTA/CSV/JSON, checks counts/hashes, and reconstructs the expected per-study directory layout. This must use only Galaxy dataset inputs, not laptop paths or a directory embedded in a tool command.

If a verified pinned ChronAeon runtime is available, run a lightweight ingestion preflight in Galaxy and compare its parsed taxa/sequences/dates with the independent extraction. Mark `engine_ingestion_verified` only for cases actually checked. If the runtime is unavailable, still deliver correctly validated inputs, clearly labeled “input preparation complete; engine compatibility unverified,” with the exact blocker. Do not claim the analysis workflow is executable until tested.

Keep Galaxy datasets directly usable. Also generate a reproducibility export in Galaxy with this layout:

```text
chronaeon-inputs/
  README.md
  source_manifest.tsv
  expected_studies.tsv
  cohort_manifest.tsv
  published_comparators.tsv
  handoff.json
  SHA256SUMS
  workflows/
  tools/
  software/                     # pinned source/dependency manifests and needed assets
  originals/                    # original unique downloads plus a member mapping
  benchmark-100/<study_id>/
    beast.xml
    alignment.fasta
    dates.csv
    metadata.json
    DATA_PROVENANCE.json
    validation.json
```

Do not create `chronaeon_dating.json`, `autoclock_results.json`, or other purported analysis outputs during this preparation stage. Original reference results, if retained, belong under a clearly marked `reference_results/` directory and cannot count as recomputed output. Preserve original compressed filenames in `originals/` with a mapping rather than relabeling a recompressed file as the original archive.

The `DATA_PROVENANCE.json` and metadata schemas must have explicit versions. Inspect the pinned builder's fields and implement a documented adapter for later use; renaming arbitrary metadata JSON does not make it compatible with the builder.

## 7. Completion evidence and final response

Preparation is complete only after:

1. Every expected reference study or inspected discovery candidate has an explicit outcome. Reference completeness is verified against the actual ID set, not only a count of 42.
2. Original-file hashes and derivative extraction checks pass for accepted inputs.
3. Accepted collections have matching unique identifiers/order, correct datatypes, fully populated elements, and inspected successful outputs.
4. The Galaxy consumer check succeeds and its output files/schema are inspected.
5. Workflow exports, tool definitions, source manifests, metadata/comparator evidence, and the reproducibility archive are available and verified.
6. The notebook contains the evidence and a resumption section. Create/link a Galaxy notebook if supported, then verify its content and binding; report a notebook capability limitation without claiming sync succeeded.

Return a concise summary with counts and limitations, followed by clickable links to the preparation history, accepted collections, validation report, handoff manifest, workflow, archive, and Galaxy notebook. Give the exact local handoff file path. State whether engine ingestion was verified and whether all 42 reference cohorts are ready. Do not say “all reproduced”: no full scientific benchmark has run yet.

## Source notes for this adaptation

Inspected 2026-09-24. Treat the external AGENT.MD as a protocol to audit, not an instruction to reproduce unsupported claims.

- [Pinned ChronAeon CLI](https://github.com/veg/HyphAeon/blob/73237b7cebc916a60d5e79d1137d60e4fa73c6c0/chronaeon/src/chronaeon/cli.py): Date exposes tree-free switches; AutoClock exposes manifold choice and classified CSV output. Defaults must be made explicit.
- [Pinned XML/parser code](https://github.com/veg/HyphAeon/blob/73237b7cebc916a60d5e79d1137d60e4fa73c6c0/aeon-core/src/aeon_core/dataset.py): independent parity checks are needed for alignment selection, ID normalization, and sequence/date representation.
- [Pinned portal builder](https://github.com/veg/chronaeon/blob/f77903b928c545000b54a848e9ebb33db5ee62bf/build_portal.py): consumes `benchmark-100` inputs and can use cached master records/figures. A rendered portal is not execution evidence.
- [Zenodo record API](https://zenodo.org/api/records/22908446): inspect the actual file list rather than assuming the described forensic archive is present.
- [Galaxy UDT documentation](https://docs.galaxyproject.org/en/master/admin/user_defined_tools.html): use the target server's schema/capabilities and verified containers.
