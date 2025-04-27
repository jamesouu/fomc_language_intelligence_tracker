import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
fomc_df = pd.read_csv('fomc_statements_analyzed_fixed.csv')
rates_df = pd.read_csv('fedfunds_monthly.csv')

# Make sure dates are datetime
fomc_df['date'] = pd.to_datetime(fomc_df['date'])
rates_df['observation_date'] = pd.to_datetime(rates_df['observation_date'])

# Merge
merged_df = pd.merge_asof(
    fomc_df.sort_values('date'),
    rates_df.sort_values('observation_date'),
    left_on='date',
    right_on='observation_date',
    direction='backward'
)

# Plot
fig, ax1 = plt.subplots(figsize=(12,6))

# Hawkishness
ax1.plot(merged_df['date'], merged_df['hawkishness_score'], label='Hawkishness',color='blue')
ax1.set_ylabel('Hawkishness Score', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Fed Funds Rate
ax2 = ax1.twinx()
ax2.plot(merged_df['date'], merged_df['FEDFUNDS'], label='Fed Funds Rate', color='green')
ax2.set_ylabel('Fed Funds Rate (%)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

fig.suptitle('FOMC Hawkishness vs Fed Funds Rate')
fig.legend(
    loc='upper left',
    bbox_to_anchor=(0.15, 0.85),  # Very close to the top-left inside
    frameon=True,                 # Add a light background box
    fontsize=10
)
plt.show()