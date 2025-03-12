import praw
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

REDDIT_CLIENT_ID = "kT_kKOaK9fWNIrhlOBr8Eg"
REDDIT_CLIENT_SECRET = "CiKZsVFePlQH3uNugggZvpUwYuvaGQ"
REDDIT_USER_AGENT = "SpritzAI-Scraper"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

SEARCH_TERMS = [
    "DASC 1574 Virginia Tech",
    "STAT 3005 Virginia Tech",
    "Professor Knowlton Virginia Tech",
]

reddit_data = []

def scrape_reddit():
    logging.info("Starting Reddit Scraper...")

    for term in SEARCH_TERMS:
        logging.info(f"🔍 Searching Reddit for: {term}")

        try:
            posts = reddit.subreddit("all").search(term, limit=10)  # Fetch top 10 posts

            for post in posts:
                post_data = {
                    "title": post.title,
                    "url": post.url,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "text": post.selftext,
                    "comments": []
                }

                post.comments.replace_more(limit=2)  
                for comment in post.comments.list()[:5]:  
                    post_data["comments"].append({
                        "author": str(comment.author),
                        "score": comment.score,
                        "text": comment.body
                    })

                reddit_data.append(post_data)

            logging.info(f"Extracted {len(reddit_data)} posts for {term}")

            time.sleep(2)  # Prevent API rate limits

        except Exception as e:
            logging.error(f"Error fetching {term}: {e}")

    with open("reddit_data.json", "w") as f:
        json.dump(reddit_data, f, indent=4)
    logging.info("Reddit data successfully saved to reddit_data.json")

scrape_reddit()