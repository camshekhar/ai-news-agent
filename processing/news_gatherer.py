from datetime import (
    datetime,
    timezone
)

from email.utils import (
    parsedate_to_datetime
)


from config.settings import (
    RSS_SOURCES
)

from news.rss_fetcher import (
    fetch_feed
)

from news.article_fetcher import (
    fetch_article
)

from news.content_extractor import (
    extract_content
)

from processing.article_filter import (
    topic_matches,
    within_time_window
)

from processing.deduplicator import (
    deduplicate
)


def parse_date(value):
    """
    Convert RSS publication date into
    a timezone-aware datetime.
    """

    if not value:
        return None

    try:

        return parsedate_to_datetime(
            value
        ).astimezone(
            timezone.utc
        )

    except Exception:

        return None


def gather_news(
    topic,
    hours_back=24,
    max_articles=25
):
    """
    Complete news gathering pipeline.

    1. Search RSS sources
    2. Filter by topic
    3. Filter by time
    4. Deduplicate
    5. Download article pages
    6. Extract article content
    """

    all_articles = []

    errors = []


    # ========================================================
    # STEP 1
    # RSS DISCOVERY
    # ========================================================

    for (
        source_name,
        feed_url
    ) in RSS_SOURCES.items():

        articles, error = fetch_feed(
            source_name,
            feed_url,
            topic
        )

        if error:

            errors.append(
                f"{source_name}: {error}"
            )


        for article in articles:

            article[
                "published_dt"
            ] = parse_date(
                article.get(
                    "published"
                )
            )


            # -----------------------------------------------
            # TOPIC FILTER
            # -----------------------------------------------

            if not topic_matches(
                article,
                topic
            ):
                continue


            # -----------------------------------------------
            # TIME FILTER
            # -----------------------------------------------

            if not within_time_window(
                article,
                hours_back
            ):
                continue


            all_articles.append(
                article
            )


    # ========================================================
    # STEP 2
    # DEDUPLICATION
    # ========================================================

    all_articles = deduplicate(
        all_articles
    )


    # ========================================================
    # STEP 3
    # SORT NEWEST FIRST
    # ========================================================

    all_articles.sort(

        key=lambda article:

            article.get(
                "published_dt"
            )

            or datetime.min.replace(
                tzinfo=timezone.utc
            ),

        reverse=True
    )


    # ========================================================
    # STEP 4
    # SELECT ARTICLES
    # ========================================================

    selected = all_articles[
        :max_articles
    ]


    # ========================================================
    # STEP 5
    # FETCH ORIGINAL ARTICLE
    # ========================================================

    for article in selected:

        html, error = fetch_article(
            article["url"]
        )


        if error:

            article[
                "fetch_error"
            ] = error

            article[
                "content"
            ] = ""

            continue


        # ====================================================
        # STEP 6
        # EXTRACT ARTICLE CONTENT
        # ====================================================

        article[
            "content"
        ] = extract_content(
            html
        )


    return selected, errors