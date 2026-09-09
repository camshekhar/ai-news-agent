import requests

from config.settings import ARTICLE_FETCH_TIMEOUT


def fetch_article(url):
    """
    Download the original article webpage.
    """

    try:

        response = requests.get(
            url,
            timeout=ARTICLE_FETCH_TIMEOUT,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "AI-News-Agent/1.0"
            }
        )

        response.raise_for_status()

        return response.text, None

    except Exception as exc:

        return None, str(exc)