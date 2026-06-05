
import matplotlib.pyplot as plt
import pandas as pd
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['CPI_Annual_Pct'])
 
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')
 
colours = ['#E24B4A' if v >= 7
           else '#EF9F27' if v >= 4
           else '#1E6B2E'
           for v in df['CPI_Annual_Pct']]
bars = ax.bar(df['Financial_Year'], df['CPI_Annual_Pct'],
              color=colours, width=0.5, zorder=3)
 
for bar, val in zip(bars, df['CPI_Annual_Pct']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.1,
            f'{val:.1f}%', ha='center', va='bottom',
            fontsize=9, color='#0B1F12', fontweight='bold')
 
ax.axhspan(2, 3, alpha=0.08, color='#1E6B2E')
ax.axhline(y=2, color='#1E6B2E', linewidth=1,
           linestyle='--', alpha=0.5, label='RBA target band (2–3%)')
ax.axhline(y=3, color='#1E6B2E', linewidth=1,
           linestyle='--', alpha=0.5)
 
ax.set_title('SA CPI Annual Change (%)',
             fontsize=12, fontweight='bold',
             color='#0B1F12', pad=10)
ax.set_ylabel('CPI %', fontsize=10, color='#64748B')
ax.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#C0C0C0')
ax.legend(fontsize=8, framealpha=0.9)
plt.tight_layout()
plt.show()