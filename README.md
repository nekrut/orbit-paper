# Orbit LLM reanalysis: eight frontier models, one dataset

This repository captures a controlled experiment in which **eight frontier models** each drove a [Loom **orbit**](https://github.com/galaxyproject/loom) session to independently reanalyze the **same** RNA-seq dataset, then a cross-model analysis of how they did and what broke.

The dataset is the bulk RNA-seq from **Santana et al. 2023, *Science*** — *"A Candida auris–specific adhesin, Scf1, governs surface association, colonization, and virulence"* (PMC11235122; BioProject `PRJNA904261`). Each run was tasked to reproduce two `DESeq2` contrasts on the current B8441 v3 assembly (`GCA_002759435.3`), bridge v3↔v2 gene IDs, and recreate a Fig. 1D-analog volcano plot with SCF1 highlighted.

## Contents

| Path | What |
|---|---|
| [`orbit_llm_reanalysis_report.md`](orbit_llm_reanalysis_report.md) | Full report: model comparison + shortcomings of orbit / Galaxy / Galaxy MCP / BRC MCP + actionable recommendations |
| [`GALAXY_HISTORIES.md`](GALAXY_HISTORIES.md) | Table mapping each run to its Galaxy history (name + ID + link) |
| [`scf1_expression_across_attempts.png`](scf1_expression_across_attempts.png) / `.pdf` | Figure: SCF1 log2FC and per-sample expression across attempts |
| [`plot_scf1_across_attempts.py`](plot_scf1_across_attempts.py) | Script that regenerates the figure |
| [`runs/<model>/`](runs) | Each run's working directory: `notebook.md` (narrative + provenance), `activity.jsonl` (turn-by-turn event log), and produced artifacts (DE tables, volcano plots, reports) |

## The runs at a glance

Six of eight runs completed and reproduced the central finding (SCF1 = v3 `B9J08_03708`, strongly down: log2FC ≈ −6.8 to −7.4); `gpt` (1st attempt) and `haiku` aborted at data preparation.

| Model | Outcome | SCF1 | Deliverables | Cost | Errors |
|---|---|---|---|---|---|
| opus | Completed; both contrasts | reproduced | volcano + PDF | $131.83 | 7 |
| sonnet | Completed; both contrasts | reproduced | volcano + PDF | $24.87 | 16 |
| gpt (1st) | Failed; stalled at data prep | — | none | — | 10 |
| gpt2 | Completed (after naive-ID trap) | reproduced | volcano + PDF | $23.46 | 11 |
| gemini-2.5-pro | Completed; both contrasts | reproduced | text + PDF | $16.22 | 45 |
| gemini-3.5-flash | Completed; both contrasts | reproduced | volcano + PDF | $17.31 | 15 |
| deepseek | Completed; all steps | reproduced | notebook + HTML | $2.82 | 28 |
| haiku | Failed; aborted in ~3 min | — | none | — | 3 |

Models (provider): opus = `claude-opus-4-7`, sonnet = `claude-sonnet-4-6`, haiku = `claude-haiku-4-5` (Anthropic); **gpt and gpt2 both = `gpt-5.5`** (OpenAI, via the Codex provider — `openai-codex`/`codex-responses`); gemini-2.5-pro and gemini-3.5-flash (Google); deepseek.

The central scientific pitfall: the paper's v2 6-digit locus tags were **silently re-numbered** in v3, so the naive zero-strip guess (`B9J08_001458` → `B9J08_01458`) maps SCF1 to the wrong gene and yields a false negative. The correct bridge is protein reciprocal-best-hit (DIAMOND): `B9J08_001458` → `B9J08_03708`. See the [report](orbit_llm_reanalysis_report.md) for the full breakdown.

Findings from this experiment were filed as issues/comments on [`galaxyproject/loom`](https://github.com/galaxyproject/loom/issues) (#215–#220 and comments on #150, #210, #209, #186, #199, #23, #21, #75).

## Notes on the data

- **Redaction:** one run's `activity.jsonl` had written a literal Galaxy API key into a shell command; all occurrences were replaced with `REDACTED_GALAXY_API_KEY`. (The key has been rotated.)
- **Excluded:** per-run `.loom/env/` conda environments (hundreds of MB of binaries) and `session.jsonl` (symlinks to external raw session transcripts) are **not** included.
- `activity.jsonl` is the ground-truth event log (`user.prompt`, `tool.start`/`tool.end`, `guard.decision`); `notebook.md` is the polished narrative with `loom-session`/`loom-invocation` provenance blocks.

## Regenerate the figure

```bash
python3 plot_scf1_across_attempts.py   # needs matplotlib + numpy
```
