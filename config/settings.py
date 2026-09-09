import os

from dotenv import load_dotenv


load_dotenv()


# ============================================================
# GEMINI
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite"
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

DEFAULT_ARTICLE_LIMIT = int(
    os.getenv(
        "DEFAULT_ARTICLE_LIMIT",
        "3"
    )
)

DEFAULT_HOURS_BACK = int(
    os.getenv(
        "DEFAULT_HOURS_BACK",
        "24"
    )
)

ARTICLE_FETCH_TIMEOUT = int(
    os.getenv(
        "ARTICLE_FETCH_TIMEOUT",
        "15"
    )
)


# ============================================================
# NEWS SOURCES
# ============================================================

RSS_SOURCES = {

    "Google News India":
        "https://news.google.com/rss/search?"
        "q={topic}+India&hl=en-IN&gl=IN&ceid=IN:en",

    "Indian Express":
        "https://indianexpress.com/feed/",


    "Times of India":
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",

    
    "Hindustan Times":
        "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",


    "Business Standard":
        "https://www.business-standard.com/rss/latest.rss",

    "Economic Times":
        "https://economictimes.indiatimes.com/rssfeedsdefault.cms",

    "Mint":
        "https://www.livemint.com/rss/news",

    "Google News":
        "https://news.google.com/rss/search?"
        "q={topic}&hl=en-US&gl=US&ceid=US:en",

    "BBC":
        "https://feeds.bbci.co.uk/news/rss.xml",

    "NPR":
        "https://feeds.npr.org/1001/rss.xml",

    "Guardian":
        "https://www.theguardian.com/world/rss",

    "Al Jazeera":
        "https://www.aljazeera.com/xml/rss/all.xml",

    "CNBC":
        "https://www.cnbc.com/id/100003114/"
        "device/rss/rss.html",

}