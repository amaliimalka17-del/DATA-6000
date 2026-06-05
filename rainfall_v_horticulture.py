
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Data ─────────────────────────────────────────────────
try:
    df = dataset.copy()
    df = df.sort_values('Financial_Year').reset_index(drop=True)
    df = df.dropna(subset=['Total_Rainfall_mm','Total_Production_Kt'])
    hist_labels = list(df['Financial_Year'])
    hist_rain   = list(df['Total_Rainfall_mm'])
    hist_prod   = list(df['Total_Production_Kt'])
except:
    hist_labels = ['FY 20/21','FY 21/22','FY 22/23',
                   'FY 23/24','FY 24/25']
    hist_rain   = [1829.4, 2152.2, 2686.6, 1531.0, 1351.8]
    hist_prod   = [998.1,  1015.8, 1007.3, 1037.5, 1018.1]

n_hist = len(hist_labels)
PEARSON_R = -0.621
PEARSON_P = 0.2634

# ── Forecast labels ───────────────────────────────────────
fore_labels = ['FY 25/26','FY 26/27','FY 27/28',
               'FY 28/29','FY 29/30']
n_fore = len(fore_labels)

# ── Rainfall forecast — declining BOM trend ───────────────
rain_arr = np.array(hist_rain)
prod_arr = np.array(hist_prod)
x_h      = np.arange(n_hist, dtype=float)
r_slope, r_intercept, *_ = stats.linregress(x_h, rain_arr)
fore_x    = np.arange(n_hist, n_hist + n_fore, dtype=float)
fore_rain = [max(750, r_intercept + r_slope * xi) for xi in fore_x]

# ── Production forecast — INVERSE of rainfall ────────────
# When rainfall DECREASES → production INCREASES (Pearson R = -0.621)
# Use regression: Production = a + b * Rainfall (b is negative)
# Scale: b = R * (std_prod / std_rain)
rain_mean  = rain_arr.mean()
prod_mean  = prod_arr.mean()
rain_std   = rain_arr.std()
prod_std   = prod_arr.std()
b_coef     = PEARSON_R * (prod_std / rain_std)   # negative slope
a_coef     = prod_mean - b_coef * rain_mean

# Apply inverse relationship to forecasted rainfall
# Lower rainfall → higher production forecast
fore_prod  = [a_coef + b_coef * r for r in fore_rain]

# Smooth transition from last historical value
# Blend from last actual to regression-based forecast
last_actual     = hist_prod[-1]
first_forecast  = fore_prod[0]
blend_offset    = last_actual - first_forecast
fore_prod = [v + blend_offset * max(0, 1 - i*0.4)
             for i, v in enumerate(fore_prod)]

# Confidence interval
fore_upper = [v + prod_std * (i+1) * 0.35 for i,v in enumerate(fore_prod)]
fore_lower = [v - prod_std * (i+1) * 0.35 for i,v in enumerate(fore_prod)]

# ── Labels and positions ──────────────────────────────────
all_labels = hist_labels + fore_labels
x_hist     = list(range(n_hist))
x_fore     = list(range(n_hist, n_hist + n_fore))
x_all      = list(range(n_hist + n_fore))
mid        = (x_hist[-1] + x_fore[0]) / 2

# ── Colours ───────────────────────────────────────────────
C_BG     = '#F8FAF8'
C_RAIN_H = '#185FA5'
C_RAIN_F = '#94A3B8'
C_PROD_H = '#1E6B2E'
C_PROD_F = '#E24B4A'
C_PEAK   = '#1A4A24'
C_GRID   = '#E5E5E5'
C_MUTED  = '#64748B'
C_TITLE  = '#0B1F12'

# ── Figure ────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(13, 6.5))
fig.patch.set_facecolor(C_BG)
ax1.set_facecolor('white')

# ── Rainfall bars ─────────────────────────────────────────
ax1.bar(x_hist, hist_rain, width=0.38,
        color=C_RAIN_H, alpha=0.70, zorder=2,
        label='Rainfall — Historical (mm)')
ax1.bar(x_fore, fore_rain, width=0.38,
        color=C_RAIN_F, alpha=0.55, zorder=2,
        label='Rainfall — Forecast (mm) \u2193 declining')

# Rainfall value labels
for i, val in enumerate(hist_rain):
    ax1.text(x_hist[i], val + 45,
             f'{val:,.0f}mm', ha='center',
             fontsize=8, color=C_RAIN_H, fontweight='bold')
for i, val in enumerate(fore_rain):
    ax1.text(x_fore[i], val + 45,
             f'{val:,.0f}mm', ha='center',
             fontsize=8, color=C_RAIN_F, fontweight='bold')

ax1.set_ylabel('Total Rainfall (mm)',
               fontsize=10, color=C_RAIN_H, labelpad=10)
ax1.tick_params(axis='y', colors=C_RAIN_H, labelsize=9)
ax1.set_ylim(0, max(hist_rain) * 1.52)

# ── Production line — right axis ──────────────────────────
ax2 = ax1.twinx()

# Historical
ax2.plot(x_hist, hist_prod,
         color=C_PROD_H, linewidth=2.8,
         marker='o', markersize=9,
         markerfacecolor=C_PROD_H,
         markeredgecolor='white', markeredgewidth=2.2,
         label='Production — Historical (K t)', zorder=6)

# CI band
ax2.fill_between(x_fore, fore_lower, fore_upper,
                 color=C_PROD_F, alpha=0.12,
                 label='Forecast uncertainty band', zorder=3)

