#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import openai
import time


# In[3]:


# Initialize OpenAI API key
openai.api_key = "YOUR-API-KEY"


# In[10]:


# Function to process a batch of press releases using OpenAI API
def label_press_releases_batch(batch):
    results = []
    for press_release_text in batch:
        prompt = f"""
You are analyzing official press releases published by the Turkish Ministry of Foreign Affairs. These releases usually convey emotional reactions to international events, though some are purely informative (such as announcing meetings or procedural updates).

Task:
For each given press release, return the following structured output:

Main Event Category: [Event Category]
Actor: [Actor]
Emotion: [Emotion]
Key Words/Phrases: [Keyword 1, Keyword 2, Keyword 3, Keyword 4, Keyword 5]

Emotion choices: Happiness, Sadness, Fear, Sympathy, Frustration, Hope, Anger, None (if no emotion detected).

Emotions (as guidelines):
- **Happiness**: This could be related to celebration, pride, approval, or successful outcomes. Look for signs of positive sentiment.
- **Sadness**: Look for mourning, loss, tragedy, or expressions of condolences. 
- **Fear**: Pay attention to language about threats, insecurity, or anxiety about future events.
- **Sympathy**: This might include expressions of solidarity, condolences, or empathy.
- **Frustration**: This can come across as dissatisfaction or difficulties faced, especially when progress is hindered.
- **Hope**: This typically reflects optimism, future expectations, or desires for positive change.
- **Anger**: Look for strong condemnation, outrage, or moral disapproval of certain events or actions.

Important Note:
- If no clear emotion is conveyed, feel free to choose "None" or skip the emotion label.


Examples:

Input: "Turkey strongly condemns the terrorist attack against civilians in Country X..."
Output:
Main Event Category: Terrorism
Actor: Country X
Emotion: Sadness
Key Words/Phrases: ["condemns", "terrorist attack", "civilians", "innocent victims", "solidarity"]

Input: "Turkey welcomes the signing of the trade agreement with Country Y..."
Output:
Main Event Category: Trade Agreement
Actor: Country Y
Emotion: Happiness
Key Words/Phrases: ["welcomes", "trade agreement", "significant step", "strengthening ties", "mutual benefit"]

---

Process each press release individually and return a list of structured outputs.

        Press Release Text:
        {press_release_text}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            result = response['choices'][0]['message']['content']
            results.append(result)
        except Exception as e:
            print(f"Error: {e}")
            results.append(None)
    return results


# In[12]:


# Load dataset from Excel file
input_file = "/Users/azadesel/Desktop/mfa_archive/mfa_2025_clean_woanalysis.xlsx"
output_file = "/Users/azadesel/Desktop/mfa_archive/mfa_en/processed_press_releases_2025.xlsx"  # Change as needed
df = pd.read_excel(input_file)

# Ensure the input dataset has a 'Body Text' column
if 'Body Text' not in df.columns:
    raise ValueError("The dataset must contain a 'Body Text' column.")

# Create an empty column for the combined analysis
df['Analysis'] = ""

# Process the data in batches
batch_size = 100
for start_idx in range(0, len(df), batch_size):
    end_idx = min(start_idx + batch_size, len(df))
    batch = df['Body Text'].iloc[start_idx:end_idx].tolist()
    
    # Get results for this batch
    results = label_press_releases_batch(batch)

    # Update the DataFrame with the results
    for i, result in enumerate(results):
        if result:
            try:
                # Combine all fields into a single 'Analysis' column
                df.at[start_idx + i, 'Analysis'] = result.strip()
            except Exception as e:
                print(f"Error parsing result for row {start_idx + i}: {e}")
    
    # Save periodically to avoid data loss
    df.to_excel(output_file, index=False)
    print(f"Processed batch {start_idx + 1}-{end_idx}, saving to {output_file}")

    # Sleep to avoid hitting rate limits (adjust based on your API limits)
    time.sleep(5)

# Final save to ensure all data is written
df.to_excel(output_file, index=False)
print(f"Final processed dataset saved to {output_file}")

