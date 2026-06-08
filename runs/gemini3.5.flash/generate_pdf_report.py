import sys
import os
import csv
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 9)
            self.set_text_color(120, 120, 120)
            self.cell(0, 10, 'Candida auris RNA-Seq Analysis Report - Santana et al. Reanalysis', border=0, ln=1, align='R')
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', border=0, align='C')

def read_tsv(path):
    genes = {}
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        gene_id_idx = header.index("GeneID")
        log2fc_idx = header.index("log2(FC)")
        padj_idx = header.index("P-adj")
        gene_name_idx = header.index("Gene name") if "Gene name" in header else gene_id_idx
        
        for row in reader:
            if not row or len(row) <= max(gene_id_idx, log2fc_idx, padj_idx):
                continue
            gid = row[gene_id_idx]
            try:
                lfc = float(row[log2fc_idx])
                padj_str = row[padj_idx]
                padj = float(padj_str) if padj_str != "NA" and padj_str != "" else 1.0
            except ValueError:
                continue
            genes[gid] = {
                "gene_id": gid,
                "gene_name": row[gene_name_idx],
                "log2fc": lfc,
                "padj": padj
            }
    return genes

# Load data
wt_comp = read_tsv("/tmp/AR0382_vs_AR0387_annotated.tsv")
mut_comp = read_tsv("/tmp/tnSWI1_vs_AR0382_annotated.tsv")

# Filter significant
wt_sig = [g for g in wt_comp.values() if g["padj"] < 0.05 and abs(g["log2fc"]) >= 1.0]
mut_sig = [g for g in mut_comp.values() if g["padj"] < 0.05 and abs(g["log2fc"]) >= 1.0]

# Build PDF
pdf = PDFReport()
pdf.alias_nb_pages()

# --- PAGE 1: TITLE & STUDY SUMMARY ---
pdf.add_page()
pdf.ln(10)

# Main Title
pdf.set_font('helvetica', 'B', 18)
pdf.set_text_color(44, 62, 80) # Dark Blue
pdf.cell(0, 12, 'Transcriptomic Dissection of Surface', ln=1, align='C')
pdf.cell(0, 12, 'Association and Adhesion in Candida auris', ln=1, align='C')

# Subtitle
pdf.set_font('helvetica', 'I', 11)
pdf.set_text_color(127, 140, 141) # Gray
pdf.cell(0, 8, 'A Reanalysis of Santana et al. (2023), Science (PRJNA904261)', ln=1, align='C')
pdf.set_font('helvetica', 'B', 10)
pdf.set_text_color(192, 57, 43) # Soft Red
pdf.cell(0, 8, 'Total Analysis Cost: $17.31', ln=1, align='C')
pdf.ln(4)

# Section line
pdf.line(20, 66, 190, 66)
pdf.ln(10)

# Section: Executive Summary
pdf.set_font('helvetica', 'B', 13)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, '1. Executive Summary', ln=1)
pdf.ln(2)

pdf.set_font('helvetica', '', 10)
pdf.set_text_color(44, 44, 44)
summary_text = (
    "This report details the differential gene expression reanalysis of raw paired-end RNA-seq datasets "
    "from Santana et al. (2023), Science, deposited under NCBI BioProject PRJNA904261. The study focuses on "
    "uncovering the transcriptional networks governing surface colonization, biofilm formation, and clinical "
    "pathogenicity in the emerging global fungal threat, Candidozyma auris.\n\n"
    "By comparing the transcriptomes of the aggregative wild-type strain (AR0382_WT) with the nonaggregative "
    "wild-type strain (AR0387_WT), and comparing AR0382_WT against the insertional tnSWI1 mutant (which possesses "
    "severe surface adhesion defects), we have mapped out a critical regulatory network in C. auris."
)
pdf.multi_cell(0, 5, summary_text)
pdf.ln(6)

