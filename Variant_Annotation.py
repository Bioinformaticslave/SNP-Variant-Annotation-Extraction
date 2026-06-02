import sys
import argparse
import csv


ANN_FIELDS = [
    "Allele",
    "Effect",
    "Impact",
    "Gene_Name",
    "Gene_ID",
    "Feature_Type",
    "Transcript_ID",
    "Transcript_Biotype",
    "Rank",
    "HGVS_c",
    "HGVS_p",
    "cDNA_position",
    "CDS_position",
    "Protein_position",
    "Distance",
    "Warnings"
]


def parse_info(info):
    """Convert VCF INFO column into a dictionary."""
    info_dict = {}
    for item in info.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            info_dict[key] = value
        else:
            info_dict[item] = True
    return info_dict


def parse_ann(ann_string):
    """Parse SnpEff ANN field into one dictionary per transcript annotation."""
    annotations = []

    for ann in ann_string.split(","):
        parts = ann.split("|")

        # Pad if annotation has fewer fields than expected
        parts += [""] * (len(ANN_FIELDS) - len(parts))

        annotations.append(dict(zip(ANN_FIELDS, parts)))

    return annotations


def main():
    parser = argparse.ArgumentParser(
        description="Extract improved SNP annotations from a SnpEff-annotated VCF."
    )

    parser.add_argument("vcf_file", help="Input annotated VCF file")
    parser.add_argument("gene_start", type=int, help="Gene start coordinate")
    parser.add_argument("gene_end", type=int, help="Gene end coordinate")
    parser.add_argument("-o", "--output", default="improved_snp_annotations.tsv",
                        help="Output TSV file")
    parser.add_argument("--effect", default=None,
                        help="Only keep annotations with this effect, e.g. missense_variant")
    parser.add_argument("--impact", default=None,
                        help="Only keep annotations with this impact, e.g. HIGH, MODERATE, LOW")
    parser.add_argument("--only-rs", action="store_true",
                        help="Only keep variants with dbSNP rs IDs")

    args = parser.parse_args()

    with open(args.vcf_file, "r") as infile, open(args.output, "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter="\t")

        writer.writerow([
            "CHROM",
            "POS",
            "ID",
            "REF",
            "ALT",
            "QUAL",
            "FILTER",
            "DP",
            "AF",
            "Effect",
            "Impact",
            "Gene_Name",
            "Transcript_ID",
            "Transcript_Biotype",
            "HGVS_c",
            "HGVS_p",
            "Protein_position"
        ])

        for line in infile:
            if line.startswith("#"):
                continue

            cols = line.rstrip("\n").split("\t")

            chrom = cols[0]
            pos = int(cols[1])
            snp_id = cols[2]
            ref = cols[3]
            alt = cols[4]
            qual = cols[5]
            filt = cols[6]
            info = cols[7]

            # Keep only variants inside target gene region
            if not (args.gene_start <= pos <= args.gene_end):
                continue

            # Optional: keep only known dbSNP variants
            if args.only_rs and not snp_id.startswith("rs"):
                continue

            info_dict = parse_info(info)

            if "ANN" not in info_dict:
                continue

            dp = info_dict.get("DP", "")
            af = info_dict.get("AF", "")

            annotations = parse_ann(info_dict["ANN"])

            for ann in annotations:
                effect = ann["Effect"]
                impact = ann["Impact"]

                if args.effect and args.effect not in effect:
                    continue

                if args.impact and args.impact != impact:
                    continue

                writer.writerow([
                    chrom,
                    pos,
                    snp_id,
                    ref,
                    alt,
                    qual,
                    filt,
                    dp,
                    af,
                    effect,
                    impact,
                    ann["Gene_Name"],
                    ann["Transcript_ID"],
                    ann["Transcript_Biotype"],
                    ann["HGVS_c"],
                    ann["HGVS_p"],
                    ann["Protein_position"]
                ])

    print(f"Done. Output saved to: {args.output}")


if __name__ == "__main__":
    main()