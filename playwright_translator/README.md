# German to Bavarian Translator

A tool for automatically translating German text to Bavarian dialect using web automation. This script uses Playwright to interact with the Respekt Empire translation website and captures screenshots of both input and output pages.

## Features

- Automates translation of German texts to Bavarian dialect
- Captures screenshots of both the German input and Bavarian translation pages
- Saves translations and screenshot references in a CSV file
- Processes multiple sentences in batch
- Error handling with screenshot capture

## Requirements

- Python 3.7+
- Playwright
- Firefox browser

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Amityadav9/Automation.git
   cd playwright_translator
   ```

2. Install required dependencies:
   ```
   pip install playwright
   playwright install
   ```

## Usage

1. Create a file named `german_texts.txt` with your German sentences, one per line:
   ```
   Das Wetter ist heute schön.
   Ich möchte ein Bier bestellen.
   Können Sie mir bitte helfen?
   ```

2. Run the translator:
   ```
   python translator.py
   ```

3. The script will:
   - Process each sentence in the file
   - Take screenshots of the German input page
   - Take screenshots of the resulting Bavarian translation page
   - Save all translations to a CSV file

## Output

The script creates the following outputs:

- `translations.csv`: CSV file containing all translations and screenshot references
- `german_screenshots/`: Folder with screenshots of German input pages
- `bavarian_screenshots/`: Folder with screenshots of Bavarian translation pages

The CSV file contains these columns:
- German text
- Bavarian translation
- German screenshot filename
- Bavarian screenshot filename

## Customization

You can customize the script by modifying these variables in the code:

```python
input_file = "german_texts.txt"  # Your input file with German sentences
output_file = "translations.csv"  # CSV file for saving translations
german_screenshots_folder = "german_screenshots"  # Folder for German screenshots
bavarian_screenshots_folder = "bavarian_screenshots"  # Folder for Bavarian screenshots
```

## How It Works

1. The script reads German sentences from the input file
2. For each sentence:
   - It navigates to the translation website
   - Enters the German text
   - Takes a screenshot of the input page
   - Clicks the translate button
   - Takes a screenshot of the result page
   - Extracts the Bavarian translation text
   - Saves all information to the CSV file

## Limitations

- Depends on the translation website's structure; changes to the website may break functionality
- May encounter timeouts or connectivity issues with slow internet connections
- Translation quality depends on the underlying translation service

## License

[MIT License](LICENSE)

## Acknowledgements

- This tool uses the [Respekt Empire](https://respekt-empire.de/Translator/?page=translateEngine) translation service
- Web automation is powered by [Playwright](https://playwright.dev/)
