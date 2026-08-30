# Genomic Variant Analysis Toolkit

<p align="center">
  <strong>Small Python utilities for FASTA sequence editing, SnpEff annotation parsing, and experimental variant ranking.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/Status-Prototype-orange.svg" alt="Prototype">
  <img src="https://img.shields.io/badge/Use-Research%20%26%20Education-lightgrey.svg" alt="Research and Education">
  <img src="https://img.shields.io/badge/Clinical%20Use-Not%20Validated-red.svg" alt="Not validated for clinical use">
</p>

<p align="center">
  Developed by <strong>Edward Ying</strong><br>
  Imperial College London
</p>

---

## Overview

The **Genomic Variant Analysis Toolkit** contains three Python scripts covering a simple genomics workflow:

1. Introduce a nucleotide substitution into a FASTA sequence.
2. Extract transcript-level annotations from a SnpEff-annotated VCF file.
3. Rank annotated variants using an experimental heuristic score.

The repository is intended for:

* Bioinformatics teaching
* Genomics practicals
* Research prototyping
* Variant-table exploration
* Early-stage pipeline development

> [!CAUTION]
> This repository is a prototype. It is not clinically validated and must not be used for diagnosis, treatment, patient management, or formal variant classification.

---

## Table of Contents

* [Features](#features)
* [Repository Structure](#repository-structure)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [FASTA Nucleotide Editor](#fasta-nucleotide-editor)
* [SnpEff Annotation Parser](#snpeff-annotation-parser)
* [Variant Prioritization Prototype](#variant-prioritization-prototype)
* [Current Limitations](#current-limitations)
* [Suggested Repository Setup](#suggested-repository-setup)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [References](#references)
* [Disclaimer](#disclaimer)
* [Author](#author)

---

## Features

### FASTA sequence editing

* Reads a FASTA file interactively
* Preserves the first FASTA header
* Joins multi-line sequence content
* Converts sequence characters to uppercase
* Replaces a nucleotide using 1-based indexing
* Writes the modified sequence to a new file

### SnpEff annotation parsing

* Reads a SnpEff-annotated VCF file
* Filters records by an inclusive genomic interval
* Parses the SnpEff `ANN` field
* Reports one row per transcript annotation
* Extracts selected VCF and SnpEff fields
* Supports effect, impact, and dbSNP filters
* Writes tab-separated output

### Experimental variant ranking

* Runs the annotation parser through a subprocess
* Loads the resulting TSV with pandas
* Scores variants using allele frequency, SnpEff impact, optional ClinVar status, and limited protein-domain information
* Sorts variants by score
* Assigns heuristic interpretation labels

---

## Repository Structure

The scripts should use the following filenames:

```text
genomic-variant-analysis-toolkit/
├── Introduce_nucleotide_change.py
├── Variant_Annotation.py
├── Variant_Prioritization_Engine.py
└── README.md
```

| File                               | Current purpose                                             |
| ---------------------------------- | ----------------------------------------------------------- |
| `Introduce_nucleotide_change.py`   | Introduces one nucleotide replacement into a FASTA sequence |
| `Variant_Annotation.py`            | Parses selected fields from a SnpEff-annotated VCF          |
| `Variant_Prioritization_Engine.py` | Applies an experimental score to the annotation output      |
| `README.md`                        | Repository documentation                                    |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/genomic-variant-analysis-toolkit.git
cd genomic-variant-analysis-toolkit
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install the current dependency

```bash
pip install pandas
```

`Introduce_nucleotide_change.py` and `Variant_Annotation.py` use only the Python standard library.

`Variant_Prioritization_Engine.py` imports `requests`, but the external API functions are not yet implemented. Installing it is therefore optional for the current code:

```bash
pip install requests
```

A matching `requirements.txt` could contain:

```text
pandas
requests
```

---

## Quick Start

### Modify a FASTA sequence

```bash
python Introduce_nucleotide_change.py
```

### Parse a SnpEff-annotated VCF

```bash
python Variant_Annotation.py \
    input.vcf \
    11089462 \
    11133820 \
    --output annotations.tsv
```

### Use the prioritizer from Python

```python
from Variant_Prioritization_Engine import VariantPrioritizer

prioritizer = VariantPrioritizer()

results = prioritizer.prioritize(
    vcf_file="input.vcf",
    gene_start=11089462,
    gene_end=11133820,
    patient_id="Sample-001",
)

print(
    results[
        [
            "Gene_Name",
            "HGVS_p",
            "priority_score",
            "acmg_classification",
        ]
    ].head()
)
```

The input VCF must already contain SnpEff `ANN` annotations.

---

# FASTA Nucleotide Editor

## Purpose

`Introduce_nucleotide_change.py` performs one nucleotide replacement in a FASTA sequence.

It can support simple tasks such as:

* In silico mutagenesis
* Sequence-manipulation exercises
* Preparing candidate mutant sequences
* Teaching 1-based versus 0-based indexing

---

## Usage

```bash
python Introduce_nucleotide_change.py
```

The script prompts for:

```text
Input FASTA file path:
Output FASTA file path:
Position to change:
New nucleotide:
```

The supplied position uses **1-based indexing**.

---

## Example

Input file:

```fasta
>example_sequence
ATGCAAGTCC
```

Example interaction:

```text
Input FASTA file path: example.fasta
Output FASTA file path: example_mutant.fasta
Position to change: 5
New nucleotide: T
```

Output:

```fasta
>example_sequence
ATGCTAGTCC
```

At position 5, the original `A` is replaced by `T`.

---

## Current Behaviour

The script:

1. Reads every line from the input file.
2. Treats the first line as the FASTA header.
3. Joins all remaining lines into one sequence.
4. Converts the sequence to uppercase.
5. Replaces the character at `position - 1`.
6. writes the original header followed by the modified sequence.

---

## Important Limitations

The current implementation does not check whether:

* The input file is empty
* The first line is a valid FASTA header
* The requested position is within the sequence
* The position is positive
* The replacement is exactly one character
* The replacement is one of `A`, `C`, `G`, or `T`
* The nucleotide at the position matches an expected reference allele

The script also writes the full sequence on one line and does not add a final newline after the sequence.

> [!WARNING]
> An out-of-range position may produce an unintended sequence rather than a clear validation error. Inspect the output before using it downstream.

---

# SnpEff Annotation Parser

## Purpose

`Variant_Annotation.py` extracts selected transcript-level annotations from a SnpEff-annotated VCF file and writes them to a TSV file.

---

## Requirements

* Python 3.7 or later
* A tab-delimited VCF file
* A SnpEff `ANN` field in the VCF `INFO` column

No third-party Python package is required.

---

## Command Syntax

```bash
python Variant_Annotation.py \
    <vcf_file> \
    <gene_start> \
    <gene_end> \
    [options]
```

---

## Arguments

| Argument         | Required | Description                                                        |
| ---------------- | :------: | ------------------------------------------------------------------ |
| `vcf_file`       |    Yes   | Path to the annotated VCF file                                     |
| `gene_start`     |    Yes   | Inclusive interval start                                           |
| `gene_end`       |    Yes   | Inclusive interval end                                             |
| `-o`, `--output` |    No    | Output TSV path                                                    |
| `--effect`       |    No    | Retain annotations containing the supplied effect text             |
| `--impact`       |    No    | Retain annotations whose impact exactly matches the supplied value |
| `--only-rs`      |    No    | Retain records whose VCF ID begins with `rs`                       |

Default output:

```text
improved_snp_annotations.tsv
```

---

## Examples

### Extract every annotated record in an interval

```bash
python Variant_Annotation.py \
    input.vcf \
    11089462 \
    11133820
```

### Extract missense annotations

```bash
python Variant_Annotation.py \
    input.vcf \
    11089462 \
    11133820 \
    --effect missense_variant \
    --output missense.tsv
```

### Extract exact `HIGH` impact annotations

```bash
python Variant_Annotation.py \
    input.vcf \
    11089462 \
    11133820 \
    --impact HIGH \
    --output high_impact.tsv
```

### Retain records with dbSNP-style IDs

```bash
python Variant_Annotation.py \
    input.vcf \
    11089462 \
    11133820 \
    --only-rs \
    --output known_variants.tsv
```

### Combine filters

```bash
python Variant_Annotation.py \
    input.vcf \
    11089462 \
    11133820 \
    --effect missense_variant \
    --impact MODERATE \
    --only-rs \
    --output known_moderate_missense.tsv
```

---

## Output Columns

| Column               | Source                         |
| -------------------- | ------------------------------ |
| `CHROM`              | VCF column                     |
| `POS`                | VCF column                     |
| `ID`                 | VCF column                     |
| `REF`                | VCF column                     |
| `ALT`                | VCF column                     |
| `QUAL`               | VCF column                     |
| `FILTER`             | VCF column                     |
| `DP`                 | VCF `INFO` field, when present |
| `AF`                 | VCF `INFO` field, when present |
| `Effect`             | SnpEff `ANN` field             |
| `Impact`             | SnpEff `ANN` field             |
| `Gene_Name`          | SnpEff `ANN` field             |
| `Transcript_ID`      | SnpEff `ANN` field             |
| `Transcript_Biotype` | SnpEff `ANN` field             |
| `HGVS_c`             | SnpEff `ANN` field             |
| `HGVS_p`             | SnpEff `ANN` field             |
| `Protein_position`   | SnpEff `ANN` field             |

---

## Transcript Handling

The SnpEff `ANN` value may contain several comma-separated annotations.

The parser writes each annotation as a separate TSV row:

```text
one genomic variant
├── transcript annotation 1
├── transcript annotation 2
└── transcript annotation 3
```

Repeated genomic coordinates in the output are therefore expected.

---

## Filter Behaviour

### Effect filter

The effect filter uses substring matching:

```python
if args.effect and args.effect not in effect:
    continue
```

For example:

```bash
--effect missense
```

can match:

```text
missense_variant
```

### Impact filter

The impact filter uses exact string matching:

```bash
--impact HIGH
```

does not match `MODERATE`, `LOW`, or differently capitalized values.

### dbSNP filter

`--only-rs` retains a record only when its VCF ID starts with:

```text
rs
```

It does not query dbSNP or verify the identifier online.

---

## Current Assumptions and Limitations

The parser currently assumes:

* Each non-header line has at least eight VCF columns
* `POS` can be converted to an integer
* The `INFO` field uses semicolon-separated entries
* The SnpEff `ANN` structure follows the hard-coded field order
* `DP` and `AF`, when present, are stored in the `INFO` column
* Region filtering by position alone is sufficient
* No chromosome argument is needed

Additional limitations include:

* The parser does not filter by chromosome.
* It does not validate `gene_start <= gene_end`.
* It does not explicitly handle malformed VCF rows.
* It does not normalize variants.
* It does not split multiallelic ALT values.
* It does not pair ALT alleles with their corresponding annotations.
* It does not inspect FORMAT or sample genotype columns.
* It does not parse allele-specific `AF` values.
* It silently skips records without `ANN`.
* Extra SnpEff annotation fields beyond the configured list are ignored.
* Missing fields are padded with empty strings.

---

# Variant Prioritization Prototype

## Purpose

`Variant_Prioritization_Engine.py` demonstrates how annotation output can be ranked with a simple, transparent heuristic score.

It should be considered a **prototype and teaching example**, not a complete clinical prioritization system.

---

## Pipeline

```mermaid
flowchart LR
    A[SnpEff-annotated VCF] --> B[Variant_Annotation.py]
    B --> C[temp_annotations.tsv]
    C --> D[VariantPrioritizer]
    D --> E[Heuristic scores]
    E --> F[Sorted pandas DataFrame]
```

The annotation step is executed using:

```text
python Variant_Annotation.py <VCF> <START> <END> -o temp_annotations.tsv
```

The temporary output filename is fixed as:

```text
temp_annotations.tsv
```

---

## Implemented Scoring Components

### Population allele frequency

| Condition     | Points |
| ------------- | -----: |
| `AF < 0.0001` |     30 |
| `AF < 0.01`   |     20 |
| `AF < 0.05`   |     10 |
| Otherwise     |      0 |

A missing or empty `AF` is converted to `1.0`, giving zero rarity points.

### SnpEff impact

| Impact     | Points |
| ---------- | -----: |
| `HIGH`     |     25 |
| `MODERATE` |     15 |
| `LOW`      |      5 |
| `MODIFIER` |      0 |

### Optional ClinVar-style status

The scorer checks for a column named:

```text
clinvar_status
```

| Exact value              | Points |
| ------------------------ | -----: |
| `Pathogenic`             |     30 |
| `Likely Pathogenic`      |     20 |
| Anything else or missing |      0 |

The current annotation parser does not generate this column, and the ClinVar query function is not implemented. Consequently, normal pipeline output receives no ClinVar points.

### Hard-coded protein domains

The code currently contains only these example ranges:

| Gene    | Domain        | Inclusive amino-acid range |
| ------- | ------------- | -------------------------: |
| `BRCA1` | `zinc_finger` |                      1–100 |
| `BRCA1` | `BRCT`        |                  1600–1863 |
| `TP53`  | `DNA_binding` |                    100–300 |

A variant within one of these ranges receives 15 points.

No other genes or domains are currently supported.

### Literature evidence

Literature scoring is commented out and contributes no points.

---

## Heuristic Labels

After scoring, the script assigns the following labels:

|  Score | Output label                        |
| -----: | ----------------------------------- |
| 80–100 | `Pathogenic`                        |
|  60–79 | `Likely Pathogenic`                 |
|  40–59 | `Variant of Uncertain Significance` |
|  20–39 | `Likely Benign`                     |
|   0–19 | `Benign`                            |

> [!CAUTION]
> These are score-band labels only. They are not evidence-based ACMG/AMP classifications and should not be reported as clinical interpretations.

A clearer future column name would be:

```text
heuristic_priority_label
```

rather than:

```text
acmg_classification
```

---

## Maximum Score in the Current Pipeline

With the current parser output, no `clinvar_status` column is added.

The normally available components are therefore:

```text
Population frequency: 30
Impact:              25
Functional domain:   15
--------------------------------
Maximum:             70
```

This means the `Pathogenic` threshold of 80 is normally unreachable unless a valid `clinvar_status` column is added separately.

---

## Usage as a Module

```python
from Variant_Prioritization_Engine import VariantPrioritizer

prioritizer = VariantPrioritizer()

results = prioritizer.prioritize(
    vcf_file="input.vcf",
    gene_start=11089462,
    gene_end=11133820,
    patient_id="Sample-001",
)

print(
    results[
        [
            "Gene_Name",
            "HGVS_p",
            "priority_score",
            "acmg_classification",
        ]
    ].head()
)
```

---

## Running the Script Directly

The current `__main__` block contains hard-coded inputs:

```python
vcf_file="patient.vcf"
gene_start=43044295
gene_end=43125482
patient_id="Patient-XYZ-001"
```

Therefore:

```bash
python Variant_Prioritization_Engine.py
```

only works when:

* A suitable `patient.vcf` exists in the current directory
* The VCF has already been annotated by SnpEff
* `Variant_Annotation.py` is in the same working directory
* The required region is appropriate for that VCF and reference assembly

For other input files, edit the `__main__` block or import `VariantPrioritizer` from another Python script.

---

## Unimplemented Components

The following methods are currently placeholders:

```python
query_cadd()
query_clinvar_api()
query_pubmed()
generate_clinical_report()
```

The external-enrichment loop also contains only `pass`.

As a result, the current engine does **not**:

* Query CADD
* Query ClinVar
* Query PubMed
* Add publication counts
* Generate a clinical report file
* Generate treatment recommendations
* Produce a standalone saved prioritization report
* Apply formal ACMG/AMP evidence rules

The final ranked pandas DataFrame is returned to the caller but is not automatically saved.

---

## Known Runtime Risks

### Protein-position conversion

`Protein_position` is read from the annotation TSV and may be represented as text, such as:

```text
745
```

or:

```text
745/1863
```

The current domain function compares it directly with integers:

```python
if start <= protein_position <= end:
```

This may raise a `TypeError`.

Protein positions should be parsed safely before comparison.

### Allele-frequency conversion

The scorer calls:

```python
float(af)
```

This may fail for values such as:

```text
0.01,0.02
```

which can occur in multiallelic records.

### Subprocess interpreter

The annotation pipeline invokes:

```text
python
```

rather than the interpreter currently executing the script. In some environments, this may run a different Python installation.

### Fixed temporary filename

Every run writes:

```text
temp_annotations.tsv
```

This can overwrite a previous file and may conflict with concurrent runs.

---

# Current Limitations

| Component         | Limitation                                                    |
| ----------------- | ------------------------------------------------------------- |
| FASTA editor      | No input, position, or nucleotide validation                  |
| FASTA editor      | Writes an unwrapped sequence without a final sequence newline |
| Annotation parser | No chromosome filtering                                       |
| Annotation parser | No malformed-row handling                                     |
| Annotation parser | Limited multiallelic handling                                 |
| Annotation parser | Hard-coded SnpEff field layout                                |
| Annotation parser | No genotype/sample processing                                 |
| Prioritizer       | CADD query not implemented                                    |
| Prioritizer       | ClinVar query not implemented                                 |
| Prioritizer       | PubMed query not implemented                                  |
| Prioritizer       | Report generation not implemented                             |
| Prioritizer       | Domain data limited to BRCA1 and TP53 examples                |
| Prioritizer       | Protein-position parsing may fail                             |
| Prioritizer       | Multivalue AF parsing may fail                                |
| Prioritizer       | Score labels are not ACMG classifications                     |
| Repository        | No tests or example input files                               |
| Repository        | No formal licence specified                                   |

---

## Suggested Repository Setup

A clearer project layout would be:

```text
genomic-variant-analysis-toolkit/
├── Introduce_nucleotide_change.py
├── Variant_Annotation.py
├── Variant_Prioritization_Engine.py
├── README.md
├── requirements.txt
├── LICENSE
├── examples/
│   ├── example.fasta
│   └── README.md
└── tests/
    ├── test_sequence_editor.py
    ├── test_annotation_parser.py
    └── test_prioritizer.py
```

Do not upload identifiable patient VCF files or protected health information to a public repository.

---

## Project Status

| Component                          | Status          |
| ---------------------------------- | --------------- |
| Basic FASTA nucleotide replacement | Implemented     |
| Multi-line FASTA joining           | Implemented     |
| FASTA validation                   | Not implemented |
| SnpEff `ANN` parsing               | Implemented     |
| Genomic-position filtering         | Implemented     |
| Effect filtering                   | Implemented     |
| Impact filtering                   | Implemented     |
| `rs`-prefix filtering              | Implemented     |
| TSV output                         | Implemented     |
| Basic heuristic scoring            | Implemented     |
| Variant sorting                    | Implemented     |
| CADD integration                   | Placeholder     |
| ClinVar integration                | Placeholder     |
| PubMed integration                 | Placeholder     |
| Report generation                  | Placeholder     |
| Formal ACMG/AMP engine             | Not implemented |
| Automated testing                  | Not implemented |
| Clinical validation                | Not performed   |

This pipeline can be complemented with the pipeline on https://github.com/Bioinformaticslave/genomic-medicine-portfolio which focuses on clinical significance of variants from unannotated VCF. 
---

## Roadmap

### Code reliability

* [ ] Validate FASTA headers and sequence characters
* [ ] Reject positions outside the sequence
* [ ] Require one valid replacement nucleotide
* [ ] Add informative exceptions
* [ ] Validate VCF column counts
* [ ] Validate coordinate order
* [ ] Parse multiallelic records safely
* [ ] Parse numeric protein positions robustly
* [ ] Parse scalar and multivalue allele frequencies
* [ ] Use `sys.executable` for subprocess calls
* [ ] Replace the fixed temporary file with `tempfile`

### Prioritization

* [ ] Rename score-derived ACMG labels
* [ ] Add configurable weights
* [ ] Add more protein-domain annotations
* [ ] Implement ClinVar retrieval
* [ ] Implement CADD retrieval
* [ ] Implement PubMed retrieval
* [ ] Record evidence provenance
* [ ] Export ranked TSV or CSV files
* [ ] Generate a research summary report
* [ ] Separate missing evidence from benign evidence

### Repository quality

* [ ] Add unit tests
* [ ] Add example files
* [ ] Add expected outputs
* [ ] Add type hints
* [ ] Add docstrings and developer documentation
* [ ] Add continuous integration
* [ ] Add a formal open-source licence
* [ ] Pin or constrain dependency versions

---

## Contributing

Contributions and issue reports are welcome.

A typical workflow is:

```bash
git checkout -b feature/improve-vcf-parsing
```

After making and testing changes:

```bash
git add .
git commit -m "Improve multiallelic VCF handling"
git push origin feature/improve-vcf-parsing
```

Then open a pull request describing:

* The problem addressed
* The implementation
* Example input and output
* Tests performed
* Remaining limitations

---

## Development Principles

Contributions should prioritize:

* Transparent behaviour
* Reproducibility
* Input validation
* Clear error messages
* Explicit assumptions
* Standard genomic formats
* Separation of research ranking from clinical interpretation
* Protection of sensitive genomic information

---

## References

1. Cingolani, P. et al.
   *A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff.*
   Fly, 2012.

2. Landrum, M. J. et al.
   *ClinVar: public archive of relationships among sequence variation and human phenotype.*
   Nucleic Acids Research, 2014.

3. Karczewski, K. J. et al.
   *The mutational constraint spectrum quantified from variation in 141,456 humans.*
   Nature, 2020.

4. Richards, S. et al.
   *Standards and guidelines for the interpretation of sequence variants.*
   Genetics in Medicine, 2015.

---

## Licence

No formal open-source licence is currently specified in the repository description.

Before describing the project as open source, add a `LICENSE` file. Common options include:

* MIT License
* Apache License 2.0
* BSD 3-Clause License

Update the badge and this section after choosing a licence.

---

## Disclaimer

> [!WARNING]
> This software is intended only for education, research, and software prototyping.

It is not intended for:

* Clinical diagnosis
* Medical screening
* Treatment selection
* Patient management
* Clinical reporting
* Automated ACMG/AMP classification

The priority scores and labels are experimental software outputs. They must not be interpreted as validated evidence of pathogenicity or benignity.

All research findings should be independently reviewed and validated using appropriate genomic methods, databases, quality controls, and expert interpretation.

---

## Author

**Edward Ying**
Imperial College London

Developed as an extension of a genomic annotation practical organised by Dr. Derek Huntley to explore FASTA manipulation, SnpEff annotation parsing, and transparent variant-ranking workflows.

---

<p align="center">
  <strong>Prototype research software — not validated for clinical use</strong>
</p>
