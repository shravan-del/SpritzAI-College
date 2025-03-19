from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Chromedriver Path
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

# Anaanu Base URL
BASE_ANAANU_COURSE_URL = "https://anaanu.com/s/virginia-tech-vt/course/{}"

# Load only valid courses from file
with open("vt_courses.json", "r") as f:
    COURSES = json.load(f)

def scrape_anaanu_course(course):
    logging.info(f"Scraping Anaanu for {course}...")

    formatted_course = course.replace(" ", "%2B")  # Format for Anaanu
    course_url = BASE_ANAANU_COURSE_URL.format(formatted_course)

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Start Selenium
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(course_url)
        wait = WebDriverWait(driver, 10)

        # Click 'Instructors' tab
        try:
            instructor_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Instructors')]")))
            driver.execute_script("arguments[0].click();", instructor_tab)
            logging.info("Clicked 'Instructors' tab")
            time.sleep(2)
        except Exception as e:
            logging.warning(f"Failed to click 'Instructors' tab for {course}: {e}")
            return None

        # Parse professor data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        professors = []
        for row in soup.select("tr"):
            cols = row.find_all("td")
            if len(cols) > 5:
                name = cols[0].text.strip()
                classes_taught = cols[1].text.strip()
                a_percent = cols[2].text.strip()
                gpa = cols[-1].text.strip()

                professors.append({
                    "course": course,
                    "name": name,
                    "classes_taught": classes_taught,
                    "A_grade_percentage": a_percent,
                    "GPA": gpa
                })

        if professors:
            logging.info(f"✅ Found {len(professors)} professors for {course}")
            return professors
        else:
            logging.warning(f"⚠️ No professor data found for {course}")
            return None

    except Exception as e:
        logging.error(f"Error while scraping {course}: {e}")
        return None
    finally:
        driver.quit()

# Process only valid courses
all_professors_data = []

for i, course in enumerate(COURSES):
    logging.info(f"📌 Processing course {i+1}/{len(COURSES)}: {course}")

    course_data = scrape_anaanu_course(course)
    if course_data:
        all_professors_data.extend(course_data)

    # Short pause to avoid rate limits
    time.sleep(1)

# Save to JSON
with open("anaanu_data.json", "w") as f:
    json.dump(all_professors_data, f, indent=4)

logging.info("✅ All professor data saved to anaanu_data.json")