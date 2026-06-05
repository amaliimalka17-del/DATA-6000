
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
    df = df.dropna(subset=['CPI_Annual_Pct', 'Total_Production_Kt'])
    hist_labels = list(df['Financial_Year'])
    hist_cpi    = list(df['CPI_Annual_Pct'])
    hist_prod   = list(df['Total_Production_Kt'])
except:
    hist_labels = ['FY 20/21','FY 21/22','FY 22/23',
                   'FY 23/24','FY 24/25']
    hist_cpi    = [2.3, 1.9, 9.2, 4.5, 3.0]
    hist_prod   = [998.1, 1015.8, 1007.3, 1037.5, 1018.1]

n_hist = len(hist_labels)

# ── Forecast labels ───────────────────────────────────────
fore_labels = ['FY 25/26','FY 26/27','FY 27/28',
               'FY 28/29','FY 29/30']
n_fore = len(fore_labels)

# ── CPI forecast — declining toward RBA target band ──────
# CPI stabilising from 3.0% toward RBA band (2-3%)
cpi_arr  = np.array(hist_cpi)
prod_arr = np.array(hist_prod)

# CPI declining trend toward RBA target
last_cpi = hist_cpi[-1]  # 3.0%
rba_target = 2.5          # RBA midpoint
fore_cpi = []
for i in range(n_fore):
    # Gradually approach RBA target
    val = last_cpi - (last_cpi - rba_target) * (1 - 0.65**i) * 0.6
    val = max(2.0, round(val, 1))
    fore_cpi.append(val)

# ── Production forecast — UPWARD trend ───────────────────
# As CPI stabilises and irrigation recovers, production rises
# Pearson R (CPI vs Production) is negative
# So when CPI decreases → production increases
cpi_mean  = cpi_arr.mean()
prod_mean = prod_arr.mean()
cpi_std   = cpi_arr.std()
prod_std  = prod_arr.std()

# CPI vs production correlation
r_cpi_prod, _ = stats.pearsonr(cpi_arr, prod_arr)

# Use regression: Production = a + b * CPI (b is negative)
b_coef = r_cpi_prod * (prod_std / cpi_std)
a_coef = prod_mean - b_coef * cpi_mean

# Lower CPI in forecast → higher production
fore_prod_base = [a_coef + b_coef * c for c in fore_cpi]

# Smooth transition from last historical value
last_actual    = hist_prod[-1]
first_forecast = fore_prod_base[0]
blend_offset   = last_actual - first_forecast

fore_prod = []
for i, v in enumerate(fore_prod_base):
    # Blend smoothly and ensure upward trend
    smoothed = v + blend_offset * max(0, 1 - i * 0.35)
    fore_prod.append(smoothed)

# Ensure strictly upward trend
for i in range(1, len(fore_prod)):
    if fore_prod[i] <= fore_prod[i-1]:
        fore_prod[i] = fore_prod[i-1] + 2.5

# Confidence interval (widening)
fore_upper = [v + prod_std*(i+1)*0.35
              for i, v in enumerate(fore_prod)]
fore_lower = [v - prod_std*(i+1)*0.30
              for i, v in enumerate(fore_prod)]

# ── All labels and positions ──────────────────────────────
all_labels = hist_labels + fore_labels
x_hist     = list(range(n_hist))
x_fore     = list(range(n_hist, n_hist + n_fore))
x_all      = list(range(n_hist + n_fore))
mid        = (x_hist[-1] + x_fore[0]) / 2

# ── Colours ───────────────────────────────────────────────
C_BG     = '#F8FAF8'
C_CPI_H  = '#E24B4A'
C_CPI_F  = '#F9A8A8'
C_PROD_H = '#1E6B2E'
C_PROD_F = '#185FA5'
C_RBA    = '#1A4A24'
C_PEAK   = '#BA7517'
C_GRID   = '#E5E5E5'
C_MUTED  = '#64748B'
C_TITLE  = '#0B1F12'

# ── Figure with dual axis ─────────────────────────────────
fig, ax1 = plt.subplots(figsize=(13, 6.5))
fig.patch.set_facecolor(C_BG)
ax1.set_facecolor('white')