# Connector
ax2.plot([x_hist[-1], x_fore[0]],
         [hist_prod[-1], fore_prod[0]],
         color=C_PROD_F, lw=1.5,
         linestyle=':', alpha=0.5, zorder=4)

# Forecast production — RISING as rainfall falls
ax2.plot(x_fore, fore_prod,
         color=C_PROD_F, linewidth=2.5,
         marker='D', markersize=7, linestyle='--',
         markerfacecolor=C_PROD_F,
         markeredgecolor='white', markeredgewidth=2,
         label='Production — Forecast (K t) \u2191 rising', zorder=6)

# Production value labels
all_prod_vals = hist_prod + fore_prod
ymin_p = min(all_prod_vals + fore_lower) * 0.978
ymax_p = max(all_prod_vals + fore_upper) * 1.055
offset = (ymax_p - ymin_p) * 0.018

for i, val in enumerate(hist_prod):
    ax2.text(x_hist[i], val + offset,
             f'{val:.0f}K', ha='center',
             fontsize=8.5, color=C_PROD_H, fontweight='bold')
for i, val in enumerate(fore_prod):
    ax2.text(x_fore[i], val + offset,
             f'{val:.0f}K', ha='center',
             fontsize=8.5, color=C_PROD_F, fontweight='bold')

# Peak reference line
peak_val = max(hist_prod)
ax2.axhline(y=peak_val, color=C_PEAK,
            linewidth=1.5, linestyle=':',
            alpha=0.7, zorder=3,
            label=f'FY 23/24 peak ({peak_val:.0f}K t)')
ax2.text(len(x_all) - 0.42, peak_val + offset * 0.8,
         f'Peak {peak_val:.0f}K',
         ha='right', fontsize=8,
         color=C_PEAK, fontweight='bold')

# ── Inverse relationship arrows annotation ────────────────
ax1.annotate('',
             xy=(x_fore[-1] + 0.1, max(hist_rain) * 0.22),
             xytext=(x_fore[-1] + 0.1, max(hist_rain) * 0.42),
             arrowprops=dict(arrowstyle='->', color=C_RAIN_F,
                             lw=2.0, mutation_scale=15))
ax1.text(x_fore[-1] + 0.28, max(hist_rain) * 0.32,
         'Rain\n\u2193',
         ha='left', fontsize=9,
         color=C_RAIN_F, fontweight='bold')

ax2.annotate('',
             xy=(x_fore[-1] + 0.1, fore_prod[-1] + offset * 3),
             xytext=(x_fore[-1] + 0.1, fore_prod[-1] - offset * 3),
             arrowprops=dict(arrowstyle='->', color=C_PROD_F,
                             lw=2.0, mutation_scale=15))
ax2.text(x_fore[-1] + 0.28, fore_prod[-1],
         'Prod\n\u2191',
         ha='left', fontsize=9,
         color=C_PROD_F, fontweight='bold')

ax2.set_ylabel('Total Horticulture Production (K tonnes)',
               fontsize=10, color=C_PROD_H, labelpad=10)
ax2.tick_params(axis='y', colors=C_PROD_H, labelsize=9)
ax2.set_ylim(ymin_p, ymax_p)

# ── Pearson R box ─────────────────────────────────────────
ax1.text(0.01, 0.07,
         f'Pearson R = {PEARSON_R}  (p = {PEARSON_P})\n'
         f'Rainfall \u2193 \u2192 Irrigation compensates \u2192 Production \u2191\n'
         f'(irrigation dependency — Murray-Darling Basin)',
         transform=ax1.transAxes,
         fontsize=8.5, color=C_MUTED,
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor='#E2E8F0', alpha=0.92))

# ── Divider ───────────────────────────────────────────────
ax1.axvline(x=mid, color='#94A3B8',
            linestyle='--', lw=1.2, alpha=0.5)
ax1.text(mid - 1.2,
         max(hist_rain) * 1.42,
         'Historical',
         ha='center', fontsize=9,
         color='#94A3B8', style='italic', fontweight='bold')
ax1.text(mid + 1.5,
         max(hist_rain) * 1.42,
         'Forecast \u2192',
         ha='center', fontsize=9,
         color=C_PROD_F, style='italic', fontweight='bold')

# ── Axes ──────────────────────────────────────────────────
ax1.set_xticks(x_all)
ax1.set_xticklabels(all_labels, fontsize=9.5, color=C_MUTED)
ax1.set_xlim(-0.6, len(x_all) - 0.1)
ax1.set_xlabel('Financial Year',
               fontsize=10, color=C_MUTED, labelpad=8)
ax1.tick_params(axis='x', colors=C_MUTED, labelsize=9.5, length=0)
ax1.tick_params(axis='y', length=0)
ax1.yaxis.grid(True, color=C_GRID, lw=0.8)
ax1.xaxis.grid(False)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# ── Title ─────────────────────────────────────────────────
ax1.set_title(
    'SA Rainfall vs Total Horticulture Production \u2014 '
    'Historical & Forecast (FY 20/21\u201329/30)',
    fontsize=12, fontweight='bold', color=C_TITLE, pad=36)
ax1.text(0.0, 1.055,
         'Rainfall declining \u2193  \u00b7  '
         'Production rising \u2191 (irrigation dependency, R = \u22120.621)  \u00b7  '
         'Sources: BOM 2026; ABS 2025; DEW 2025',
         transform=ax1.transAxes,
         fontsize=8.5, color=C_MUTED, style='italic')

# ── Legend ────────────────────────────────────────────────
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2,
           fontsize=8.5, loc='upper right',
           framealpha=0.92,
           edgecolor='#E2E8F0', fancybox=False)

plt.tight_layout()
plt.show()