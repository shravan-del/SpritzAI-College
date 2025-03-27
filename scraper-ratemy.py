import time
import json
import logging
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CHROMEDRIVER_PATH = "/Users/rohan/Downloads/chromedriver-mac-arm64/chromedriver"
RATE_MY_SEARCH_URL = "https://www.ratemyprofessors.com/search/professors/1349?q=*"

def scrape_by_clicking_each_card():
    """Clicks on each professor card, scrapes detail info, then goes back."""
    logging.info("Starting RateMyProfessors scraper...")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Increase the wait time to 30 seconds
    wait = WebDriverWait(driver, 30)

    all_professors = []

    try:
        logging.info(f"Navigating to {RATE_MY_SEARCH_URL}")
        driver.get(RATE_MY_SEARCH_URL)

        # Optionally, scroll down to load lazy-loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load

        # Try an alternative selector if needed. Adjust based on what you see in DevTools.
        try:
            cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='teacher-card']")))
        except Exception as e:
            logging.error("Failed to find cards using div selector, trying li selector.")
            cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-testid='teacher-card']")))
        
        logging.info(f"Found {len(cards)} professor cards on the search page.")

        card_index = 0
        while True:
            # Re-fetch cards on every iteration because the DOM may refresh after going back.
            cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='teacher-card']")
            if card_index >= len(cards):
                break

            logging.info(f"Processing card {card_index+1} of {len(cards)}")
            try:
                card = cards[card_index]
                card.click()

                # Wait for the detail view (e.g., professor name element)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class*='NameTitle__Name']")))

                try:
                    prof_name = driver.find_element(By.CSS_SELECTOR, "h1[class*='NameTitle__Name']").text.strip()
                except Exception:
                    prof_name = "N/A"
                try:
                    department = driver.find_element(By.CSS_SELECTOR, "div[class*='TeacherHeader__Department']").text.strip()
                except Exception:
                    department = "N/A"
                try:
                    quality = driver.find_element(By.CSS_SELECTOR, "div[class*='RatingValue__Numerator']").text.strip()
                except Exception:
                    quality = "N/A"

                all_professors.append({
                    "name": prof_name,
                    "department": department,
                    "quality": quality
                })
                logging.info(f"Scraped professor: {prof_name}")

            except Exception as e:
                logging.error(f"Error processing card {card_index+1}: {e}\n{traceback.format_exc()}")

            # Navigate back to the search page.
            driver.back()
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='teacher-card']")))
            card_index += 1

        with open("rate_my_professors_details_click.json", "w") as f:
            json.dump(all_professors, f, indent=4)
        logging.info("Scraping complete! Data saved to rate_my_professors_details_click.json")

    except Exception as e:
        logging.error(f"General error: {e}\n{traceback.format_exc()}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_by_clicking_each_card()
