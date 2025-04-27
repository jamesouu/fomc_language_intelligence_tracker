import openai
import pandas as pd
import time

# --- Step 1: Set your OpenAI API key ---
client = openai.OpenAI(
    api_key="SD01balpPP4qjA"  # ⚠️ Replace with your working API key
)

# --- Step 2: Load your FOMC statements ---
df = pd.read_csv('fed_annoucement_202001-202503.csv')

# Fix the date column
df['date'] = pd.to_datetime(df['date'])

# Add new empty columns to store results
df['hawkishness_score'] = ""
df['reasoning'] = ""
df['top_3_topics'] = ""
df['full_response'] = ""

# --- Step 3: Create the prompt template ---
def create_prompt(text):
    return f"""
You are a Federal Reserve policy expert.

Task 1:
Classify the overall monetary policy tone of the following FOMC statement:
- 1 = Very Dovish
- 2 = Moderately Dovish
- 3 = Neutral
- 4 = Moderately Hawkish
- 5 = Very Hawkish

Task 2:
Explain your classification in 2 sentences.

Task 3:
Identify and list the top 3 economic issues discussed. For each issue, mention whether it is improving, worsening, or uncertain.

Statement:
{text}
"""

# --- Step 4: Process each FOMC statement ---
for idx, row in df.iterrows():
    print(f"Processing row {idx}...")  # Add live progress feedback
    prompt = create_prompt(row['text'])

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            timeout=30  # Set a 30-second timeout for API calls
        )

        content = response.choices[0].message.content

        # Save the full raw response
        df.at[idx, 'full_response'] = content

        # Parse basic fields
        lines = content.splitlines()
        first_line = lines[0].strip()

        if first_line and first_line[0] in '12345':
            df.at[idx, 'hawkishness_score'] = first_line[0]
            reasoning = []
            topics = []
            in_reasoning = True
            for line in lines[1:]:
                if "Task 3:" in line:
                    in_reasoning = False
                elif in_reasoning:
                    reasoning.append(line.strip())
                else:
                    topics.append(line.strip())
            df.at[idx, 'reasoning'] = " ".join(reasoning)
            df.at[idx, 'top_3_topics'] = " ".join(topics)

        time.sleep(1)  # Sleep between API calls to avoid rate limits

    except Exception as e:
        print(f"❌ Error processing row {idx}: {e}")
        continue

# --- Step 5: Save results to CSV ---
df.to_csv('fomc_statements_analyzed.csv', index=False)

print("✅ Analysis finished and results saved to fomc_statements_analyzed.csv!")
