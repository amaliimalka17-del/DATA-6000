

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Irrigation_GL', 'Total_Rainfall_mm'])
 
# Established capstone Pearson R values — do not change
PEARSON_R = -0.621
PEARSON_P = 0.2634
 
fig, ax1 = plt.subplots(figsize=(9, 4.5))
fig.patch.set_facecolor('#F8FAF8')
ax1.set_facecolor('white')
 
x = np.arange(len(df))
 
ax1.bar(x - 0.18, df['Irrigation_GL'],
        width=0.35, color='#E24B4A',
        alpha=0.8, label='Irrigation (GL)', zorder=3)
ax1.set_ylabel('Irrigation Water Use (GL)',
               fontsize=10, color='#E24B4A')
ax1.tick_params(axis='y', colors='#E24B4A', labelsize=9)
ax1.set_ylim(0, df['Irrigation_GL'].max() * 1.35)
 
ax2 = ax1.twinx()
ax2.plot(x + 0.18, df['Total_Rainfall_mm'],
         color='#185FA5', linewidth=2.5,
         marker='o', markersize=7,
         markerfacecolor='#185FA5',
         markeredgecolor='white', markeredgewidth=2,
         label='Rainfall (mm)', zorder=5)
ax2.set_ylabel('Total Rainfall (mm)',
               fontsize=10, color='#185FA5')
ax2.tick_params(axis='y', colors='#185FA5', labelsize=9)
ax2.set_ylim(0, df['Total_Rainfall_mm'].max() * 1.4)
 
for i, val in enumerate(df['Irrigation_GL']):
    ax1.text(i - 0.18, val + 15, f'{val:,.0f}GL',
             ha='center', fontsize=8,
             color='#A32D2D', fontweight='bold')
for i, val in enumerate(df['Total_Rainfall_mm']):
    ax2.text(i + 0.18, val + 30, f'{val:,.0f}mm',
             ha='center', fontsize=8,
             color='#185FA5', fontweight='bold')
 
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
ax2.spines['top'].set_visible(False)
 
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, fontsize=8,
           loc='upper left', framealpha=0.9)
 
fig.suptitle(
    'Irrigation Water Use vs SA Rainfall — Drought Buffer Breakdown',
    fontsize=12, fontweight='bold',
    color='#0B1F12', y=0.992)
fig.text(0.5, -0.03,
         'As rainfall fell, irrigation intensified — '
         'confirming buffer exhaustion by FY 2023/24',
         ha='center', fontsize=9,
         color='#64748B', style='italic')
plt.tight_layout()
plt.show()