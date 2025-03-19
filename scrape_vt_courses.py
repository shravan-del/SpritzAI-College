import requests
from bs4 import BeautifulSoup
import json
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base URL for VT course catalog
VT_COURSE_CATALOG_URL = "https://catalog.vt.edu/undergraduate/course-descriptions/"

def scrape_vt_courses():
    logging.info("Scraping Virginia Tech course catalog...")

    response = requests.get(VT_COURSE_CATALOG_URL)
    if response.status_code != 200:
        logging.error(f"Failed to fetch VT course subjects: HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    subjects = {}

    # Extract links to each subject page
    for link in soup.find_all("a", href=True):
        if "/undergraduate/course-descriptions/" in link["href"] and link.text.strip():
            subject_name = link.text.strip()
            subject_url = f"https://catalog.vt.edu{link['href']}"
            subjects[subject_name] = subject_url

    logging.info(f"Found {len(subjects)} subjects. Now extracting valid courses...")

    all_courses = []
    for subject, url in subjects.items():
        logging.info(f"Scraping {subject} courses from {url}")
        subject_response = requests.get(url)
        if subject_response.status_code != 200:
            logging.warning(f"Failed to fetch {subject}: HTTP {subject_response.status_code}")
            continue

        subject_soup = BeautifulSoup(subject_response.text, "html.parser")

        # Find valid course names (e.g., "MGT 2000")
        for course in subject_soup.find_all("strong"):
            course_text = course.text.strip()
            if " " in course_text and course_text.split()[1].isdigit():  # Ensure it's in format "XYZ 1234"
                all_courses.append(course_text)

    logging.info(f"✅ Found {len(all_courses)} valid courses.")

    # Save valid courses to JSON
    with open("vt_courses.json", "w") as f:
        json.dump(all_courses, f, indent=4)

    logging.info("✅ VT courses saved to vt_courses.json")
    return all_courses

# Run the function to scrape courses
scrape_vt_courses()