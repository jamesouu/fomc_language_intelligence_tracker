import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the CSV
df = pd.read_csv('fomc_statements_analyzed_fixed.csv')

# Fix the 'date' format
df['date'] = pd.to_datetime(df['date'])

# Function to extract score from full_response if hawkishness_score is missing
def extract_score(text):
    if pd.isna(text):
        return None
    match = re.search(r'(\d)\s*=', text)
    if match:
        return int(match.group(1))
    return None

# Fill hawkishness_score
df['hawkishness_score'] = pd.to_numeric(df['hawkishness_score'], errors='coerce')
df['hawkishness_score'] = df['hawkishness_score'].fillna(df['full_response'].apply(extract_score))

# Sort by date
df = df.sort_values('date')

# Calculate moving average (you can change window=3 if needed)
df['hawkishness_ma'] = df['hawkishness_score'].rolling(window=3, min_periods=1).mean()

# Plot
plt.figure(figsize=(12,6))
plt.plot(df['date'], df['hawkishness_score'], label='Original Hawkishness Score', linestyle='--', alpha=0.6)
plt.plot(df['date'], df['hawkishness_ma'], label='3-Meeting Moving Average', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Hawkishness Score\n(1 = Very Dovish, 5 = Very Hawkish)')
plt.title('FOMC Hawkishness Trend with Smoothing (2020-2025)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()