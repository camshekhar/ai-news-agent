import re
from urllib.parse import quote

import feedparser
import requests

from config.settings import ARTICLE_FETCH_TIMEOUT


def clean_text(text):
    """
    Remove HTML tags and normalize whitespace.
    """

    if not text:
        return ""

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def fetch_feed(
    source_name,
    feed_url,
    topic
):
    """
    Fetch articles from one RSS source.
    """

    # Google News requires the topic
    # to be inserted into the URL.
    if "{topic}" in feed_url:

        feed_url = feed_url.format(
            topic=quote(topic)
        )

    try:

        response = requests.get(
            feed_url,
            timeout=ARTICLE_FETCH_TIMEOUT,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "AI-News-Agent/1.0"
            }
        )

        response.raise_for_status()

        feed = feedparser.parse(
            response.content
        )

    except Exception as exc:

        return [], str(exc)


    articles = []

    for entry in feed.entries:

        title = clean_text(
            entry.get(
                "title",
                ""
            )
        )

        url = entry.get(
            "link",
            ""
        )

        summary = clean_text(
            entry.get(
                "summary",
                ""
            )
        )

        published = entry.get(
            "published",
            ""
        )

        if not title or not url:
            continue

        articles.append({

            "title": title,

            "url": url,

            "summary": summary,

            "published": published,

            "source": source_name,

        })

    return articles, None