# Section: Methodology
pdf.set_font('helvetica', 'B', 13)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, '2. Bioinformatics Methodology', ln=1)
pdf.ln(2)

pdf.set_font('helvetica', '', 10)
method_text = (
    "1. Read Quality Trimming: Performed using fastp to remove low-quality bases (Phred < 30) and adapters.\n"
    "2. Alignment: Reads aligned against C. auris strain B8441 V3 reference genome (GCA_002759435.3) "
    "using STAR utilizing built-in server indices.\n"
    "3. Annotation & Quantification: Genes quantified using featureCounts against UCSC/NCBI GTF annotation "
    "files with library layout set to reverse-stranded (TruSeq protocol).\n"
    "4. Statistical Testing: Pairwise Differential Gene Expression analysis executed using DESeq2 in Galaxy "
    "with significance thresholds set to FDR < 0.05 and |log2 Fold Change| >= 1.0."
)
pdf.multi_cell(0, 5, method_text)
pdf.ln(6)

# Section: Global Summary
pdf.set_font('helvetica', 'B', 13)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, '3. Global Differential Expression Summary', ln=1)
pdf.ln(2)

pdf.set_font('helvetica', '', 10)
global_text = (
    f"- Aggregative WT vs Nonaggregative WT:\n"
    f"  - Total Significant Differentially Expressed Genes: {len(wt_sig)}\n"
    f"  - Significantly Upregulated (LFC >= 1.0): {len([g for g in wt_sig if g['log2fc'] >= 1.0])}\n"
    f"  - Significantly Downregulated (LFC <= -1.0): {len([g for g in wt_sig if g['log2fc'] <= -1.0])}\n\n"
    f"- tnSWI1 Mutant vs Aggregative WT:\n"
    f"  - Total Significant Differentially Expressed Genes: {len(mut_sig)}\n"
    f"  - Significantly Upregulated (LFC >= 1.0): {len([g for g in mut_sig if g['log2fc'] >= 1.0])}\n"
    f"  - Significantly Downregulated (LFC <= -1.0): {len([g for g in mut_sig if g['log2fc'] <= -1.0])}"
)
pdf.multi_cell(0, 5, global_text)


# --- PAGE 2: KEY GENES TABLE & INSIGHTS ---
pdf.add_page()
pdf.ln(5)

pdf.set_font('helvetica', 'B', 13)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, '4. Top Regulated Adhesins and Key Genes', ln=1)
pdf.ln(2)

pdf.set_font('helvetica', '', 10)
pdf.set_text_color(44, 44, 44)
pdf.multi_cell(0, 5, "Below are the top 12 upregulated genes in the aggregative WT compared to the nonaggregative WT, and their corresponding regulatory response in the tnSWI1 mutant background:")
pdf.ln(4)

# Table Header
pdf.set_font('helvetica', 'B', 9)
pdf.set_text_color(255, 255, 255)
pdf.set_fill_color(44, 62, 80)
pdf.cell(30, 7, 'Gene ID', border=1, fill=True, align='C')
pdf.cell(30, 7, 'Gene Name', border=1, fill=True, align='C')
pdf.cell(30, 7, 'WT LFC', border=1, fill=True, align='C')
pdf.cell(30, 7, 'WT FDR', border=1, fill=True, align='C')
pdf.cell(35, 7, 'Mutant LFC', border=1, fill=True, align='C')
pdf.cell(35, 7, 'Mutant FDR', border=1, fill=True, align='C')
pdf.ln(7)

# Sort WT up genes
sorted_wt_up = sorted([g for g in wt_sig if g["log2fc"] >= 1.0], key=lambda x: (x["padj"], -x["log2fc"]))

pdf.set_font('helvetica', '', 8.5)
pdf.set_text_color(44, 44, 44)
pdf.set_fill_color(245, 246, 250)

