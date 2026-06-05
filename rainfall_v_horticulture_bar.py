

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Total_Fruit_Prod_t', 'Total_Veg_Prod_t'])
df['Fruit_Kt'] = df['Total_Fruit_Prod_t'] / 1000
df['Veg_Kt']   = df['Total_Veg_Prod_t']   / 1000
 
# Established capstone Pearson R values — do not change
PEARSON_R = -0.621
PEARSON_P = 0.2634
 
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7),
                                 sharex=True)
fig.patch.set_facecolor('#F8FAF8')
 
# Top panel: Rainfall
ax1.set_facecolor('white')
x = np.arange(len(df))
ax1.bar(x, df['Total_Rainfall_mm'],
        color='#185FA5', alpha=0.75,
        width=0.5, zorder=3, label='Rainfall (mm)')
for i, val in enumerate(df['Total_Rainfall_mm']):
    ax1.text(i, val + 20, f'{val:,.0f}mm',
             ha='center', fontsize=8,
             color='#185FA5', fontweight='bold')
ax1.set_ylabel('Rainfall (mm)', fontsize=10, color='#185FA5')
ax1.tick_params(colors='#64748B', labelsize=9)
ax1.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax1.set_axisbelow(True)
ax1.spines[['top','right','left']].set_visible(False)
ax1.set_title('SA Rainfall (mm)', fontsize=11,
              color='#0B1F12', pad=5)
 
# Hardcoded Pearson R on top panel
ax1.text(0.01, 0.90,
         f'Pearson R (Rain vs Veg) = {PEARSON_R}  '
         f'p = {PEARSON_P}',
         transform=ax1.transAxes, fontsize=8.5,
         color='#64748B',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='white',
                   edgecolor='#E2E8F0', alpha=0.9))
 
# Bottom panel: Fruit vs Veg grouped
ax2.set_facecolor('white')
ax2.bar(x - 0.2, df['Fruit_Kt'],
        width=0.35, color='#E8A230',
        label='Fruit (K t)', zorder=3)
ax2.bar(x + 0.2, df['Veg_Kt'],
        width=0.35, color='#1E6B2E',
        label='Vegetable (K t)', zorder=3)
 
for i, (f, v) in enumerate(zip(df['Fruit_Kt'], df['Veg_Kt'])):
    ax2.text(i - 0.2, f + 2, f'{f:.0f}K',
             ha='center', fontsize=7.5,
             color='#BA7517', fontweight='bold')
    ax2.text(i + 0.2, v + 2, f'{v:.0f}K',
             ha='center', fontsize=7.5,
             color='#1E6B2E', fontweight='bold')
 
ax2.set_xticks(x)
ax2.set_xticklabels(df['Financial_Year'],
                    fontsize=9, color='#64748B')
ax2.set_ylabel('Production (K tonnes)',
               fontsize=10, color='#64748B')
ax2.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax2.tick_params(colors='#64748B', labelsize=9)
ax2.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax2.set_axisbelow(True)
ax2.spines[['top','right','left']].set_visible(False)
ax2.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax2.set_title('Fruit vs Vegetable Production (K tonnes)',
              fontsize=11, color='#0B1F12', pad=5)
 
fig.suptitle(
    'SA Rainfall vs Fruit & Vegetable Production (FY 20/21–24/25)',
    fontsize=12, fontweight='bold',
    color='#0B1F12', y=0.990)
plt.tight_layout()
plt.show()