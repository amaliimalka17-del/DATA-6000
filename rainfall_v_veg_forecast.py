
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from scipy import stats
 
df = dataset.copy()
df = df.sort_values('Financial_Year').reset_index(drop=True)
df = df.dropna(subset=['Total_Rainfall_mm', 'Total_Veg_Prod_t'])
df['Veg_Kt'] = df['Total_Veg_Prod_t'] / 1000
 
# Hardcoded Pearson R — do not change
PEARSON_R = -0.621
PEARSON_P = 0.2634
 
# Historical data points
hist_labels = list(df['Financial_Year'])
hist_rain   = list(df['Total_Rainfall_mm'])
hist_veg    = list(df['Veg_Kt'])
 
# Forecast years: FY 25/26 to 29/30
# Rainfall forecast: continuing BOM declining trend
# (-157.6mm/yr from linear trend on FY data)
rain_slope  = -157.6
rain_last   = df['Total_Rainfall_mm'].iloc[-1]
fore_labels = ['25/26','26/27','27/28','28/29','29/30']
fore_rain   = [max(800, rain_last + rain_slope * (i+1))
               for i in range(5)]
 
# Use linear regression to project veg from rainfall forecast
slope_rv, intercept_rv, *_ = stats.linregress(
    df['Total_Rainfall_mm'], df['Veg_Kt'])
fore_veg = [intercept_rv + slope_rv * r for r in fore_rain]
 
# Uncertainty band: ±1 std of residuals
residuals = df['Veg_Kt'] - (intercept_rv +
            slope_rv * df['Total_Rainfall_mm'])
sigma      = residuals.std()
fore_lo    = [v - 1.5*sigma for v in fore_veg]
fore_hi    = [v + 1.5*sigma for v in fore_veg]
 
all_labels = hist_labels + fore_labels
x_all      = np.arange(len(all_labels))
x_hist     = x_all[:len(hist_labels)]
x_fore     = x_all[len(hist_labels):]
 
fig, ax1 = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#F8FAF8')
ax1.set_facecolor('white')
 
# Rainfall bars
colours_rain = (['#185FA5'] * len(hist_labels) +
                ['#94A3B8'] * len(fore_labels))
ax1.bar(x_all, hist_rain + fore_rain,
        width=0.4, color=colours_rain,
        alpha=0.55, label='Rainfall (mm)', zorder=2)
ax1.set_ylabel('Total Rainfall (mm)',
               fontsize=10, color='#185FA5')
ax1.tick_params(axis='y', colors='#185FA5', labelsize=9)
ax1.set_ylim(0, max(hist_rain + fore_rain) * 1.45)
 
# Veg production line (right axis)
ax2 = ax1.twinx()
ax2.plot(x_hist, hist_veg,
         color='#1E6B2E', linewidth=2.5,
         marker='o', markersize=8,
         markerfacecolor='#1E6B2E',
         markeredgecolor='white', markeredgewidth=2,
         label='Historical Veg (K t)', zorder=6)
ax2.plot(x_fore, fore_veg,
         color='#E24B4A', linewidth=2.2,
         marker='D', markersize=7, linestyle='--',
         markerfacecolor='#E24B4A',
         markeredgecolor='white', markeredgewidth=2,
         label='Forecast Veg (K t)', zorder=6)
ax2.fill_between(x_fore, fore_lo, fore_hi,
                 color='#E24B4A', alpha=0.12,
                 label='Forecast uncertainty band')
 
# Dotted connector
ax2.plot([x_hist[-1], x_fore[0]],
         [hist_veg[-1], fore_veg[0]],
         color='#E24B4A', linewidth=1.2,
         linestyle=':', alpha=0.5, zorder=4)
 
ax2.set_ylabel('Vegetable Production (K tonnes)',
               fontsize=10, color='#1E6B2E')
ax2.tick_params(axis='y', colors='#1E6B2E', labelsize=9)
ymin = min(min(hist_veg), min(fore_lo)) * 0.97
ymax = max(max(hist_veg), max(fore_hi)) * 1.06
ax2.set_ylim(ymin, ymax)
 
# Value labels
for i, val in enumerate(hist_veg):
    ax2.text(x_hist[i], val + (ymax-ymin)*0.015,
             f'{val:.0f}K', ha='center', fontsize=8,
             color='#1E6B2E', fontweight='bold')
for i, val in enumerate(fore_veg):
    ax2.text(x_fore[i], val + (ymax-ymin)*0.015,
             f'{val:.0f}K', ha='center', fontsize=8,
             color='#E24B4A', fontweight='bold')
 
# Divider
mid = (x_hist[-1] + x_fore[0]) / 2
ax1.axvline(x=mid, color='#94A3B8',
            linestyle='--', linewidth=1.2, alpha=0.5)
ax1.text(mid - 0.9, ax1.get_ylim()[1]*0.92,
         'Historical', ha='center', fontsize=9,
         color='#94A3B8', style='italic', fontweight='bold')
ax1.text(mid + 1.3, ax1.get_ylim()[1]*0.92,
         'Forecast →', ha='center', fontsize=9,
         color='#E24B4A', style='italic', fontweight='bold')
 
# Pearson R annotation
ax1.text(0.01, 0.06,
         f'Pearson R = {PEARSON_R}  p = {PEARSON_P}',
         transform=ax1.transAxes, fontsize=9,
         color='#64748B',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='white',
                   edgecolor='#E2E8F0', alpha=0.9))
 
ax1.set_xticks(x_all)
ax1.set_xticklabels(all_labels, fontsize=9, color='#64748B')
ax1.set_xlabel('Financial Year', fontsize=10, color='#64748B')
ax1.yaxis.grid(True, color='#E5E5E5', linewidth=0.8)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
 
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, fontsize=8,
           loc='upper right', framealpha=0.9)
 
fig.suptitle(
    'SA Rainfall vs Vegetable Production — Historical & Forecast '
    '(FY 20/21–29/30)',
    fontsize=12, fontweight='bold',
    color='#0B1F12', y=0.992)
fig.text(0.5, -0.03,
         'Forecast based on BOM declining rainfall trend '
         f'({rain_slope:.0f}mm/yr)  |  '
         f'Pearson R = {PEARSON_R}  Sources: BOM 2026; ABS 2025',
         ha='center', fontsize=8.5,
         color='#64748B', style='italic')
plt.tight_layout()
plt.show()