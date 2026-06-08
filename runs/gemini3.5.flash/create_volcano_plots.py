import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plotting style
sns.set_theme(style="ticks")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# Reconcile old to new/mapped gene names
GENE_NAME_MAP = {
    "B9J08_03708": "SCF1 (B9J08_03708)",
    "B9J08_00453": "B9J08_00453",
    "B9J08_04747": "B9J08_04747",
    "B9J08_00369": "B9J08_00369",
    "B9J08_05200": "B9J08_05200",
}

def load_data(path):
    df = pd.read_csv(path, sep="\t")
    # Convert FDR/P-adj to float, handle NAs
    df['P-adj'] = pd.to_numeric(df['P-adj'], errors='coerce')
    df['log2(FC)'] = pd.to_numeric(df['log2(FC)'], errors='coerce')
    df = df.dropna(subset=['P-adj', 'log2(FC)'])
    
    # Add -log10(P-adj) column, cap very small p-values to prevent inf
    df['log10_padj'] = -np.log10(df['P-adj'].clip(lower=1e-300))
    
    # Classify significance
    df['color'] = 'Not Significant'
    df.loc[(df['log2(FC)'] >= 1.0) & (df['P-adj'] < 0.05), 'color'] = 'Upregulated'
    df.loc[(df['log2(FC)'] <= -1.0) & (df['P-adj'] < 0.05), 'color'] = 'Downregulated'
    
    return df

def draw_volcano(df, title, save_path, label_genes=[]):
    plt.figure(figsize=(10, 8), dpi=300)
    
    # Color palette
    colors = {'Not Significant': '#b2bec3', 'Upregulated': '#ff7675', 'Downregulated': '#74b9ff'}
    
    # Scatter plot
    sns.scatterplot(
        data=df, 
        x='log2(FC)', 
        y='log10_padj', 
        hue='color', 
        palette=colors, 
        alpha=0.8, 
        edgecolor=None,
        s=15
    )
    
    # Threshold lines
    plt.axhline(y=-np.log10(0.05), color='#2d3436', linestyle='--', linewidth=0.8, alpha=0.7)
    plt.axvline(x=1.0, color='#2d3436', linestyle='--', linewidth=0.8, alpha=0.7)
    plt.axvline(x=-1.0, color='#2d3436', linestyle='--', linewidth=0.8, alpha=0.7)
    
    # Add annotations/labels
    for gene_id in label_genes:
        row = df[df['GeneID'] == gene_id]
        if not row.empty:
            x = row['log2(FC)'].values[0]
            y = row['log10_padj'].values[0]
            label = GENE_NAME_MAP.get(gene_id, gene_id)
            
            plt.annotate(
                label,
                xy=(x, y),
                xytext=(x + 0.15 * np.sign(x), y + 10),
                arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=4, headlength=4),
                fontsize=9,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5)
            )
            
    # Labels and title
    plt.title(title, fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('log2 Fold Change', fontsize=12, labelpad=8)
    plt.ylabel('-log10 Adjusted P-value (FDR)', fontsize=12, labelpad=8)
    plt.legend(title='Expression', loc='upper right')
    
    # Clean borders
    sns.despine()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# Load comparisons
df_wt = load_data('/tmp/AR0382_vs_AR0387_annotated.tsv')
df_mut = load_data('/tmp/tnSWI1_vs_AR0382_annotated.tsv')

# Top interesting genes to label
top_genes = ["B9J08_03708", "B9J08_00453", "B9J08_04747"]

print("Generating volcano plots...")
draw_volcano(
    df_wt, 
    'Aggregative WT (AR0382_WT) vs Nonaggregative WT (AR0387_WT)', 
    'volcano_AR0382_vs_AR0387.png',
    label_genes=top_genes
)
print("Saved volcano_AR0382_vs_AR0387.png")

draw_volcano(
    df_mut, 
    'tnSWI1 Mutant vs Aggregative WT (AR0382_WT)', 
    'volcano_tnSWI1_vs_AR0382.png',
    label_genes=top_genes
)
print("Saved volcano_tnSWI1_vs_AR0382.png")
print("All plots generated successfully!")
