# Orbit continuation prompt: run ChronAeon from prepared Galaxy inputs

Use this only after the preparation prompt has produced a handoff manifest. Supplying this prompt authorizes the main cohort analysis; the preparation prompt alone does not.

## Objective

Use the verified Galaxy input package recorded in this project's notebook and `handoff.json` to run ChronAeon Date with LOOCV/nonlinear clocks, AutoClock, diagnostic figures, reference comparisons, and a reproducible report bundle. Execute all scientific processing and figure/portal generation in Galaxy. Keep the main conversation informed and record verified outcomes in the notebook.

Use the handoff's explicit scope. Preserve separate results for the published reference set and newly discovered cohorts. Do not silently add surveillance challenges, BEAST MCMC reruns, new datasets, public sharing, or GitHub Pages deployment.

## 1. Reopen and verify the handoff

Read the recorded Galaxy server/history, exact cohort IDs, collection mappings, workflow/tool definitions, hashes, and unresolved issues. Verify access and dataset/collection states. Resolve recorded prerequisites before submitting dependent work; do not repeat acquisition or overwrite previous results unnecessarily.

Create or reuse a dedicated analysis history, referencing/copying existing Galaxy datasets through native Galaxy operations with provenance. Use a parameterized Galaxy workflow whose inputs are the prepared collections and explicit software/method configuration. A fresh workflow invocation must be able to run without laptop paths or prior chat context.

If preparation exists but engine compatibility remains unverified, resolve that first. Never treat input readiness as proof that the engine ran correctly.

## 2. Pin and smoke-test the actual runtime in Galaxy

Prefer installed tools with appropriate functionality; otherwise create versioned UDTs for missing engine/preflight/aggregation/plotting functions. Use verified Linux-compatible containers and complete dependencies pinned to the recorded engine revision. Record package versions, image digest, Python/platform information, source changes, CPU/thread limits, and any model weights. Do not assume Apple MPS is available or install dependencies from the internet at job runtime.

Run import checks and `date --help` / `autoclock --help` in Galaxy and retain the output. Check the actual JSON/CSV schemas against downstream consumers. Run one small real cohort end to end before mapping the full input set. Inspect scientific output content as well as job success; fix an identified problem once and rerun only the affected test before expanding.

Default method for the supplied TN93-only protocol: explicit tree-free TN93 on CPU. The inspected engine's AutoClock default was `transformer`, and Date could ingest a starting tree from XML. Explicit arguments and log/result inspection must establish the chosen mode.

If historical published results used a transformer, classify the TN93 run as a method variant unless equivalence is demonstrated. An exact historical-engine reproduction requires documented method/weights/version provenance. Do not silently switch models to obtain agreement.

## 3. Workflow steps and command contracts

Use synchronized collection mapping: the alignment, dates, metadata, and provenance for a study must arrive together. Verify identifiers before launching mapped steps; avoid accidental cross-products. Each cohort is an independent Galaxy job per analysis step, allowing scheduler concurrency and targeted recovery. Do not run the entire 42-study suite inside one opaque shell loop.

The following are command contracts for the pinned runtime, to be confirmed by its help and smoke run. UDTs must substitute actual Galaxy input paths safely and claim fixed output files through their supported output definitions. These are not laptop commands.

**Date, LOOCV, and nonlinear clocks:**

```sh
python3 -m chronaeon.cli date \
  -a alignment.fasta -d dates.csv \
  --strain-col taxon_id --date-col decimal_year \
  --no-tree --distance-mode tn93 --cpu \
  --loocv --nonlinear-clocks \
  -o chronaeon_dating.json -c chronaeon_dating.csv
```

**AutoClock with explicit TN93 and classified metadata:**

```sh
python3 -m chronaeon.cli autoclock \
  -a alignment.fasta -d dates.csv \
  --strain-col taxon_id --date-col decimal_year \
  --manifold tn93 --device cpu -k 6 \
  --output-dir clock_communities \
  -o autoclock_results.json -c autoclock_classified_metadata.csv
```

Use the verified FASTA/date interface by default to avoid implicit XML alignment/date selection. Where native XML ingestion is verified, a documented alternative may use `--beast` with explicit tree-free settings and verified dates. Compare its parsed inputs with the preparation manifest. Do not label a representation-changing fallback an identical-input reproduction without evidence.

Capture stdout/stderr, exit code, effective arguments, engine version, elapsed process time, allocated resources, and input/output hashes as Galaxy outputs. A logging pipeline must not mask a nonzero engine exit code. Record any randomness and supported seed controls; do not invent a `--seed` flag. Keep the original engine result JSON and make a separate strict-JSON summary if non-finite values need normalization, with explicit missing/unbounded reasons rather than zeros.

Required workflow outputs per study:

- Date JSON, per-taxon CSV, and log.
- AutoClock JSON, classified metadata CSV, and log; claimed community outputs or a verified archive of them where needed.
- Run provenance/timing and semantic validation JSON.
- Per-study comparison record, four-panel diagnostic PNG/PDF or a documented partial-panel report.

Preserve matching study identifiers across output collections. Aggregation/plotting steps consume explicit Galaxy inputs, not files discovered from a previous job's working directory.

