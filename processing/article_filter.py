import re

from datetime import (
    datetime,
    timedelta,
    timezone
)


def topic_matches(
    article,
    topic
):
    """
    Check whether an article appears
    relevant to the requested topic.
    """

    words = [
        word.lower()
        for word in re.findall(
            r"\w+",
            topic
        )
        if len(word) > 2
    ]

    if not words:
        return True

    text = (
        article.get(
            "title",
            ""
        )
        + " "
        + article.get(
            "summary",
            ""
        )
    ).lower()

    return any(
        word in text
        for word in words
    )


def within_time_window(
    article,
    hours_back
):
    """
    Determine whether an article was
    published within the requested window.
    """

    published = article.get(
        "published_dt"
    )

    if not published:
        return True

    cutoff = (
        datetime.now(timezone.utc)
        - timedelta(
            hours=hours_back
        )
    )

    return published >= cutoff