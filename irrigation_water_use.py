
import matplotlib.pyplot as plt
import pandas as pd
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Irrigation_GL'])
 
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')
 
colours = ['#E24B4A' if v >= 1000 else '#185FA5'
           for v in df['Irrigation_GL']]
bars = ax.bar(df['Financial_Year'], df['Irrigation_GL'],
              color=colours, width=0.5, zorder=3)
 
for bar, val in zip(bars, df['Irrigation_GL']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 8,
            f'{val:,.0f} GL',
            ha='center', va='bottom',
            fontsize=9, color='#0B1F12', fontweight='bold')
 
ax.set_title('SA Agricultural Irrigation Water Use (GL)',
             fontsize=12, fontweight='bold',
             color='#0B1F12', pad=10)
ax.set_ylabel('Water Use (GL)', fontsize=10, color='#64748B')
ax.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#C0C0C0')
plt.tight_layout()
plt.show()