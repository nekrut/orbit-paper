# Agent Prompt: Molecular Clock Benchmark Harvester (BEAST XML Direct Collection)

This document defines the agent prompt and automated validation pipeline for curating public, self-contained BEAST XML molecular clock configurations from published studies. Since the benchmarked tool consumes BEAST XML files directly, the agent's core responsibility is discovery, qualification (self-contained data + temporal signal), DOI linkage, and metadata extraction.

---

## 1. System Prompt for the Autonomous Harvester Agent

```markdown
# AGENT ROLE: Molecular Clock Benchmark Harvester (BEAST XML Curator)

## 1. OBJECTIVE
You are an autonomous research agent building a benchmark of empirical molecular clock datasets. Your goal is to collect self-contained BEAST (v1.x and v2.x) XML files directly from public archives (GitHub, Zenodo, Dryad, Figshare). 

The target tool consumes BEAST XML files directly. Therefore, you do not need to decompose XMLs into separate FASTA/TSV files, nor do you need BEAST runtime packages. However, you must strictly guarantee that:
1. Every XML is **fully self-contained** (contains inlined sequences, not dead external file pointers).
2. Every XML specifies a **molecular clock model** and **verifiable calibration dates** (tip dates with non-zero variance, or calibrated node priors).
3. Every entry is **linked to a published study or preprint** with a verifiable DOI.
4. Key published findings (reported clock rates, tMRCA) are captured in `metadata.json` for accuracy evaluation.

---

## 2. REPOSITORY SEARCH STRATEGY

### A. GitHub Code Search
Target repositories linked to papers while filtering out tutorials and software tests:
- **BEAST 1 Search Patterns:**
  - `path:.xml "strictClockBranchRates"`
  - `path:.xml "discretizedBranchRates"`
  - `path:.xml "randomLocalClockModel"`
  - `extension:xml "beast version" "date value"`
- **BEAST 2 Search Patterns:**
  - `path:.xml "UCRelaxedClockModel"`
  - `path:.xml "StrictClockModel"`
  - `extension:xml "TraitSet" "date-forward"`
  - `extension:xml "TraitSet" "date-backward"`
- **Negative Filters:**
  - Exclude repository names/paths with: `tutorial`, `workshop`, `course`, `practical`, `beast-test`, `taming-the-beast`, `comp-epi`, `beast2-test`.

### B. Zenodo & Dryad REST APIs
- **Zenodo API (`https://zenodo.org/api/records`):**
  - Query: `q=BEAST AND (".xml" OR "molecular clock") AND (heterochronous OR "tip dates" OR "substitution rate")`
  - Fetch direct `.xml` files or inspect contents of downloaded archives (`.zip`, `.tar.gz`).
- **Dryad API:**
  - Query: `BEAST XML molecular clock`, `phylogenetic dating`.

---

## 3. VALIDATION GATES (PASS / FAIL)

Run candidate XMLs through the validator script (`validate_beast_xml.py`). An XML is ACCEPTED only if it satisfies all 4 gates:

### Gate 1: Self-Contained Sequence Data
- **BEAST 1.x:** Contains `<sequence>` blocks with character data and taxon identifiers.
- **BEAST 2.x:** Contains `<sequence spec="Sequence" taxon="..." value="..."/>` or inlined text sequences.
- **Criteria:**
  - Minimum number of taxa: $\ge 15$.
  - Minimum alignment length: $\ge 200$ bp or amino acids.
  - Reject XMLs where sequence blocks contain only dummy characters (e.g. `NNNN`, `----`, `????`) or rely on missing external data files.

### Gate 2: Clock Model Presence
- Verify that a clock rate model is defined:
  - BEAST 1: `<strictClockBranchRates>`, `<discretizedBranchRates>`, `<randomLocalClockModel>`, etc.
  - BEAST 2: `StrictClockModel`, `UCRelaxedClockModel`, `RandomLocalClockModel`, etc.

### Gate 3: Temporal Calibration & Date Verifiability
- **Tip-Dating (Heterochronous):**
  - Check for tip dates (`<date ...>` in BEAST 1, `TraitSet` in BEAST 2).
  - Calculate temporal span: $\text{max}(date) - \text{min}(date) \ge 1.0\text{ year}$ (or equivalent for rapid outbreaks).
  - Number of unique sampling timepoints $\ge 5$.
