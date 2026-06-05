
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Total_Rainfall_mm'])
df['Veg_Kt'] = df['Total_Veg_Prod_t'] / 1000
 
fig, ax1 = plt.subplots(figsize=(9, 4.5))
fig.patch.set_facecolor('#F8FAF8')
ax1.set_facecolor('white')
 
x = np.arange(len(df))
 
# Rainfall bars (left axis)
bars = ax1.bar(x - 0.2, df['Total_Rainfall_mm'],
               width=0.35, color='#185FA5',
               alpha=0.75, label='Rainfall (mm)', zorder=3)
ax1.set_ylabel('Total Rainfall (mm)',
               fontsize=10, color='#185FA5')
ax1.tick_params(axis='y', colors='#185FA5', labelsize=9)
ax1.set_ylim(0, df['Total_Rainfall_mm'].max() * 1.3)
 
# Veg production line (right axis)
ax2 = ax1.twinx()
ax2.plot(x + 0.2, df['Veg_Kt'],
         color='#1E6B2E', linewidth=2.5,
         marker='o', markersize=7,
         markerfacecolor='#1E6B2E', markeredgecolor='white',
         markeredgewidth=2, label='Veg Production (K t)', zorder=5)
ax2.set_ylabel('Vegetable Production (K tonnes)',
               fontsize=10, color='#1E6B2E')
ax2.tick_params(axis='y', colors='#1E6B2E', labelsize=9)
ax2.set_ylim(df['Veg_Kt'].min() * 0.95,
             df['Veg_Kt'].max() * 1.10)
 
# Value labels
for i, val in enumerate(df['Total_Rainfall_mm']):
    ax1.text(i - 0.2, val + 30, f'{val:,.0f}',
             ha='center', fontsize=8,
             color='#185FA5', fontweight='bold')
for i, val in enumerate(df['Veg_Kt']):
    ax2.text(i + 0.2, val + 3, f'{val:.0f}K',
             ha='center', fontsize=8,
             color='#1E6B2E', fontweight='bold')
 
ax1.set_xticks(x)
ax1.set_xticklabels(df['Financial_Year'],
                    fontsize=9, color='#64748B')
ax1.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax1.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax1.set_axisbelow(True)
ax1.spines[['top']].set_visible(False)
ax2.spines[['top']].set_visible(False)
 
# Pearson R annotation
from scipy import stats
r, p = stats.pearsonr(df['Total_Rainfall_mm'], df['Veg_Kt'])
ax1.text(0.02, 0.93,
         f'Pearson R = {r:.3f}  (p = {p:.4f})',
         transform=ax1.transAxes, fontsize=9,
         color='#64748B',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='white',
                   edgecolor='#E2E8F0', alpha=0.9))
 
# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           fontsize=8, loc='upper right', framealpha=0.9)
 
fig.suptitle('SA Rainfall vs Vegetable Production (FY 20/21–24/25)',
             fontsize=12, fontweight='bold',
             color='#0B1F12', y=0.99)
plt.tight_layout()
plt.show()