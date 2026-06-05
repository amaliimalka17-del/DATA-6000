
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from scipy import stats

df = dataset.copy()
df = df.sort_values('Financial_Year').reset_index(drop=True)
df = df.dropna(subset=['Total_Production_Kt'])

x     = np.arange(len(df))
y     = df['Total_Production_Kt'].values
ymin  = y.min() * 0.985
ymax  = y.max() * 1.025

# ── Trend line ────────────────────────────────────────────
slope, intercept, r, p, _ = stats.linregress(x, y)
trend = intercept + slope * x

# ── Peak and trough ───────────────────────────────────────
peak_idx  = int(np.argmax(y))
trough_idx = int(np.argmin(y))

# ── Colours ───────────────────────────────────────────────
C_BG    = '#F8FAF8'
C_HIST  = '#1E6B2E'
C_TREND = '#E24B4A'
C_PEAK  = '#BA7517'
C_TROUGH = '#185FA5'
C_GRID  = '#E5E5E5'
C_TITLE = '#0B1F12'
C_MUTED = '#64748B'

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor('white')

# ── Shaded area under production line ─────────────────────
ax.fill_between(x, ymin, y,
                color=C_HIST, alpha=0.07, zorder=1)

# ── Production line ───────────────────────────────────────
ax.plot(x, y,
        color=C_HIST, linewidth=2.8,
        marker='o', markersize=9,
        markerfacecolor=C_HIST,
        markeredgecolor='white',
        markeredgewidth=2.2,
        label='Total Production (K t)',
        zorder=5)

# ── Trend line ────────────────────────────────────────────
ax.plot(x, trend,
        color=C_TREND, linewidth=1.8,
        linestyle='--', alpha=0.85,
        label=f'Trend  ({slope:+.1f}K t/yr)',
        zorder=4)

# ── Highlight peak ────────────────────────────────────────
ax.scatter(peak_idx, y[peak_idx],
           color=C_PEAK, s=160, zorder=7,
           edgecolors='white', linewidth=2.5)
ax.annotate(f'Peak\n{y[peak_idx]:.0f}K t',
            (peak_idx, y[peak_idx]),
            textcoords='offset points',
            xytext=(0, 18),
            ha='center', fontsize=8.5,
            color=C_PEAK, fontweight='bold',
            arrowprops=dict(arrowstyle='-',
                            color=C_PEAK,
                            lw=1.2))

# ── Highlight trough ──────────────────────────────────────
ax.scatter(trough_idx, y[trough_idx],
           color=C_TROUGH, s=160, zorder=7,
           edgecolors='white', linewidth=2.5)
ax.annotate(f'Lowest\n{y[trough_idx]:.0f}K t',
            (trough_idx, y[trough_idx]),
            textcoords='offset points',
            xytext=(0, -32),
            ha='center', fontsize=8.5,
            color=C_TROUGH, fontweight='bold',
            arrowprops=dict(arrowstyle='-',
                            color=C_TROUGH,
                            lw=1.2))

# ── Value labels on all points ────────────────────────────
for i, val in enumerate(y):
    offset = 14 if i != trough_idx else -22
    ax.text(i, val + (ymax - ymin) * 0.012,
            f'{val:.0f}K',
            ha='center', fontsize=9,
            color=C_HIST, fontweight='bold')

# ── Post-peak decline arrow ───────────────────────────────
ax.annotate('',
            xy=(len(x) - 1, y[-1]),
            xytext=(peak_idx, y[peak_idx]),
            arrowprops=dict(
                arrowstyle='->,head_width=0.25,head_length=0.15',
                color='#E24B4A', lw=1.5,
                connectionstyle='arc3,rad=-0.2'))
ax.text((peak_idx + len(x) - 1) / 2 + 0.3,
        (y[peak_idx] + y[-1]) / 2 + 4,
        f'{((y[-1] - y[peak_idx]) / y[peak_idx] * 100):+.1f}%\nsince peak',
        ha='center', fontsize=8,
        color='#E24B4A', fontweight='bold')

# ── Stats annotation box ──────────────────────────────────
sig = 'p < 0.05 *' if p < 0.05 else f'p = {p:.3f}'
ax.text(0.01, 0.05,
        f'Linear slope: {slope:+.1f}K t/yr\n'
        f'R\u00b2 = {r**2:.3f}   ({sig})',
        transform=ax.transAxes,
        fontsize=9, color=C_MUTED,
        bbox=dict(boxstyle='round,pad=0.5',
                  facecolor='white',
                  edgecolor='#E2E8F0',
                  alpha=0.9))

# ── Axes ─────────────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(df['Financial_Year'],
                   fontsize=10, color=C_MUTED)
ax.set_xlim(-0.5, len(x) - 0.5)
ax.set_ylim(ymin, ymax)
ax.set_ylabel('Total Horticulture Production (K tonnes)',
              fontsize=10, color=C_MUTED, labelpad=10)
ax.set_xlabel('Financial Year',
              fontsize=10, color=C_MUTED, labelpad=8)
ax.tick_params(colors=C_MUTED, labelsize=9, length=0)
ax.yaxis.grid(True, color=C_GRID,
              linewidth=0.8, linestyle='-')
ax.xaxis.grid(False)
ax.set_axisbelow(True)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color('#C0C0C0')

# ── Title ─────────────────────────────────────────────────
ax.set_title(
    'SA Total Horticulture Production \u2014 Trend Analysis '
    '(FY 20/21\u201324/25)',
    fontsize=13, fontweight='bold',
    color=C_TITLE, pad=14)
ax.text(0.0, 1.02,
        'Peak: FY 23/24 (1,037.5K t)  \u00b7  '
        'FY 24/25: 1,018.1K t  \u00b7  '
        'Post-peak decline signals supply constraint',
        transform=ax.transAxes,
        fontsize=8.5, color=C_MUTED,
        style='italic')

# ── Legend ────────────────────────────────────────────────
peak_patch   = mpatches.Patch(color=C_PEAK,
                               label='Production peak (FY 23/24)')
trough_patch = mpatches.Patch(color=C_TROUGH,
                               label='Production low (FY 20/21)')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles + [peak_patch, trough_patch],
          labels  + ['Production peak (FY 23/24)',
                     'Production low (FY 20/21)'],
          fontsize=8.5, loc='lower right',
          framealpha=0.92,
          edgecolor='#E2E8F0',
          fancybox=False)

plt.tight_layout()
plt.show()