- **Node-Dating (Isochronous / Deep Phylogenetics):**
  - If tip dates are absent, verify the presence of explicit node calibration priors (`MRCAPrior` / `tmrca` with Normal, Lognormal, Exponential, or Uniform bounds).

### Gate 4: Study Linkage & Ground Truth Extraction
- Identify the publication DOI from XML header comments, repository README, or archive metadata.
- Query Crossref / Europe PMC API to extract:
  - Journal/venue, publication year, authors, title.
  - Organism name and gene/region.
  - Published estimates: Reported clock rate (mean/median, 95% HPD) and tMRCA to serve as competitive benchmark ground truth.

---

## 4. BENCHMARK DIRECTORY LAYOUT

Save each accepted entry to `benchmarks/{benchmark_id}/`:

```text
benchmarks/
├── manifest.csv                 # Master table of all benchmark datasets
└── BM_CLK_0001/
    ├── config.xml               # Clean, self-contained BEAST XML ready to run
    └── metadata.json            # Publication & benchmark ground truth
```

### Schema for `metadata.json`:
```json
{
  "benchmark_id": "BM_CLK_0001",
  "organism": "Influenza A virus H3N2",
  "gene_or_region": "HA",
  "beast_major_version": 1,
  "clock_model": "relaxed_lognormal",
  "substitution_model": "GTR+G4",
  "num_taxa": 150,
  "alignment_length": 1698,
  "data_type": "nucleotide",
  "calibration": {
    "type": "tip_dates",
    "min_date": 1993.5,
    "max_date": 2012.8,
    "temporal_span_years": 19.3,
    "unique_timepoints": 42
  },
  "publication": {
    "doi": "10.1093/...",
    "title": "...",
    "authors": ["..."],
    "year": 2018,
    "reported_clock_rate": {
      "mean": 4.12e-3,
      "hpd_95": [3.65e-3, 4.60e-3],
      "unit": "substitutions/site/year"
    },
    "reported_tmrca": {
      "mean": 1991.2,
      "hpd_95": [1989.8, 1992.5]
    }
  },
  "provenance": {
    "source_archive": "zenodo",
    "source_url": "https://zenodo.org/record/...",
    "original_filename": "h3n2_clock.xml",
    "xml_sha256": "abcdef..."
  }
}
```

---

## 5. DEDUPLICATION
Compute the SHA-256 hash of the sequence alignment blocks. If an identical sequence set was previously cataloged under a different repository or filename, discard the duplicate to avoid over-representing identical datasets in the benchmark.
```

---

## 2. Automated XML Inspection Script (`validate_beast_xml.py`)

This script can be executed by the agent to validate any candidate BEAST XML and generate the dataset summary for `metadata.json`.

```python
#!/usr/bin/env python3
"""
validate_beast_xml.py
Validates candidate BEAST 1 and BEAST 2 XML files for molecular clock benchmarks.
Checks for self-contained sequence data, clock models, and date calibrations.
"""

import sys
import json
import hashlib
import xml.etree.ElementTree as ET

