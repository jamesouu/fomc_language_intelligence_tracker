import pandas as pd
import matplotlib.pyplot as plt

# Load FOMC statements
fomc_df = pd.read_csv('fomc_statements_analyzed_fixed.csv')
fomc_df['date'] = pd.to_datetime(fomc_df['date'])

# Load Fed Funds monthly data
rates_df = pd.read_csv('fedfunds_monthly.csv')
rates_df['observation_date'] = pd.to_datetime(rates_df['observation_date'])
rates_df.rename(columns={'observation_date': 'rate_date', 'FEDFUNDS': 'FEDFUNDS'}, inplace=True)

# Merge: find the latest rate available BEFORE each FOMC statement
merged_df = pd.merge_asof(
    fomc_df.sort_values('date'),
    rates_df.sort_values('rate_date'),
    left_on='date',
    right_on='rate_date',
    direction='backward'
)

# Detect important policy shifts based on hawkishness score
important_events = []
for i in range(1, len(merged_df)):
    prev = merged_df.iloc[i - 1]
    curr = merged_df.iloc[i]

    if pd.notnull(prev['hawkishness_score']) and pd.notnull(curr['hawkishness_score']):
        change = int(curr['hawkishness_score']) - int(prev['hawkishness_score'])

        if change <= -1:
            important_events.append((curr['date'], 'Dovish Shift'))
        elif change >= 1:
            important_events.append((curr['date'], 'Hawkish Shift'))

# Plot
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Hawkishness Score
ax1.plot(merged_df['date'], merged_df['hawkishness_score'], linestyle='-', color='blue',
         label='Hawkishness Score')
ax1.set_ylabel('Hawkishness Score', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(0.8, 5.2)

# Plot Fed Funds Rate
ax2 = ax1.twinx()
ax2.plot(merged_df['date'], merged_df['FEDFUNDS'], color='green', linestyle='-', label='Fed Funds Rate (%)')
ax2.set_ylabel('Fed Funds Rate (%)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Annotate important FOMC shifts
for event_date, label in important_events:
    ax1.axvline(x=event_date, color='gray', linestyle='--', linewidth=1)
    ax1.text(
        event_date,
        ax1.get_ylim()[1] * 0.85,
        label,
        rotation=90,
        verticalalignment='center',
        fontsize=8,
        color='black',
        backgroundcolor='white'
    )

# Title and Grid
plt.title('FOMC Hawkishness Score and Fed Funds Rate (2020-2025)', fontsize=16)
ax1.grid(False)

# Combined Legend inside plot
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
fig.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.82, 0.15), fontsize=10, frameon=False)

plt.tight_layout()
plt.show()