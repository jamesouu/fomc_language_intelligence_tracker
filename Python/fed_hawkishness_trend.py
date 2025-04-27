import pandas as pd
import matplotlib.pyplot as plt

# Load the fixed CSV
df = pd.read_csv('fomc_statements_analyzed_fixed.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Drop missing hawkishness scores
df = df.dropna(subset=['hawkishness_score'])

# Sort by date
df = df.sort_values('date')

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['hawkishness_score'], marker='o', linestyle='-', linewidth=2, color='blue')

# Beautify the chart
plt.title('FOMC Hawkishness Over Time (2020–2025)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Hawkishness Score (1 = Very Dovish, 5 = Very Hawkish)', fontsize=14)
plt.ylim(1, 5)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
plt.savefig('fomc_hawkishness_trend_fixed.png', dpi=300)

# Show the plot
plt.show()