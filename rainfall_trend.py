

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

df = dataset.copy()
df = df.sort_values('Financial_Year').reset_index(drop=True)

x = np.arange(len(df))
y = df['Total_Rainfall_mm'].values

# Calculate trend line
slope, intercept, r, p, se = stats.linregress(x, y)
trend = intercept + slope * x

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')

# Actual data line
ax.plot(x, y,
        color='#185FA5', linewidth=2.5,
        marker='o', markersize=8,
        markerfacecolor='#185FA5',
        markeredgecolor='white',
        markeredgewidth=2,
        label='Actual Rainfall')

# Trend line
ax.plot(x, trend,
        color='#E24B4A', linewidth=1.8,
        linestyle='--',
        label=f'Trend ({slope:.0f}mm/yr)')

# Value labels
for i, val in enumerate(y):
    ax.text(i, val + 40, f'{val:,.0f}mm',
            ha='center', fontsize=8,
            color='#185FA5', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(df['Financial_Year'],
                   fontsize=9, color='#64748B')
ax.set_ylabel('Rainfall (mm)',
              fontsize=10, color='#64748B')
ax.set_title('SA Rainfall Trend (FY 20/21–24/25)',
             fontsize=12, fontweight='bold',
             color='#0B1F12', pad=10)
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
ax.legend(fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.show()