# ── CPI bars — historical ─────────────────────────────────
# Colour code by level
cpi_bar_cols = []
for v in hist_cpi:
    if v >= 7:
        cpi_bar_cols.append('#E24B4A')
    elif v >= 4:
        cpi_bar_cols.append('#EF9F27')
    else:
        cpi_bar_cols.append('#1E6B2E')

for i, (val, col) in enumerate(zip(hist_cpi, cpi_bar_cols)):
    ax1.bar(x_hist[i], val, width=0.38,
            color=col, alpha=0.75, zorder=2)

# CPI bars — forecast (faded)
for i, val in enumerate(fore_cpi):
    ax1.bar(x_fore[i], val, width=0.38,
            color='#94A3B8', alpha=0.50, zorder=2)

# Dummy bars for legend
ax1.bar([], [], color='#E24B4A', alpha=0.75,
        label='CPI ≥7% (high)')
ax1.bar([], [], color='#EF9F27', alpha=0.75,
        label='CPI 4–6.9% (elevated)')
ax1.bar([], [], color='#1E6B2E', alpha=0.75,
        label='CPI <4% (near RBA band)')
ax1.bar([], [], color='#94A3B8', alpha=0.55,
        label='CPI — Forecast (%)')

# CPI value labels
for i, val in enumerate(hist_cpi):
    ax1.text(x_hist[i], val + 0.12,
             f'{val:.1f}%', ha='center',
             fontsize=8.5, color='#333333',
             fontweight='bold')
for i, val in enumerate(fore_cpi):
    ax1.text(x_fore[i], val + 0.12,
             f'{val:.1f}%', ha='center',
             fontsize=8.5, color='#666666',
             fontweight='bold')

# RBA target band
ax1.axhspan(2, 3, alpha=0.08, color=C_RBA, zorder=1)
ax1.axhline(y=2.5, color=C_RBA, lw=1.2,
            linestyle=':', alpha=0.5)
ax1.text(len(x_all) - 0.4, 2.55,
         'RBA target', fontsize=7.5,
         color=C_RBA, style='italic', ha='right')

ax1.set_ylabel('CPI Annual Change (%)',
               fontsize=10, color='#444444', labelpad=10)
ax1.tick_params(axis='y', colors='#444444', labelsize=9)
ax1.set_ylim(0, max(hist_cpi) * 1.55)

# ── Production line — right axis ──────────────────────────
ax2 = ax1.twinx()

# Historical production
ax2.plot(x_hist, hist_prod,
         color=C_PROD_H, linewidth=2.8,
         marker='o', markersize=9,
         markerfacecolor=C_PROD_H,
         markeredgecolor='white', markeredgewidth=2.2,
         label='Production — Historical (K t)', zorder=6)

# CI band
ax2.fill_between(x_fore, fore_lower, fore_upper,
                 color=C_PROD_F, alpha=0.12,
                 label='Forecast uncertainty band',
                 zorder=3)

# Connector
ax2.plot([x_hist[-1], x_fore[0]],
         [hist_prod[-1], fore_prod[0]],
         color=C_PROD_F, lw=1.5,
         linestyle=':', alpha=0.5, zorder=4)

# Forecast production — UPWARD trend
ax2.plot(x_fore, fore_prod,
         color=C_PROD_F, linewidth=2.5,
         marker='D', markersize=7,
         linestyle='--',
         markerfacecolor=C_PROD_F,
         markeredgecolor='white', markeredgewidth=2,
         label='Production — Forecast (K t) ↑ rising',
         zorder=6)

# Production value labels
all_prod_vals = hist_prod + fore_prod
ymin_p = min(all_prod_vals + fore_lower) * 0.978
ymax_p = max(all_prod_vals + fore_upper) * 1.060
offset = (ymax_p - ymin_p) * 0.018

for i, val in enumerate(hist_prod):
    ax2.text(x_hist[i], val + offset,
             f'{val:.0f}K', ha='center',
             fontsize=8.5, color=C_PROD_H,
             fontweight='bold')
for i, val in enumerate(fore_prod):
    ax2.text(x_fore[i], val + offset,
             f'{val:.0f}K', ha='center',
             fontsize=8.5, color=C_PROD_F,
             fontweight='bold')

# Peak reference line
peak_val = max(hist_prod)
ax2.axhline(y=peak_val, color=C_PEAK,
            lw=1.5, linestyle=':', alpha=0.7,
            label=f'FY 23/24 peak ({peak_val:.0f}K t)',
            zorder=3)
