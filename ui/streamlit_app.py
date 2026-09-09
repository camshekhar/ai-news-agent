import re
import sys

from pathlib import Path


import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT = Path(
    __file__
).resolve().parents[1]


if str(ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(ROOT)
    )


# ============================================================
# INTERNAL SERVICES
# ============================================================

from config.settings import (
    DEFAULT_ARTICLE_LIMIT,
    DEFAULT_HOURS_BACK
)

from processing.news_gatherer import (
    gather_news
)

from ai.gemini_client import (
    GeminiNewsAnalyzer
)

from output.pdf_generator import (
    generate_pdf
)


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(

    page_title=
        "AI News Research Agent",

    page_icon="📰",

    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "📰 AI News Research Agent"
)

st.caption(
    "Multi-source discovery → "
    "article extraction → "
    "Gemini analysis"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "🔎 Search Configuration"
)


topic = st.sidebar.text_input(

    "News topic",

    placeholder=
        "Artificial Intelligence"
)


hours_back = st.sidebar.selectbox(

    "Time window",

    [
        6,
        12,
        24,
        48,
        72,
        168
    ],

    index=2,

    format_func=lambda x:
        f"Last {x} hours"
)


article_limit = st.sidebar.slider(

    "Articles to collect",

    min_value=5,

    max_value=50,

    value=DEFAULT_ARTICLE_LIMIT
)


# ============================================================
# MAIN BUTTON
# ============================================================

if st.button(

    "🚀 Research Latest News",

    type="primary",

    use_container_width=True
):


    # ========================================================
    # VALIDATE TOPIC
    # ========================================================

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

        st.stop()


    # ========================================================
    # NEWS COLLECTION
    # ========================================================

    with st.status(

        "Collecting and processing news...",

        expanded=True

    ) as status:


        st.write(
            "Searching multiple RSS sources..."
        )


        articles, errors = gather_news(

            topic=topic,

            hours_back=hours_back,

            max_articles=article_limit
        )


        st.write(
            f"Found {len(articles)} "
            "candidate stories."
        )


        if errors:

            st.write(
                f"{len(errors)} "
                "sources had errors."
            )


        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        if not articles:

            status.update(

                label=
                    "No news found",

                state=
                    "error"
            )


            st.error(
                "No recent matching "
                "news was found."
            )


            st.info(
                "Try a broader topic or "
                "increase the time window."
            )


            st.stop()


        # ====================================================
        # GEMINI ANALYSIS
        # ====================================================

        st.write(
            "Sending article content "
            "to Gemini..."
        )


        try:

            analyzer = (
                GeminiNewsAnalyzer()
            )


            report = analyzer.analyze(

                topic,

                articles
            )


        except Exception as exc:

            status.update(

                label=
                    "Gemini failed",

                state=
                    "error"
            )


            st.error(
                f"Gemini error: {exc}"
            )


            st.stop()


        status.update(

            label=
                "News research complete",

            state=
                "complete"
        )


    # ========================================================
    # METRICS
    # ========================================================

    source_count = len(
        set(
            article["source"]
            for article in articles
        )
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Articles",
            len(articles)
        )


    with col2:

        st.metric(
            "Sources",
            source_count
        )


    with col3:

        st.metric(
            "Time Window",
            f"{hours_back}h"
        )


    # ========================================================
    # SOURCE ARTICLES
    # ========================================================

    st.subheader(
        "🌐 Collected Sources"
    )


    for article in articles:

        with st.expander(

            f"{article['title']} — "
            f"{article['source']}"

        ):

            st.write(

                f"**Published:** "
                f"{article['published']}"

            )


            if article.get(
                "content"
            ):

                preview = article[
                    "content"
                ][:1500]


                st.write(
                    preview + "..."
                )


            else:

                st.write(

                    article.get(
                        "summary",
                        "No content available."
                    )

                )


            st.link_button(

                "Read Original Article",

                article["url"]
            )


    # ========================================================
    # AI REPORT
    # ========================================================

    st.divider()


    st.subheader(

        f"🤖 Gemini Analysis — "
        f"{topic}"

    )


    st.markdown(
        report
    )


    # ========================================================
    # DOWNLOAD FILE NAME
    # ========================================================

    safe_name = re.sub(

        r"[^a-zA-Z0-9_-]",

        "_",

        topic
    )


    # ========================================================
    # TXT DOWNLOAD
    # ========================================================

    st.download_button(

        "📄 Download TXT Report",

        data=report,

        file_name=(
            f"{safe_name}_news_report.txt"
        ),

        mime="text/plain"
    )


    # ========================================================
    # PDF
    # ========================================================

    try:

        pdf_bytes = generate_pdf(

            topic,

            report
        )


        st.download_button(

            "📕 Download PDF Report",

            data=pdf_bytes,

            file_name=(
                f"{safe_name}_news_report.pdf"
            ),

            mime="application/pdf"
        )


    except Exception as exc:

        st.warning(

            f"PDF generation failed: "
            f"{exc}"
        )


# ============================================================
# HOME SCREEN
# ============================================================

else:

    st.info(

        "Enter a topic and click "
        "**Research Latest News**."
    )


    st.markdown(
        """
## How it works

### 1. News Discovery

The application checks multiple RSS
sources for recent stories.

### 2. Article Fetching

The original article URL is downloaded.

### 3. Content Extraction

The main article content is extracted
from the webpage.

### 4. Processing

Articles are filtered and duplicate
stories are removed.

### 5. Gemini Analysis

Gemini analyzes the collected article
content and produces a research report.

### 6. Output

The report is displayed in Streamlit
and can be downloaded as TXT or PDF.

---

## Try these topics

- Artificial Intelligence
- OpenAI
- Google Gemini
- Bitcoin
- Indian Stock Market
- Cybersecurity
- SpaceX
- Tesla
- Climate Change
- Quantum Computing
- Cricket
- Football
"""
    )