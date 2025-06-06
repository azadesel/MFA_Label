

import pandas as pd
import openai
import time


# Set your OpenAI API key
openai.api_key = "YOUR-API-KEY"


file_path = "FILE-PATH"
unique_tr = pd.read_excel(file_path)

# Assuming unique_tr is a pandas DataFrame and 'body_text' contains the text to translate
def translate_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Translate the following diplomatic text from Turkish to English:"},
                {"role": "user", "content": text}
            ],
            max_tokens=5000,  # Adjust max tokens based on the text size
            temperature=0.3
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Translation failed for text: {text[:50]}... with error: {e}")
        return None

# Function to translate in batches
def batch_translate(df, batch_size=100):
    translated_texts = []
    
    # Divide the dataframe into batches
    for i in range(0, len(df), batch_size):
        batch = df['Body Text'].iloc[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} of {len(df) // batch_size + 1}")
        
        for text in batch:
            translated = translate_text(text)
            translated_texts.append(translated)
            time.sleep(1)  # To avoid hitting API rate limits, adjust the sleep time if needed
        
    # Add the translations back to the DataFrame
    df['translated_text'] = pd.Series(translated_texts)
    
    return df



# Assuming unique_tr is the dataframe containing Turkish press releases
batch_size = 50  # Process 50 press releases per batch
translated_df = batch_translate(unique_tr, batch_size)


# Save the translated dataset
translated_df.to_excel("OUTPU-FILE-PATH", index=False)