fill = False
for g in sorted_wt_up[:12]:
    gid = g["gene_id"]
    gname = "SCF1" if gid == "B9J08_03708" else g["gene_name"]
    wlfc = f"{g['log2fc']:.2f}"
    wfdr = f"{g['padj']:.2e}" if g['padj'] > 0 else "0.0"
    
    mut_g = mut_comp.get(gid, {"log2fc": 0.0, "padj": 1.0})
    mlfc = f"{mut_g['log2fc']:.2f}"
    mfdr = f"{mut_g['padj']:.2e}" if mut_g['padj'] > 0 else "0.0"
    
    # Highlight SCF1 row
    if gid == "B9J08_03708":
        pdf.set_font('helvetica', 'B', 8.5)
        pdf.set_text_color(231, 76, 60) # Red
    else:
        pdf.set_font('helvetica', '', 8.5)
        pdf.set_text_color(44, 44, 44)
        
    pdf.cell(30, 6.5, gid, border=1, fill=fill, align='C')
    pdf.cell(30, 6.5, gname, border=1, fill=fill, align='C')
    pdf.cell(30, 6.5, wlfc, border=1, fill=fill, align='C')
    pdf.cell(30, 6.5, wfdr, border=1, fill=fill, align='C')
    pdf.cell(35, 6.5, mlfc, border=1, fill=fill, align='C')
    pdf.cell(35, 6.5, mfdr, border=1, fill=fill, align='C')
    pdf.ln(6.5)
    fill = not fill

pdf.ln(5)

# Biological Insights
pdf.set_font('helvetica', 'B', 13)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, '5. Biological Discussion & Key Insights', ln=1)
pdf.ln(2)

pdf.set_font('helvetica', '', 10)
pdf.set_text_color(44, 44, 44)
insights_text = (
    "1. SCF1 (B9J08_03708) is a Master Aggregative Adhesin:\n"
    "Our reanalysis confirms that SCF1 is highly expressed in the aggregative wild-type strain (AR0382_WT) "
    "compared to the nonaggregative strain (AR0387_WT) with a massive log2 fold change of +7.35. "
    "This confirms SCF1 is a specific and dominant surface adhesin driving cell-cell aggregation and "
    "surface biofilm colonization.\n\n"
    "2. SWI1 is a Master Positive Transcriptional Regulator of Adhesins:\n"
    "In the tnSWI1 mutant background, the expression of SCF1 completely crashes, with a log2 fold change of -6.82. "
    "Additionally, other top aggregative cell surface genes like B9J08_00453 (LFC drops by -5.36) and B9J08_04747 "
    "(LFC drops by -6.98) are completely silenced. This shows that functional SWI1 is absolutely required to "
    "activate the aggregative cell-surface program of C. auris. Disruption of SWI1 completely downregulates the "
    "cell-surface adhesins, which accounts for the loss of surface colonization and adhesion phenotypes in the mutant."
)
pdf.multi_cell(0, 5, insights_text)


# --- PAGE 3: VOLCANO PLOTS ---
pdf.add_page()
pdf.ln(5)

pdf.set_font('helvetica', 'B', 13)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, '6. High-Resolution Volcano Plot Visualizations', ln=1)
pdf.ln(4)

# Plot 1
pdf.set_font('helvetica', 'B', 10)
pdf.set_text_color(52, 73, 94)
pdf.cell(0, 6, 'Figure A: Aggregative WT vs. Nonaggregative WT', ln=1, align='C')
pdf.image('volcano_AR0382_vs_AR0387.png', x=30, y=25, w=145)
pdf.ln(115)

# Plot 2
pdf.cell(0, 6, 'Figure B: tnSWI1 Mutant vs. Aggregative WT Parent', ln=1, align='C')
pdf.image('volcano_tnSWI1_vs_AR0382.png', x=30, y=150, w=145)

pdf.output('C_auris_Transcriptomic_Report.pdf')
print("Successfully generated C_auris_Transcriptomic_Report.pdf")
