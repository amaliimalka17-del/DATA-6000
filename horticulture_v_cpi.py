
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
 
df = dataset.copy()
df = df.dropna(subset=['CPI_Annual_Pct', 'Total_Production_Kt'])
df = df.sort_values('Financial_Year').reset_index(drop=True)
 
# Established capstone Pearson R values — do not change
PEARSON_R = -0.621
PEARSON_P = 0.2634
 
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')
 
yr_colours = ['#185FA5','#1E6B2E','#D85A30','#BA7517','#A32D2D']
for i, (_, row) in enumerate(df.iterrows()):
    col = yr_colours[i % len(yr_colours)]
    ax.scatter(row['CPI_Annual_Pct'],
               row['Total_Production_Kt'],
               color=col, s=130, zorder=5,
               edgecolors='white', linewidth=2)
    ax.annotate(row['Financial_Year'],
                (row['CPI_Annual_Pct'],
                 row['Total_Production_Kt']),
                textcoords='offset points',
                xytext=(8, 5), fontsize=9,
                color='#0B1F12', fontweight='bold')
 
slope, intercept, *_ = stats.linregress(
    df['CPI_Annual_Pct'], df['Total_Production_Kt'])
x_line = np.linspace(df['CPI_Annual_Pct'].min() * 0.8,
                     df['CPI_Annual_Pct'].max() * 1.1, 100)
ax.plot(x_line, intercept + slope * x_line,
        color='#D85A30', linewidth=1.5,
        linestyle='--', alpha=0.6, label='Trend line')
 
# Hardcoded Pearson R annotation
ax.text(0.05, 0.90,
        f'Pearson R = {PEARSON_R}\np = {PEARSON_P}',
        transform=ax.transAxes, fontsize=10,
        color='#64748B', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4',
                  facecolor='#FAEEDA',
                  edgecolor='#D85A30', alpha=0.85))
 
ax.set_xlabel('CPI Annual Change (%)',
              fontsize=10, color='#64748B')
ax.set_ylabel('Total Production (K tonnes)',
              fontsize=10, color='#64748B')
ax.set_title(
    'CPI vs Total Production — Scatter (FY 20/21–24/25)',
    fontsize=12, fontweight='bold',
    color='#0B1F12', pad=10)
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.xaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
ax.legend(fontsize=9, framealpha=0.9)
plt.tight_layout()
plt.show()