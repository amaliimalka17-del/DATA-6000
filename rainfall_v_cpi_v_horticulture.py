
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Total_Rainfall_mm',
                        'CPI_Annual_Pct',
                        'Total_Production_Kt'])
 
# Established capstone Pearson R values — do not change
PEARSON_R = -0.621
PEARSON_P = 0.2634
 
fig, ax1 = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#F8FAF8')
ax1.set_facecolor('white')
 
x = np.arange(len(df))
 
# Rainfall bars (left axis)
ax1.bar(x, df['Total_Rainfall_mm'],
        width=0.4, color='#185FA5',
        alpha=0.5, label='Rainfall (mm)', zorder=2)
ax1.set_ylabel('Total Rainfall (mm)',
               fontsize=10, color='#185FA5')
ax1.tick_params(axis='y', colors='#185FA5', labelsize=9)
ax1.set_ylim(0, df['Total_Rainfall_mm'].max() * 1.5)
 
# Production line (right axis)
ax2 = ax1.twinx()
ax2.plot(x, df['Total_Production_Kt'],
         color='#1E6B2E', linewidth=2.5,
         marker='o', markersize=7,
         markerfacecolor='#1E6B2E',
         markeredgecolor='white', markeredgewidth=2,
         label='Production (K t)', zorder=5)
ax2.set_ylabel('Production (K tonnes)',
               fontsize=10, color='#1E6B2E')
ax2.tick_params(axis='y', colors='#1E6B2E', labelsize=9)
ax2.set_ylim(df['Total_Production_Kt'].min() * 0.95,
             df['Total_Production_Kt'].max() * 1.15)
 
# CPI line (third axis)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 55))
ax3.plot(x, df['CPI_Annual_Pct'],
         color='#D85A30', linewidth=2,
         marker='s', markersize=6,
         markerfacecolor='#D85A30',
         markeredgecolor='white', markeredgewidth=1.5,
         linestyle='--', label='CPI (%)', zorder=4)
ax3.set_ylabel('CPI Annual Change (%)',
               fontsize=10, color='#D85A30')
ax3.tick_params(axis='y', colors='#D85A30', labelsize=9)
ax3.set_ylim(0, df['CPI_Annual_Pct'].max() * 2.5)
 
# Production value labels
for i, val in enumerate(df['Total_Production_Kt']):
    ax2.text(i, val + 3, f'{val:.0f}K',
             ha='center', fontsize=8,
             color='#1E6B2E', fontweight='bold')
 
# Hardcoded Pearson R annotation
ax1.text(0.01, 0.06,
         f'Pearson R (Rain vs Veg) = {PEARSON_R}  '
         f'p = {PEARSON_P}',
         transform=ax1.transAxes, fontsize=8.5,
         color='#64748B',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='white',
                   edgecolor='#E2E8F0', alpha=0.9))
 
ax1.set_xticks(x)
ax1.set_xticklabels(df['Financial_Year'],
                    fontsize=9, color='#64748B')
ax1.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax1.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
 
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
h3, l3 = ax3.get_legend_handles_labels()
ax1.legend(h1+h2+h3, l1+l2+l3,
           fontsize=8, loc='upper left', framealpha=0.9)
 
fig.suptitle(
    'Rainfall, CPI & Horticulture Production — FY 20/21–24/25',
    fontsize=12, fontweight='bold',
    color='#0B1F12', y=0.992)
plt.tight_layout()
plt.show()