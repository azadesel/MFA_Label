
# Press Release Emotion and Event Analyzer

This Python script utilizes the OpenAI API to analyze press releases from the Turkish Ministry of Foreign Affairs, extracting key information such as the main event category, actor, emotion, and relevant keywords/phrases. The script processes press releases in batches, making it efficient for large datasets, and saves the structured analysis to an Excel file.

## Features

* **Emotion Detection**: Identifies emotions (Happiness, Sadness, Fear, Sympathy, Frustration, Hope, Anger, None) conveyed in press releases.
* **Event Categorization**: Assigns a main event category to each press release.
* **Actor Identification**: Extracts the primary actor involved in the event described.
* **Keyword Extraction**: Identifies up to five key words or phrases relevant to the press release content.
* **Batch Processing**: Efficiently processes large datasets by sending press releases to the OpenAI API in batches.
* **Rate Limit Handling**: Includes a `time.sleep` mechanism to prevent hitting OpenAI API rate limits.
* **Periodic Saving**: Saves processed data periodically to an Excel file to prevent data loss.

## Requirements

Before running the script, ensure you have the following installed:

* Python 3.x
* `pandas` library
* `openai` library

You can install these libraries using pip:

```bash
pip install pandas openai
```

## Setup

1.  **OpenAI API Key**:
    Obtain an API key from OpenAI. Replace `"YOUR-API-KEY"` in the script with your actual API key:

    ```python
    openai.api_key = "YOUR-API-KEY"
    ```

2.  **Input Excel File**:
    Prepare an Excel file containing the press releases. The script expects a column named `'Body Text'` which contains the actual text of the press releases.

    Update the `input_file` variable with the path to your Excel file:

    ```python
    input_file = "/Users/azadesel/Desktop/mfa_archive/mfa_2025_clean_woanalysis.xlsx"
    ```

3.  **Output Excel File**:
    Specify the desired path and filename for the output Excel file where the analyzed data will be saved:

    ```python
    output_file = "/Users/azadesel/Desktop/mfa_archive/mfa_en/processed_press_releases_2025.xlsx"
    ```

## Usage

1.  **Configure Paths and API Key**: As described in the Setup section, update the `openai.api_key`, `input_file`, and `output_file` variables in the script.

2.  **Run the Script**: Execute the Python script from your terminal:

    ```bash
    python your_script_name.py
    ```

    (Replace `your_script_name.py` with the actual name of your Python file.)

The script will read the press releases from the input Excel file, process them in batches using the OpenAI API, and write the structured analysis (Main Event Category, Actor, Emotion, Key Words/Phrases) into a new column named `'Analysis'` in the specified output Excel file.

Progress updates and periodic save notifications will be printed to the console.

## Customization

* **`model`**: The script uses `gpt-4o-mini-2024-07-18`. You can change this to another OpenAI chat completion model if needed.
* **`max_tokens`**: Adjust the `max_tokens` parameter in the `openai.ChatCompletion.create` call to control the length of the generated analysis.
* **`temperature`**: Modify the `temperature` parameter (default is 0.3) to control the creativity and randomness of the AI's output. Lower values make the output more deterministic.
* **`batch_size`**: The `batch_size` variable determines how many press releases are sent to the API in one go. Adjust this based on your system's memory and API rate limits.
* **`time.sleep()`**: The `time.sleep(5)` call introduces a 5-second delay between batches to avoid hitting API rate limits. You may need to adjust this value based on your OpenAI plan and usage.
* **Prompt Engineering**: The `prompt` variable contains detailed instructions for the OpenAI model. You can fine-tune this prompt to get more specific or different types of analysis.

## Output Structure

The output Excel file will be the same as your input file, but with an additional column named `'Analysis'`. Each cell in this column will contain the structured output from the OpenAI API for the corresponding press release, formatted as follows:

```
Main Event Category: [Event Category]
Actor: [Actor]
Emotion: [Emotion]
Key Words/Phrases: [Keyword 1, Keyword 2, Keyword 3, Keyword 4, Keyword 5]
```
