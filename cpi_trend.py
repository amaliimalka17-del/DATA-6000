
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from scipy import stats

df = dataset.copy()
df = df.sort_values('Financial_Year').reset_index(drop=True)
df = df.dropna(subset=['CPI_Annual_Pct'])

x    = np.arange(len(df))
y    = df['CPI_Annual_Pct'].values
ymin = 0
ymax = y.max() * 1.25

# ── Trend line ────────────────────────────────────────────
slope, intercept, r, p, _ = stats.linregress(x, y)
trend = intercept + slope * x

# ── Peak index ────────────────────────────────────────────
peak_idx = int(np.argmax(y))

# ── Colours per bar ───────────────────────────────────────
C_BG    = '#F8FAF8'
C_GRID  = '#E5E5E5'
C_TITLE = '#0B1F12'
C_MUTED = '#64748B'
C_TREND = '#185FA5'
C_RBA   = '#1E6B2E'

bar_colours = []
for val in y:
    if val >= 7:
        bar_colours.append('#E24B4A')   # red — high inflation
    elif val >= 4:
        bar_colours.append('#EF9F27')   # amber — elevated
    else:
        bar_colours.append('#1E6B2E')   # green — within RBA band

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor('white')

# ── Bars ─────────────────────────────────────────────────
bars = ax.bar(x, y,
              color=bar_colours,
              width=0.5,
              zorder=3,
              edgecolor='white',
              linewidth=1.2)

# ── RBA target band ───────────────────────────────────────
ax.axhspan(2, 3, alpha=0.10,
           color=C_RBA, zorder=1)
ax.axhline(y=2, color=C_RBA, linewidth=1.2,
           linestyle=':', alpha=0.6, zorder=2)
ax.axhline(y=3, color=C_RBA, linewidth=1.2,
           linestyle=':', alpha=0.6, zorder=2)
ax.text(len(x) - 0.42, 2.48,
        'RBA target band (2\u20133%)',
        fontsize=8, color=C_RBA,
        style='italic', va='center')

# ── Trend line ────────────────────────────────────────────
ax.plot(x, trend,
        color=C_TREND, linewidth=1.8,
        linestyle='--', alpha=0.85, zorder=4,
        label=f'Trend  ({slope:+.1f}% / yr)')

# ── Value labels on bars ──────────────────────────────────
for bar, val in zip(bars, y):
    ax.text(bar.get_x() + bar.get_width() / 2,
            val + 0.15,
            f'{val:.1f}%',
            ha='center', fontsize=10,
            color=C_TITLE, fontweight='bold')

# ── Peak annotation ───────────────────────────────────────
ax.annotate(
    f'CPI peak\n{y[peak_idx]:.1f}%\n(FY 22/23)',
    (peak_idx, y[peak_idx]),
    textcoords='offset points',
    xytext=(0, 18),
    ha='center', fontsize=9,
    color='#E24B4A', fontweight='bold',
    arrowprops=dict(arrowstyle='-',
                    color='#E24B4A', lw=1.2))

# ── Decline arrow from peak to latest ────────────────────
ax.annotate('',
            xy=(len(x) - 1, y[-1] + 0.1),
            xytext=(peak_idx, y[peak_idx] - 0.1),
            arrowprops=dict(
                arrowstyle='->,head_width=0.25,'
                           'head_length=0.2',
                color='#185FA5', lw=1.5,
                connectionstyle='arc3,rad=-0.25'))
ax.text((peak_idx + len(x) - 1) / 2 + 0.5,
        (y[peak_idx] + y[-1]) / 2 + 0.8,
        f'{((y[-1] - y[peak_idx])):.1f}pp\ndecline',
        ha='center', fontsize=8.5,
        color='#185FA5', fontweight='bold')

# ── Stats annotation box ──────────────────────────────────
sig = 'p < 0.05 *' if p < 0.05 else f'p = {p:.3f}'
ax.text(0.01, 0.93,
        f'Linear slope: {slope:+.2f}% / yr\n'
        f'R\u00b2 = {r**2:.3f}   ({sig})',
        transform=ax.transAxes,
        fontsize=9, color=C_MUTED, va='top',
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
ax.set_ylabel('CPI Annual Change (%)',
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
    'SA CPI Annual Change \u2014 Trend Analysis '
    '(FY 20/21\u201324/25)',
    fontsize=13, fontweight='bold',
    color=C_TITLE, pad=14)
ax.text(0.0, 1.02,
        'Peak: 9.2% in FY 22/23  \u00b7  '
        'Now stabilising at 3.0%  \u00b7  '
        'Approaching RBA target band',
        transform=ax.transAxes,
        fontsize=8.5, color=C_MUTED,
        style='italic')

# ── Legend ────────────────────────────────────────────────
red_p   = mpatches.Patch(color='#E24B4A',
                          label='High inflation (\u22657%)')
amber_p = mpatches.Patch(color='#EF9F27',
                          label='Elevated inflation (4\u20136.9%)')
green_p = mpatches.Patch(color='#1E6B2E',
                          label='Within/near RBA band (<4%)')
rba_p   = mpatches.Patch(color=C_RBA, alpha=0.3,
                          label='RBA target band (2\u20133%)')
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles + [red_p, amber_p, green_p, rba_p],
    labels  + ['High inflation (\u22657%)',
               'Elevated (4\u20136.9%)',
               'Within/near RBA band (<4%)',
               'RBA target band (2\u20133%)'],
    fontsize=8.5, loc='upper right',
    framealpha=0.92,
    edgecolor='#E2E8F0',
    fancybox=False)

plt.tight_layout()
plt.show()