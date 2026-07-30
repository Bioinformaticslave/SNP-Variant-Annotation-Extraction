# Complete prioritization engine that uses the existing code Variant_Annotation.py

import pandas as pd
import requests
import subprocess

class VariantPrioritizer:
    def __init__(self):
        self.acmg_criteria = {
            'PVS1': 'Null variant in gene where LOF is disease mechanism',
            'PS1': 'Same amino acid change as previously established pathogenic variant',
            'PM2': 'Absent from controls (or extremely rare)',
            'PP5': 'Reputable source recently reports variant as pathogenic'
        }
    
    def run_annotation_pipeline(self, vcf_file, gene_start, gene_end):
        """Run your existing Variant_Annotation.py"""
        cmd = [
            "python", "Variant_Annotation.py",
            vcf_file,
            str(gene_start),
            str(gene_end),
            "-o", "temp_annotations.tsv"
        ]
        subprocess.run(cmd, check=True)
        return pd.read_csv("temp_annotations.tsv", sep="\t")
    
    def query_cadd(self, chrom, pos, ref, alt):
        """Query CADD API for deleteriousness score"""
        # Implementation using CADD REST API
        pass
    
    def query_clinvar_api(self, variant):
        """Enhanced ClinVar query (reuses your genomic-medicine.ipynb code)"""
        # Use your existing ClinVar query function
        pass
    
    def query_pubmed(self, gene, variant):
        """Query PubMed for literature count (reuses your Entrez code)"""
        # Use your existing Entrez API approach
        pass
    
    def compute_domain_info(self, gene, protein_position):
        """Check if variant is in functional domain"""
        domains = {
            'BRCA1': {'zinc_finger': (1, 100), 'BRCT': (1600, 1863)},
            'TP53': {'DNA_binding': (100, 300)},
            # ... more genes
        }
        for domain_name, (start, end) in domains.get(gene, {}).items():
            if start <= protein_position <= end:
                return domain_name
        return None
    
    def calculate_priority_score(self, row):
        """Calculate comprehensive priority score"""
        score = 0
        
        # 1. Population frequency (rarity)
        af = row.get('AF', 1.0)
        if pd.isna(af) or af == '':
            af = 1.0
        else:
            af = float(af)
        
        if af < 0.0001:
            score += 30
        elif af < 0.01:
            score += 20
        elif af < 0.05:
            score += 10
        
        # 2. Impact severity
        impact_scores = {'HIGH': 25, 'MODERATE': 15, 'LOW': 5, 'MODIFIER': 0}
        score += impact_scores.get(row.get('Impact', ''), 0)
        
        # 3. ClinVar status (you'd get this from your API)
        # For demo, reading from a hypothetical column
        clinvar = row.get('clinvar_status', '')
        if clinvar == 'Pathogenic':
            score += 30
        elif clinvar == 'Likely Pathogenic':
            score += 20
        
        # 4. Functional domain
        domain = self.compute_domain_info(row.get('Gene_Name'), 
                                          row.get('Protein_position'))
        if domain:
            score += 15
        
        # 5. Literature count
        # score += min(row.get('pubmed_count', 0) * 2, 20)
        
        return min(score, 100)
    
    def generate_acmg_classification(self, row, score):
        """Suggest ACMG classification based on evidence"""
        if score >= 80:
            return "Pathogenic"
        elif score >= 60:
            return "Likely Pathogenic"
        elif score >= 40:
            return "Variant of Uncertain Significance"
        elif score >= 20:
            return "Likely Benign"
        else:
            return "Benign"
    
    def prioritize(self, vcf_file, gene_start, gene_end, patient_id="Demo-001"):
        """Main pipeline"""
        # Step 1: Run your existing annotation code
        print("🔄 Running variant annotation...")
        df = self.run_annotation_pipeline(vcf_file, gene_start, gene_end)
        
        print(f"📊 Found {len(df)} variants in region")
        
        # Step 2: Enrich with external data (you'd implement these)
        print("🔄 Querying external databases...")
        for idx, row in df.iterrows():
            # Add CADD score
            # Add ClinVar status
            # Add PubMed count
            # Add domain info
            pass
        
        # Step 3: Calculate priority scores
        df['priority_score'] = df.apply(self.calculate_priority_score, axis=1)
        df['acmg_classification'] = df.apply(
            lambda row: self.generate_acmg_classification(row, row['priority_score']),
            axis=1
        )
        
        # Step 4: Sort by score
        df_sorted = df.sort_values('priority_score', ascending=False)
        
        # Step 5: Generate report
        self.generate_clinical_report(df_sorted, patient_id)
        
        return df_sorted
    
    def generate_clinical_report(self, df, patient_id):
        """Generate the clinical prioritization report"""
        # ... (the report generation code from earlier)
        pass

# =================== USAGE ===================
if __name__ == "__main__":
    prioritizer = VariantPrioritizer()
    
    # Run the complete pipeline
    results = prioritizer.prioritize(
        vcf_file="patient.vcf",
        gene_start=43044295,
        gene_end=43125482,  # BRCA1 gene coordinates
        patient_id="Patient-XYZ-001"
    )
    
    # Show top 5
    print("\n🔝 TOP 5 PRIORITY VARIANTS:")
    print(results[['Gene_Name', 'HGVS_p', 'priority_score', 'acmg_classification']].head())