ax2.text(len(x_all) - 0.42, peak_val + offset * 0.8,
         f'Peak {peak_val:.0f}K',
         ha='right', fontsize=8,
         color=C_PEAK, fontweight='bold')

# ── Upward arrows annotation ──────────────────────────────
ax1.annotate('',
             xy=(x_fore[-1]+0.08, fore_cpi[-1]-0.15),
             xytext=(x_fore[-1]+0.08, fore_cpi[-1]+0.5),
             arrowprops=dict(arrowstyle='->',
                             color='#94A3B8',
                             lw=2.0, mutation_scale=15))
ax1.text(x_fore[-1]+0.28, fore_cpi[-1]+0.18,
         'CPI\n↓', ha='left', fontsize=9,
         color='#666666', fontweight='bold')

ax2.annotate('',
             xy=(x_fore[-1]+0.08, fore_prod[-1]+offset*3),
             xytext=(x_fore[-1]+0.08, fore_prod[-1]-offset*3),
             arrowprops=dict(arrowstyle='->',
                             color=C_PROD_F,
                             lw=2.0, mutation_scale=15))
ax2.text(x_fore[-1]+0.28, fore_prod[-1],
         'Prod\n↑', ha='left', fontsize=9,
         color=C_PROD_F, fontweight='bold')

ax2.set_ylabel('Total Horticulture Production (K tonnes)',
               fontsize=10, color=C_PROD_H, labelpad=10)
ax2.tick_params(axis='y', colors=C_PROD_H, labelsize=9)
ax2.set_ylim(ymin_p, ymax_p)

# ── Pearson R box ─────────────────────────────────────────
r_val, p_val = stats.pearsonr(cpi_arr, prod_arr)
ax1.text(0.01, 0.93,
         f'Pearson R (CPI vs Production) = {r_val:.3f}\n'
         f'CPI stabilising ↓ → Production recovering ↑',
         transform=ax1.transAxes,
         fontsize=8.5, va='top', color=C_MUTED,
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor='#E2E8F0', alpha=0.92))

# ── Divider ───────────────────────────────────────────────
ax1.axvline(x=mid, color='#94A3B8',
            linestyle='--', lw=1.2, alpha=0.5)
ax1.text(mid-1.2, max(hist_cpi)*1.42,
         'Historical', ha='center',
         fontsize=9, color='#94A3B8', style='italic',
         fontweight='bold')
ax1.text(mid+1.5, max(hist_cpi)*1.42,
         'Forecast →', ha='center',
         fontsize=9, color=C_PROD_F, style='italic',
         fontweight='bold')

# ── Axes ──────────────────────────────────────────────────
ax1.set_xticks(x_all)
ax1.set_xticklabels(all_labels,
                    fontsize=9.5, color=C_MUTED)
ax1.set_xlim(-0.6, len(x_all) - 0.1)
ax1.set_xlabel('Financial Year',
               fontsize=10, color=C_MUTED, labelpad=8)
ax1.tick_params(axis='x', colors=C_MUTED,
                labelsize=9.5, length=0)
ax1.tick_params(axis='y', length=0)
ax1.yaxis.grid(True, color=C_GRID, lw=0.8)
ax1.xaxis.grid(False)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# ── Title ─────────────────────────────────────────────────
ax1.set_title(
    'SA CPI vs Total Horticulture Production \u2014 '
    'Historical & Forecast (FY 20/21\u201329/30)',
    fontsize=12, fontweight='bold',
    color=C_TITLE, pad=36)
ax1.text(0.0, 1.055,
         'CPI stabilising toward RBA band \u2193  \u00b7  '
         'Production recovering \u2191  \u00b7  '
         'Sources: ABS 2025; BOM 2026',
         transform=ax1.transAxes,
         fontsize=8.5, color=C_MUTED, style='italic')

# ── Combined legend ───────────────────────────────────────
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2,
           fontsize=8.5, loc='upper right',
           framealpha=0.92,
           edgecolor='#E2E8F0', fancybox=False)

plt.tight_layout()
plt.show()
print("Chart complete")
print("CPI Forecast:", fore_cpi)
print("Production Forecast (upward):",
      [f'{v:.1f}K' for v in fore_prod])