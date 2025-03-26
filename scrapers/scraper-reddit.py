import praw
import requests
from bs4 import BeautifulSoup
import pandas as pd

# === Replace with your Reddit API credentials ===
reddit = praw.Reddit(
    client_id="kT_kKOaK9fWNIrhlOBr8Eg",
    client_secret="CiKZsVFePlQH3uNugggZvpUwYuvaGQ",
    user_agent="SpritzAI_scraper:v1.0 (by /u/VermicelliLazy9181)"
)

# Subreddit and keywords to search
subreddit = reddit.subreddit("VirginiaTech")
keywords = [
    "hardest classes", "CS courses", "ENGR 1215", "easy electives", 
    "professors to avoid", "professors to choose", "Calculus", "World Regions",
    "Geography of Wine", "COMM 1014", "math department", "GPA boosters"
]

# Function to fetch and scrape post data
def scrape_reddit():
    post_data = []
    for keyword in keywords:
        print(f"Searching for: {keyword}...")
        for submission in subreddit.search(keyword, limit=10):  # Adjust limit as needed
            submission.comments.replace_more(limit=5)  # Expands top comments
            comments = [comment.body for comment in submission.comments[:10]]  # Extract top 10 comments
            post_data.append({
                "Title": submission.title,
                "Upvotes": submission.score,
                "URL": submission.url,
                "Comments": comments
            })
    
    # Convert data to DataFrame
    df = pd.DataFrame(post_data)
    return df

# Scrape the data
df_reddit = scrape_reddit()

# Save to CSV for further processing
df_reddit.to_csv("VirginiaTech_Reddit_Classes.csv", index=False)
print("Scraped data saved to VirginiaTech_Reddit_Classes.csv!")

# === Scraping Easy Electives Page (from Reddit thread) ===
def scrape_easy_electives():
    url = "https://www.reddit.com/r/VirginiaTech/comments/y6szzn/easy_classes_list_80_classes/"  # Thread URL
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all("div", class_="md")  # Extracting markdown content

        electives = []
        for comment in comments:
            text = comment.get_text()
            if "GPA" in text or "easy class" in text:  # Filtering relevant info
                electives.append(text)

        df_electives = pd.DataFrame({"Elective_Classes": electives})
        df_electives.to_csv("VirginiaTech_Easy_Electives.csv", index=False)
        print("Easy electives scraped and saved!")
    else:
        print("Failed to fetch easy electives!")

scrape_easy_electives()