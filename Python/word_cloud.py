from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV (if not already loaded)
df = pd.read_csv('fomc_statements_analyzed_fixed.csv')

# Combine all FOMC statements into one big text
all_text = ' '.join(df['text'].dropna())

# Generate a Word Cloud
wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    colormap='Greens',  # 🟢 color theme!
    max_words=200,
    contour_color='black'
).generate(all_text)

# Plot the Word Cloud
plt.figure(figsize=(14,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('FOMC Statements Word Cloud (2020-2025)', fontsize=20)
plt.show()