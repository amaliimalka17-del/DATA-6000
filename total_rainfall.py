import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Total_Rainfall_mm'])
 
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')
 
colours = ['#E24B4A' if r < 1500 else '#185FA5'
           for r in df['Total_Rainfall_mm']]
bars = ax.bar(df['Financial_Year'], df['Total_Rainfall_mm'],
              color=colours, width=0.5, zorder=3)
 
for bar, val in zip(bars, df['Total_Rainfall_mm']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 20,
            f'{val:,.0f}mm', ha='center', va='bottom',
            fontsize=9, color='#0B1F12', fontweight='bold')
 
ax.set_title('SA Rainfall Trend (FY 20/21–24/25)',
             fontsize=12, fontweight='bold',
             color='#0B1F12', pad=10)
ax.set_ylabel('Total Rainfall (mm)', fontsize=10, color='#64748B')
ax.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#C0C0C0')
normal  = mpatches.Patch(color='#185FA5', label='Above 1,500mm')
decline = mpatches.Patch(color='#E24B4A', label='Below 1,500mm')
ax.legend(handles=[normal, decline], fontsize=8,
          loc='upper right', framealpha=0.9)
plt.tight_layout()
plt.show()