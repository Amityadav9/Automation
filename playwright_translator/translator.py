from playwright.sync_api import sync_playwright
import time
import csv
import os
import re


def translate_german_to_bavarian(
    input_file, output_file, german_screenshots_folder, bavarian_screenshots_folder
):
    """
    Translate German texts to Bavarian and take screenshots of both the input and output pages.
    """
    # Create folders if they don't exist
    os.makedirs(german_screenshots_folder, exist_ok=True)
    os.makedirs(bavarian_screenshots_folder, exist_ok=True)

    # Load German texts from input file
    with open(input_file, "r", encoding="utf-8") as f:
        german_texts = [line.strip() for line in f if line.strip()]

    # Setup CSV file - ALWAYS create new to avoid appending issues
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["German", "Bavarian", "German Screenshot", "Bavarian Screenshot"]
        )

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        for i, german_text in enumerate(german_texts):
            print(f"Processing ({i + 1}/{len(german_texts)}): {german_text}")

            try:
                # Navigate to website
                page.goto("https://respekt-empire.de/Translator/?page=translateEngine")
                time.sleep(2)  # Wait for page to stabilize

                # Enter German text
                text_area = page.locator("textarea")
                text_area.fill(german_text)

                # Take screenshot of German input page
                german_screenshot_path = os.path.join(
                    german_screenshots_folder, f"german_page_{i + 1}.png"
                )
                page.screenshot(path=german_screenshot_path)
                print(f"Saved German input page screenshot: {german_screenshot_path}")

                # Click the translate button
                page.click("input[value='Übersetzen']")

                # Wait for the result page to load
                time.sleep(5)

                # Take screenshot of Bavarian translation page
                bavarian_screenshot_path = os.path.join(
                    bavarian_screenshots_folder, f"bavarian_page_{i + 1}.png"
                )
                page.screenshot(path=bavarian_screenshot_path)
                print(
                    f"Saved Bavarian translation page screenshot: {bavarian_screenshot_path}"
                )

                # Extract translation for the CSV file
                bavarian_text = page.evaluate("""() => {
                    // Find all divs with dotted borders which might contain our translation
                    const possibleContainers = Array.from(document.querySelectorAll('div[style*="border"]'));
                    // Look for the one that contains text but not the German input
                    for (const container of possibleContainers) {
                        const text = container.innerText.trim();
                        if (text && text !== document.querySelector('textarea')?.value) {
                            return text;
                        }
                    }
                    // Fallback: look for any non-empty container after translation
                    const allContainers = Array.from(document.querySelectorAll('div'));
                    for (const container of allContainers) {
                        const text = container.innerText.trim();
                        if (text && 
                            text !== document.querySelector('textarea')?.value && 
                            !text.includes('Übersetzen') && 
                            !text.includes('Zurück') &&
                            text.length > 5) {
                            return text;
                        }
                    }
                    return null;
                }""")

                if not bavarian_text:
                    # If JavaScript approach fails, try a simpler approach
                    body_text = page.inner_text("body")

                    # Look for the back button which appears after translation
                    if "Zurück" in body_text:
                        # Split by lines and look for content that isn't the German text
                        lines = [
                            line.strip()
                            for line in body_text.split("\n")
                            if line.strip()
                        ]
                        for line in lines:
                            if (
                                line != german_text
                                and "Übersetzen" not in line
                                and "Zurück" not in line
                                and "Datenschutzerklärung" not in line
                                and "Neues" not in line
                                and "Apps" not in line
                                and "Literatur" not in line
                                and "Funktionsweise" not in line
                                and "Impressum" not in line
                                and "Besucher:" not in line
                                and len(line) > 5
                            ):
                                bavarian_text = line
                                break

                # Clean up the bavarian text to fix formatting issues
                if bavarian_text:
                    # Remove "Datenschutzerklärung" if present
                    bavarian_text = bavarian_text.replace(
                        "Datenschutzerklärung", ""
                    ).strip()
                    # Fix newline issues
                    bavarian_text = re.sub(r"\s+", " ", bavarian_text).strip()
                else:
                    bavarian_text = "TRANSLATION_NOT_FOUND"

                print(f"Bavarian translation: {bavarian_text}")

                # Save to CSV
                with open(output_file, "a", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            german_text,
                            bavarian_text,
                            f"german_page_{i + 1}.png",
                            f"bavarian_page_{i + 1}.png",
                        ]
                    )

                # Add a delay between requests
                time.sleep(3)

            except Exception as e:
                print(f"Error processing: {e}")
                with open(output_file, "a", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            german_text,
                            f"ERROR: {str(e)[:100]}",
                            f"german_page_{i + 1}.png"
                            if os.path.exists(
                                os.path.join(
                                    german_screenshots_folder,
                                    f"german_page_{i + 1}.png",
                                )
                            )
                            else "",
                            "",
                        ]
                    )

                # Take error screenshot
                try:
                    page.screenshot(
                        path=os.path.join(
                            bavarian_screenshots_folder, f"error_{i + 1}.png"
                        )
                    )
                except:
                    pass

        browser.close()
        print(f"All translations saved to {output_file}")
        print(f"German page screenshots saved to {german_screenshots_folder}")
        print(f"Bavarian page screenshots saved to {bavarian_screenshots_folder}")


if __name__ == "__main__":
    input_file = "german_texts.txt"
    output_file = "translations.csv"
    german_screenshots_folder = "german_screenshots"
    bavarian_screenshots_folder = "bavarian_screenshots"

    if not os.path.exists(input_file):
        # Create example file if it doesn't exist, not necessary
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("Das Wetter ist heute schön.\n")
            f.write("Ich möchte ein Bier bestellen.\n")
        print(f"Created example file {input_file} with sample sentences")

    translate_german_to_bavarian(
        input_file, output_file, german_screenshots_folder, bavarian_screenshots_folder
    )
