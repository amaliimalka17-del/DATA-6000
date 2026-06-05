
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
df = dataset.copy()
df = df.sort_values('Financial_Year').reset_index(drop=True)
 
# Established capstone Pearson R values — do not change
PEARSON_R = -0.621
PEARSON_P = 0.2634
 
metrics = {
    'Rainfall\n(mm)':     'Total_Rainfall_mm',
    'Production\n(Kt)':   'Total_Production_Kt',
    'CPI\n(%)':           'CPI_Annual_Pct',
    'Irrigation\n(GL)':   'Irrigation_GL',
    'Risk\nScore':         'Risk_Score',
}
 
norm_data = {}
for label, col in metrics.items():
    if col in df.columns:
        col_data = df[col].fillna(df[col].mean())
        col_min  = col_data.min()
        col_max  = col_data.max()
        if col_max > col_min:
            norm_data[label] = (
                (col_data - col_min) /
                (col_max - col_min)
            ).values
        else:
            norm_data[label] = np.zeros(len(df))
 
norm_df = pd.DataFrame(norm_data,
                        index=df['Financial_Year'].values)
 
fig, ax = plt.subplots(figsize=(9, 4.5))
fig.patch.set_facecolor('#F8FAF8')
 
cmap = plt.cm.RdYlGn_r
im   = ax.imshow(norm_df.T.values,
                 cmap=cmap, aspect='auto',
                 vmin=0, vmax=1)
 
ax.set_xticks(range(len(norm_df.index)))
ax.set_xticklabels(norm_df.index,
                   fontsize=10, color='#0B1F12')
ax.set_yticks(range(len(norm_df.columns)))
ax.set_yticklabels(norm_df.columns,
                   fontsize=9, color='#0B1F12')
 
for i in range(norm_df.shape[1]):
    for j in range(norm_df.shape[0]):
        val      = norm_df.iloc[j, i]
        text_col = 'white' if val > 0.6 or val < 0.25 else '#0B1F12'
        ax.text(j, i, f'{val:.2f}',
                ha='center', va='center',
                fontsize=9, color=text_col,
                fontweight='bold')
 
cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
cbar.set_label('Normalised (0 = low, 1 = high)',
               fontsize=9, color='#64748B')
cbar.ax.tick_params(labelsize=8)
 
# Hardcoded Pearson R annotation
ax.text(0.01, -0.14,
        f'Pearson R (Rain vs Veg) = {PEARSON_R}  '
        f'p = {PEARSON_P}',
        transform=ax.transAxes, fontsize=8.5,
        color='#64748B',
        bbox=dict(boxstyle='round,pad=0.4',
                  facecolor='white',
                  edgecolor='#E2E8F0', alpha=0.9))
 
ax.set_title(
    'Normalised Variable Heatmap — Risk Factors by FY\n'
    'Red = high value  ·  Green = low value',
    fontsize=11, fontweight='bold',
    color='#0B1F12', pad=10)
ax.spines[['top','right','left','bottom']].set_visible(False)
plt.tight_layout()
plt.show()