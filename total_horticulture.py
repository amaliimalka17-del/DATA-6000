
import matplotlib.pyplot as plt
import pandas as pd
 
df = dataset.copy()
df = df.sort_values('Financial_Year')
df = df.dropna(subset=['Total_Production_Kt'])
df['Fruit_Kt'] = df['Total_Fruit_Prod_t'] / 1000
df['Veg_Kt']   = df['Total_Veg_Prod_t']   / 1000
 
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor('#F8FAF8')
ax.set_facecolor('white')
 
x = range(len(df))
ax.bar(x, df['Veg_Kt'],   color='#185FA5', label='Vegetables',
       width=0.5, zorder=3)
ax.bar(x, df['Fruit_Kt'], color='#E8A230', label='Fruit',
       bottom=df['Veg_Kt'], width=0.5, zorder=3)
 
for i, (_, row) in enumerate(df.iterrows()):
    ax.text(i, row['Total_Production_Kt'] + 3,
            f"{row['Total_Production_Kt']:.0f}K",
            ha='center', va='bottom',
            fontsize=9, color='#0B1F12', fontweight='bold')
 
ax.set_xticks(list(x))
ax.set_xticklabels(df['Financial_Year'],
                   fontsize=9, color='#64748B')
ax.set_title('SA Horticulture Production by FY (K tonnes)',
             fontsize=12, fontweight='bold',
             color='#0B1F12', pad=10)
ax.set_ylabel('Production (K tonnes)',
              fontsize=10, color='#64748B')
ax.tick_params(colors='#64748B', labelsize=9)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#C0C0C0')
ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
plt.tight_layout()
plt.show()
