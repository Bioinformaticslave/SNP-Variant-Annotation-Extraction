# Genomic Variant Analysis Toolkit

**Author:** Edward Ying | Imperial College London, Biology

A collection of Python tools for manipulating genomic sequences and analyzing genetic variants from SnpEff-annotated VCF files.

---

## Repository Contents

| File | Purpose |
|------|---------|
| `Introduce_nucleotide_change.py` | Simple tool to introduce a single nucleotide substitution in a FASTA sequence |
| `Variant_Annotation.py` | Extract and filter structured variant annotations from SnpEff-annotated VCF files |
| `Variant_Prioritization_Engine.py` | Rank and prioritize clinically relevant variants using multi-evidence scoring |

---

## Tool 1: Introduce Nucleotide Change

### Overview
A simple interactive script that modifies a specific position in a FASTA sequence by replacing the nucleotide at a user-specified position.

### Use Case
This tool is useful for:
- Creating mutant sequences for functional studies
- Simulating specific mutations in reference sequences
- Generating sequences for primer design or cloning experiments
- Educational demonstrations of sequence manipulation

### Requirements
- Python 3.7 or later
- No external packages required

### Usage
Run the script interactively:

```bash
python Introduce_nucleotide_change.py
You will be prompted to provide:

Input FASTA file path — Path to your FASTA file

Output FASTA file path — Where to save the modified sequence

Position to change — The nucleotide position (1-based indexing)

New nucleotide — The replacement base (A, T, G, or C)

Example
Input FASTA (BRCA1_exon.fasta):

text
>BRCA1_exon_11
ATGGATTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCCTTATATGCTCTTT
Interaction:

text
Input FASTA file path: BRCA1_exon.fasta
Output FASTA file path: BRCA1_mutant.fasta
Position to change: 15
New nucleotide: C
Output FASTA (BRCA1_mutant.fasta):

text
>BRCA1_exon_11
ATGGATTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCCTTATATGCTCTTT
                         ^
                    Position 15 changed from A to C
How It Works
Reads the FASTA file

Extracts the header line and concatenates all sequence lines

Converts the sequence to uppercase

Replaces the nucleotide at the specified position (1-based indexing)

Writes the modified sequence with the original header

## Tool 2: Improved SNP Annotation Parser
Overview
Extracts and filters variant annotations from a SnpEff-annotated VCF file, producing a structured tab-delimited output for downstream analysis.

Why This Tool?
The original practical script only reported missense variants and printed results to the terminal. This improved version:

Produces structured tab-delimited output files — Ready for Excel, R, or Python

Extracts comprehensive annotations — Including impact level, gene name, transcript information, and HGVS nomenclature

Supports flexible filtering — By variant effect, impact category, or dbSNP status

Handles multiple transcript annotations — Each variant-transcript combination appears as a separate row

Requirements
Python 3.7 or later

No external packages required

Input Format
The script expects a SnpEff-annotated VCF file with:

Standard VCF columns (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO)

ANN field in the INFO column (SnpEff annotation format)

Optional DP (read depth) and AF (allele frequency) fields

Usage
Basic usage (extract all variants in a gene region):

bash
python Variant_Annotation.py ldlr_filtered_snps_final_ann_dbsnp.vcf 11089462 11133820
Arguments:

Argument	Description
vcf_file	Path to SnpEff-annotated VCF file
gene_start	Start coordinate of the target gene
gene_end	End coordinate of the target gene
-o, --output	Output TSV filename (default: improved_snp_annotations.tsv)
--effect	Filter by effect type (e.g., missense_variant)
--impact	Filter by impact category (HIGH, MODERATE, LOW, MODIFIER)
--only-rs	Include only variants with dbSNP rsIDs
Examples
Extract all variants in the LDLR gene:

bash
python Variant_Annotation.py ldlr_filtered_snps_final_ann_dbsnp.vcf 11089462 11133820
Extract only missense variants:

bash
python Variant_Annotation.py ldlr_filtered_snps_final_ann_dbsnp.vcf 11089462 11133820 \
    --effect missense_variant \
    -o LDLR_missense.tsv
Extract only HIGH impact variants (e.g., stop-gained, frameshift):

bash
python Variant_Annotation.py ldlr_filtered_snps_final_ann_dbsnp.vcf 11089462 11133820 \
    --impact HIGH \
    -o LDLR_high_impact.tsv
Extract only variants with dbSNP IDs:

bash
python Variant_Annotation.py ldlr_filtered_snps_final_ann_dbsnp.vcf 11089462 11133820 \
    --only-rs \
    -o LDLR_known_rs.tsv
Output Format
The script produces a tab-delimited file with the following columns:

Column	Description:
CHROM	Chromosome name
POS	Genomic position
ID	dbSNP identifier (or "." if none)
REF	Reference allele
ALT	Alternative allele
QUAL	Quality score
FILTER	Filter status
DP	Read depth (from INFO)
AF	Allele frequency (from INFO)
Effect	SnpEff effect type (e.g., missense_variant)
Impact	Severity level (HIGH/MODERATE/LOW/MODIFIER)
Gene_Name	Gene symbol
Transcript_ID	Transcript identifier
Transcript_Biotype	Transcript biotype (e.g., protein_coding)
HGVS_c	HGVS cDNA notation
HGVS_p	HGVS protein notation
Protein_position	Protein position of the variant
Important Notes
If a variant has multiple transcript annotations, each transcript appears as a separate row

The --effect filter uses partial matching (e.g., --effect missense matches missense_variant)

The --impact filter requires an exact match (e.g., HIGH)

Comparison with Original Practical Script
Feature	Original Script	Improved Script
Region filtering	✓	✓
Missense variant detection	✓	✓
Transcript extraction	✓	✓
HGVS extraction	✓	✓
Terminal output	✓	✓
Structured output file	✗	✓
Impact filtering	✗	✓
dbSNP filtering	✗	✓
Additional annotations	✗	✓
Downstream analysis ready	✗	✓

Tool 3: Clinical Variant Prioritization Engine
Overview
Transforms a flat list of annotated variants into a clinically actionable, prioritized report. This tool scores and ranks variants based on multiple lines of evidence to identify those most likely to impact patient care.

The Problem It Solves
When analyzing whole exome sequencing data, clinicians often face 10-50 candidate variants in a gene of interest, with no clear way to determine which ones to investigate first. This tool solves that bottleneck by:

Scoring each variant (0-100) based on cumulative evidence

Ranking variants from highest to lowest clinical priority

Suggesting ACMG classifications (Pathogenic, VUS, Benign, etc.)

How Scoring Works
Evidence Type	Weight	Description
Population Frequency	0-30	Rarer variants score higher (AF < 0.0001 = +30)
Impact Severity	0-25	HIGH impact variants score highest
ClinVar Status	0-30	Pathogenic/Likely Pathogenic weighted highest
Functional Domain	0-15	Variants in conserved/functional domains
Literature Evidence	0-20	More publications = stronger evidence (planned)
Score Interpretation:

80-100: High priority — likely clinically actionable

60-79: Medium-high — consider further investigation

40-59: Medium — monitor for future evidence

<40: Low — likely benign or insufficient evidence

Requirements
Python 3.7 or later

pandas for data manipulation

requests for API queries (optional, for external database integration)

Installation
bash
pip install pandas requests
Current Implementation Status
This tool provides a framework for variant prioritization with:

✅ Integrated annotation pipeline — Calls Variant_Annotation.py to generate initial variant list
✅ Priority scoring algorithm — Calculates scores based on available evidence
✅ ACMG classification mapping — Suggests classifications based on score thresholds
✅ Report generation framework — Structure for clinical reporting

🚧 Planned enhancements:

Real API integration (gnomAD, CADD, ClinVar, PubMed)

Full report generation with clinical recommendations

Interactive Streamlit dashboard

Usage
Complete pipeline (annotation + prioritization):

python
from Variant_Prioritization_Engine import VariantPrioritizer

prioritizer = VariantPrioritizer()

# Run the pipeline
results = prioritizer.prioritize(
    vcf_file="patient.vcf",
    gene_start=43044295,
    gene_end=43125482,  # BRCA1 gene coordinates
    patient_id="Patient-XYZ-001"
)

# View top 5 prioritized variants
print(results[['Gene_Name', 'HGVS_p', 'priority_score', 'acmg_classification']].head())
Direct usage with pre-annotated file:
If you already have an annotated TSV file from Variant_Annotation.py:

python
# Load your annotated variants
df = pd.read_csv("improved_snp_annotations.tsv", sep="\t")

# Add priority scores
prioritizer = VariantPrioritizer()
df['priority_score'] = df.apply(prioritizer.calculate_priority_score, axis=1)
df['acmg_classification'] = df.apply(
    lambda row: prioritizer.generate_acmg_classification(row, row['priority_score']),
    axis=1
)

# Sort by priority
results = df.sort_values('priority_score', ascending=False)
Example Output
text
🔝 TOP 5 PRIORITY VARIANTS:
  Gene_Name      HGVS_p        priority_score  acmg_classification
0   BRCA1     p.Arg745His          95         Pathogenic
1   BRCA1     p.Arg338Cys          82         Likely Pathogenic
2   BRCA1     p.Pro560Ser          65         Variant of Uncertain Significance
3   BRCA1     p.Ser152Leu          35         Likely Benign
4   BRCA1     p.Val263Ile          12         Benign
Integration with Variant_Annotation.py
The prioritization engine seamlessly integrates with your annotation tool:

text
VCF File
    │
    ▼
Variant_Annotation.py
    │
    ▼
Annotated TSV (all variants in region)
    │
    ▼
Variant_Prioritization_Engine.py
    │
    ▼
Prioritized Clinical Report
    │
    ├── Top 5 high-priority variants
    ├── ACMG classifications
    ├── Clinical recommendations
    └── Variants requiring monitoring
Real-World Applications
Use Case	Tools Involved	Example
Hereditary cancer screening	Variant_Annotation + Prioritization	Prioritize BRCA1/2 variants for breast cancer risk
Pharmacogenomics	Variant_Annotation	Identify variants affecting drug metabolism (CYP450 genes)
Functional validation	Introduce_nucleotide_change	Create mutant constructs for laboratory studies
Cardiovascular genetics	Variant_Annotation + Prioritization	Prioritize LDLR variants for familial hypercholesterolemia
Educational demonstrations	All tools	Teach genomic variant interpretation workflow
Example Workflow: BRCA1 Variant Analysis
Step 1: Create a mutant sequence for validation

bash
python Introduce_nucleotide_change.py
# Input: BRCA1_wildtype.fasta
# Position: 745
# New base: A (creates p.Arg745His mutation)
Step 2: Annotate variants in a clinical sample

bash
python Variant_Annotation.py BRCA1_patient.vcf 43044295 43125482 \
    -o BRCA1_variants.tsv
Step 3: Prioritize variants for clinical action

python
from Variant_Prioritization_Engine import VariantPrioritizer

prioritizer = VariantPrioritizer()
results = prioritizer.prioritize(
    vcf_file="BRCA1_patient.vcf",
    gene_start=43044295,
    gene_end=43125482,
    patient_id="BRCA1-001"
)
Future Improvements
Export to CSV and Excel formats

Interactive Streamlit dashboard

Real API integration (gnomAD, CADD, ClinVar, PubMed)

Support for VEP annotations (alternative to SnpEff)

Family pedigree integration (segregation analysis)

Batch processing for WGS/WES data

ACMG/AMP guideline mapping for automated classification

Machine learning for pathogenicity prediction

Automatic generation of summary statistics and plots

References
SnpEff: A program for annotating and predicting the effects of single nucleotide polymorphisms (Cingolani et al., 2012)

ClinVar: Public archive of relationships among sequence variation and human health (Landrum et al., 2014)

gnomAD: Genome Aggregation Database (Karczewski et al., 2020)

ACMG/AMP guidelines for variant interpretation (Richards et al., 2015)

Author
Edward Ying | Imperial College London, Biology

Developed as an extension of a variant annotation practical to improve exploration and interpretation of SnpEff-annotated VCF files.

License
This project is for educational and research purposes only. Not for clinical use without validation.

Disclaimer
Important: These tools are for educational and demonstration purposes only. They are not intended for clinical diagnosis or treatment decisions. All genetic findings must be confirmed by clinical-grade testing and interpreted by qualified healthcare professionals.pEff-annotated VCF files.