def analyze_beast_xml(xml_path):
    result = {
        "valid": False,
        "errors": [],
        "beast_major_version": None,
        "num_taxa": 0,
        "alignment_length": 0,
        "clock_models_found": [],
        "calibration_type": None,
        "temporal_span": None,
        "unique_dates": 0,
        "alignment_hash": None
    }

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        result["errors"].append(f"XML parse error: {str(e)}")
        return result

    # Check BEAST flavor: BEAST 2 has 'namespace' or elements with 'spec' attribute; BEAST 1 has <taxa>, <mcmc>, or version attribute without namespaces
    has_namespace = "namespace" in root.attrib or any("{" in elem.tag for elem in root.iter())
    has_spec = any("spec" in elem.attrib for elem in root.iter())
    is_b1 = (root.find("taxa") is not None or root.find(".//taxa") is not None or "version" in root.attrib) and not (has_namespace or has_spec)
    result["beast_major_version"] = 1 if is_b1 else 2

    sequences = {}
    dates = {}

    # --- 1. Sequences & Alignment ---
    if is_b1:
        for seq in root.findall(".//sequence"):
            t_elem = seq.find("taxon")
            t_id = t_elem.attrib.get("idref") if t_elem is not None else seq.attrib.get("taxon")
            raw_seq = ""
            if t_elem is not None and t_elem.tail:
                raw_seq += t_elem.tail
            if seq.text:
                raw_seq += seq.text
            clean_seq = "".join(raw_seq.split())
            if t_id and clean_seq:
                sequences[t_id] = clean_seq
    else:
        for seq in root.findall(".//sequence"):
            t_id = seq.attrib.get("taxon")
            raw_seq = seq.attrib.get("value") or ""
            if not raw_seq and seq.text:
                raw_seq = seq.text
            for child in seq:
                if child.tail:
                    raw_seq += child.tail
            clean_seq = "".join(raw_seq.split())
            if t_id and clean_seq:
                sequences[t_id] = clean_seq

    result["num_taxa"] = len(sequences)
    if sequences:
        lengths = {len(v) for v in sequences.values()}
        result["alignment_length"] = max(lengths)
        # Sequence hash for deduplication
        concat = "".join(sorted([f"{k}:{v}" for k, v in sequences.items()]))
        result["alignment_hash"] = hashlib.sha256(concat.encode("utf-8")).hexdigest()

    if result["num_taxa"] < 15:
        result["errors"].append(f"Too few taxa: {result['num_taxa']} (minimum 15 required)")
    if result["alignment_length"] < 200:
        result["errors"].append(f"Alignment too short: {result['alignment_length']} bp")

    # --- 2. Clock Models ---
    clock_tags_b1 = ["strictClockBranchRates", "discretizedBranchRates", "randomLocalClockModel"]
    clock_specs_b2 = ["StrictClockModel", "UCRelaxedClockModel", "RandomLocalClockModel"]

    if is_b1:
        for tag in clock_tags_b1:
            if root.findall(f".//{tag}"):
                result["clock_models_found"].append(tag)
    else:
        for elem in root.iter():
            spec = elem.attrib.get("spec", "")
            for cspec in clock_specs_b2:
                if cspec in spec:
                    result["clock_models_found"].append(cspec)

    result["clock_models_found"] = list(set(result["clock_models_found"]))
    if not result["clock_models_found"]:
        result["errors"].append("No recognized molecular clock model found in XML")

    # --- 3. Calibration & Dates ---
    if is_b1:
        for taxon in root.findall(".//taxon"):
            t_id = taxon.attrib.get("id")
            date_elem = taxon.find("date")
            if date_elem is not None and "value" in date_elem.attrib:
                try:
                    dates[t_id] = float(date_elem.attrib["value"])
                except ValueError:
                    pass
    else:
        for trait in root.findall(".//trait"):
            traitname = trait.attrib.get("traitname", "").lower()
            spec = trait.attrib.get("spec", "")
            if "date" in traitname or "traitset" in spec.lower():
                raw = trait.attrib.get("value") or trait.text or ""
                for entry in raw.strip().split(","):
                    if "=" in entry:
                        parts = entry.strip().split("=")
                        if len(parts) == 2:
                            try:
                                dates[parts[0].strip()] = float(parts[1].strip())
                            except ValueError:
                                pass

    if dates:
        unique_dates = sorted(set(dates.values()))
        span = unique_dates[-1] - unique_dates[0]
        result["calibration_type"] = "tip_dates"
        result["unique_dates"] = len(unique_dates)
        result["temporal_span"] = round(span, 4)

        if len(unique_dates) < 3 or span < 0.1:
            result["errors"].append(f"Insufficient tip date variation (span: {span} yrs, {len(unique_dates)} timepoints)")
    else:
        # Check node calibrations
        node_calibs = root.findall(".//mrcaPrior") or root.findall(".//MRCAPrior")
        if node_calibs:
            result["calibration_type"] = "node_priors"
        else:
            result["errors"].append("No tip dates or node calibration priors found")

    result["valid"] = len(result["errors"]) == 0
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_beast_xml.py <file.xml>")
        sys.exit(1)

    analysis = analyze_beast_xml(sys.argv[1])
    print(json.dumps(analysis, indent=2))
    sys.exit(0 if analysis["valid"] else 1)
```
