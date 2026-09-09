import trafilatura


def extract_content(html):
    """
    Extract the main readable article
    content from an HTML page.
    """

    if not html:
        return ""

    try:

        content = trafilatura.extract(
            html,
            include_links=True,
            include_tables=False,
            favor_precision=True
        )

        return content or ""

    except Exception:

        return ""