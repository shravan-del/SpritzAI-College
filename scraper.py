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

# logging aspect
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# how we are accessing the chromedriver
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

# this is the website we are trying to scrape
BASE_COURSE_URL = "https://anaanu.com/s/virginia-tech-vt/course/{}"

# courses
COURSES = ["DASC%2B1574", "STAT%2B3005", "CHEM%2B1035", "CS%2B3114", "STAT%2B4705"]  

def scrape_anaanu():
    logging.info("Starting Anaanu scraper...")

    # chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # selenium web driver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_professors = []

    try:
        for course in COURSES:
            course_url = BASE_COURSE_URL.format(course)
            logging.info(f"🌐 Navigating to {course_url}")
            driver.get(course_url)

            wait = WebDriverWait(driver, 10)

            # this clicks instructors
            try:
                instructor_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Instructors')]")))
                driver.execute_script("arguments[0].click();", instructor_tab)
                logging.info("Clicked 'Instructors' tab")
                time.sleep(3)  # Wait for instructor data to load
            except Exception as e:
                logging.warning(f"Failed to click 'Instructors' tab: {e}")
                continue  # Skip to the next course

            # scrape the professor data
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

            # save that extracted data
            if professors:
                all_professors.extend(professors)
                logging.info(f"Found {len(professors)} professors for {course}")
            else:
                logging.warning(f"No professor data found for {course}")

            # pause for next search
            time.sleep(2)

        # save all that data
        with open("anaanu_data.json", "w") as f:
            json.dump(all_professors, f, indent=4)
        logging.info("All course data successfully saved to anaanu_data.json")

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        driver.quit() 

scrape_anaanu()