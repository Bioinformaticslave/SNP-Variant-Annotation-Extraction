# Improved SNP Annotation Parser for SnpEff-Annotated VCF Files

## OverviewTool 1: Improved SNP Annotation Parser

This Python script Variant_Annotation.py extracts and summarizes variant annotations from a SnpEff-annotated VCF file. It was developed as an extension of the variant annotation practical to provide a more flexible and informative method for investigating variants within a genomic region of interest. The Variant_Prioritization_Engine.py script ranks variants by clinical actionability using multi-evidence scoring.

Unlike the original practical script, which only reports missense variants and prints results directly to the terminal, this implementation:

* Produces a structured tab-delimited output file.
* Extracts additional annotation information including impact level, gene name, transcript information and HGVS nomenclature.
* Allows filtering by variant effect (e.g. missense variants only).
* Allows filtering by impact category (HIGH, MODERATE, LOW).
* Supports selection of known dbSNP variants only.
* Generates output suitable for downstream analysis in Excel, R or Python.

## Requirements

Python 3.7 or later.

No external Python packages are required.

## Input Files

The script expects a VCF file that has already been annotated using SnpEff.

Example:

```bash
ldlr_filtered_snps_final_ann_dbsnp.vcf
```

## Usage

Basic usage:

```bash
python3 improved_parse_vcf_annotations.py \
ldlr_filtered_snps_final_ann_dbsnp.vcf \
11089462 \
11133820
```

Arguments:

| Argument   | Description                     |
| ---------- | ------------------------------- |
| vcf_file   | Annotated VCF file              |
| gene_start | Start coordinate of target gene |
| gene_end   | End coordinate of target gene   |

## Output

By default the script creates:

```text
improved_snp_annotations.tsv
```

The output table contains:

* Chromosome
* Position
* Variant ID
* Reference allele
* Alternate allele
* Quality score
* Filter status
* Read depth
* Allele frequency
* Variant effect
* Impact level
* Gene name
* Transcript ID
* Transcript biotype
* HGVS cDNA annotation
* HGVS protein annotation
* Protein position

## Examples

### Extract all variants within LDLR

```bash
python3 improved_parse_vcf_annotations.py \
ldlr_filtered_snps_final_ann_dbsnp.vcf \
11089462 \
11133820
```

### Extract missense variants only

```bash
python3 improved_parse_vcf_annotations.py \
ldlr_filtered_snps_final_ann_dbsnp.vcf \
11089462 \
11133820 \
--effect missense_variant \
-o LDLR_missense.tsv
```

### Extract HIGH impact variants only

```bash
python3 improved_parse_vcf_annotations.py \
ldlr_filtered_snps_final_ann_dbsnp.vcf \
11089462 \
11133820 \
--impact HIGH \
-o LDLR_high_impact.tsv
```

### Extract known dbSNP variants only

```bash
python3 improved_parse_vcf_annotations.py \
ldlr_filtered_snps_final_ann_dbsnp.vcf \
11089462 \
11133820 \
--only-rs \
-o LDLR_known_rs.tsv
```

## Comparison with Original Practical Script

| Feature                    | Original Script | Improved Script |
| -------------------------- | --------------- | --------------- |
| Region filtering           | ✓               | ✓               |
| Missense variant detection | ✓               | ✓               |
| Transcript extraction      | ✓               | ✓               |
| HGVS extraction            | ✓               | ✓               |
| Terminal output            | ✓               | ✓               |
| Structured output file     | ✗               | ✓               |
| Impact filtering           | ✗               | ✓               |
| dbSNP filtering            | ✗               | ✓               |
| Additional annotations     | ✗               | ✓               |
| Downstream analysis ready  | ✗               | ✓               |

## Potential Future Improvements

Possible extensions include:

* Export to CSV and Excel formats.
* Functional consequence prioritisation.
* ClinVar annotation support.
* Protein domain annotation.
* PolyPhen and SIFT score integration.
* Automatic generation of summary statistics and plots.

## Author
Edward Ying | Imperial College London, Biology

Developed as an extension of a variant annotation practical to improve exploration and interpretation of SnpEff-annotated VCF files.