## 4. Scientific verification before aggregation

Confirm every intended study has a recorded successful, failed, blocked, or scientifically inconclusive outcome. Validate output schemas and per-taxon coverage against the input manifest; detect dropped/reordered taxa and missing community assignments. Match community membership by taxon ID. Do not replace a missing membership file with community zero.

Report the actual calculated estimates and intervals, selected models, available temporal-signal statistics, LOOCV metrics and units, outlier flags, and AutoClock memberships/rates. If a promised quantity is absent from the tested engine, mark it unavailable or add a separately documented implementation; never infer that it was computed from a successful exit code.

An unbounded interval, nonpositive slope, weak temporal signal, or lack of agreement with BEAST is a scientific result, not a trigger to tune the analysis until it agrees. Explanations such as stem-versus-crown or lineage mixture require evidence. Describe uncertainty as reported; a Fieller confidence interval is not a BEAST posterior HPD interval.

Before comparing numbers, verify matched taxa/loci, population/clade scope, time origin, units, and reference statistic. Preserve `discordant`, `inconclusive`, `reference_missing`, and `not_comparable` categories in addition to any supported concordance labels. Report interval overlap as overlap, not proof of method validity or statistical equivalence. Do not select AutoClock communities or nonlinear models post hoc solely for agreement with a published date.

Record tolerances before comparing repeated numerical results. Separate algorithmic repeatability from independent Orbit-session reliability. Community labels may be permuted; compare memberships with label-invariant matching. Do not demand byte-identical plots/JSON across platforms or turn reported Apple Silicon runtimes into universal Galaxy acceptance limits.

## 5. Fresh figures and compendium generation in Galaxy

Build a checked adapter that assembles the pinned builder's expected `benchmark-100/<study_id>/` inputs from the actual Galaxy output collections, joined by identifier. Validate all required JSON fields and CSV columns; retain the adapter source and version as provenance.

Use fresh output locations. Do not allow the builder's missing-input fallback to cached `benchmarks_master.json`, reuse committed reference figures, substitute old result values, or invent default community assignments. Retain reference master records separately for comparison. Reconstruct or patch the presentation builder explicitly where needed, record a source diff, and identify the result as an adapted Galaxy report rather than an unchanged historical build.

The four panels should show only supported data: clock fits and reference estimates; genuine LOOCV predictions; a clearly labeled manifold visualization with verified communities; and the supported community flow summary. A manifold graphic is not an inferred phylogenetic tree, and a visualization alone does not establish demographic history. Explain omitted/unavailable panels instead of drawing invented results.

Generate:

- Aggregate machine-readable result and validation tables.
- Individual PNG/PDF figures and HTML/Markdown study reports as Galaxy datasets or output collections.
- A static portal archive with all required relative assets, per-study inputs/results/provenance, and SHA256SUMS.
- A Galaxy notebook/report linking the actual input histories, workflow/invocation, result datasets, figures, and downloadable archive.

A UDT cannot be assumed to support composite HTML `extra_files`, and Galaxy may restrict JavaScript. Verify the site's supported display mechanism. Always provide individually accessible outputs and a downloadable site archive; an externally hosted website is a separate task. Build and static-link checks must run in Galaxy; browser inspection is a UI verification step, not local scientific execution.

## 6. Completion and recovery

Verify the exact expected study-ID set, successful output schemas, image readability, matching figure/result provenance, archive contents/checksums, internal relative links, and report completeness. Render representative reports visually, including successful, missing-reference, and inconclusive cases if present. Checking only HTML headings or PNG file size does not validate the science.

If a job fails, inspect its actual inputs, logs, and resources, explain the failure, and retry only a justified affected step. For a timed-out submission, check whether Galaxy created it before resubmitting. Preserve failed evidence. Do not automatically remove outliers or repeat successful jobs to hide failures.

Report queue/container startup time separately from engine compute time and whole-workflow wall time. Disclose deviations from the external protocol and unresolved historical source/engine provenance. A result is “42/42 recomputed” only when all 42 specific reference cohorts were actually run and verified; otherwise report the exact completion denominator.

Update the local and linked Galaxy notebooks with evidence and concise interpretation. End with clickable links to the workflow/invocation, results collections, aggregate comparison, figures, validation report, and portable archive. State which parts were reproduced, adapted, unsupported, or inconclusive.

## Optional future surveillance extension — excluded from this run

If later requested, prepare Nextstrain and BV-BRC as separate workflows and frozen input snapshots with dates, checksums, provenance, and resource estimates. Check archive availability and API access rather than assuming current feeds match historical counts/results. Reconstructing sequences by traversing an Auspice tree is not globally tree-free ingestion; disclose that provenance or use authentic sequence inputs. Do not synthesize missing sequence states.

BV-BRC cleaning must explicitly produce a matching cleaned metadata table by exact sequence IDs before AutoClock. Define disjoint anchors/evaluation streams when testing generalization, or label same-set triage accurately. Community numbers are arbitrary, and host annotations used for biological interpretation must remain independent of unsupervised fitting. Assess memory and job limits before 10k–50k runs. Published latency/community expectations are reference claims, not guaranteed outcomes for live feeds or shared Galaxy hardware.
