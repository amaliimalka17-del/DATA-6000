
import matplotlib.pyplot as plt
import pandas as pd
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Risk_Score'])
 
colour_map = {'High':'#E24B4A','Medium':'#EF9F27','Low':'#1E6B2E'}
colours = [colour_map.get(r, '#185FA5') for r in df['Risk_Level']]
 
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')
 
bars = ax.bar(df['Financial_Year'], df['Risk_Score'],
              color=colours, width=0.5, zorder=3)
 
for bar, val, lvl in zip(bars, df['Risk_Score'], df['Risk_Level']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            f'{val:.0f} — {lvl}',
            ha='center', va='bottom',
            fontsize=9, color='#0B1F12', fontweight='bold')
 
ax.axhline(y=40, color='#E24B4A', linewidth=1.2,
           linestyle='--', alpha=0.6, label='High threshold (40)')
ax.axhline(y=20, color='#EF9F27', linewidth=1.2,
           linestyle='--', alpha=0.6, label='Medium threshold (20)')
 
ax.set_ylim(0, 70)
ax.set_title('Supply Disruption Risk Score by FY',
             fontsize=12, fontweight='bold',
             color='#0B1F12', pad=10)
ax.set_ylabel('Risk Score (0–100)',
              fontsize=10, color='#64748B')
ax.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#C0C0C0')
ax.legend(fontsize=8, framealpha=0.9)
plt.tight_layout()
plt.show()