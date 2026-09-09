import re


def normalize_title(title):
    """
    Normalize a title for basic
    duplicate detection.
    """

    title = title.lower()

    title = re.sub(
        r"[^a-z0-9 ]",
        "",
        title
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title.strip()


def deduplicate(articles):
    """
    Remove articles having the same
    normalized title.
    """

    unique = []

    seen = set()

    for article in articles:

        normalized = normalize_title(
            article.get(
                "title",
                ""
            )
        )

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        unique.append(
            article
        )

    return unique