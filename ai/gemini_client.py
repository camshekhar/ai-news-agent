import time

from google import genai

from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


class GeminiNewsAnalyzer:
    """
    Gemini service responsible for
    analyzing collected news articles.
    """

    def __init__(self):

        if not GEMINI_API_KEY:

            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )


    def analyze(
        self,
        topic,
        articles
    ):
        """
        Send collected article content
        to Gemini and generate a news report.
        """

        context = ""


        # ====================================================
        # BUILD AI CONTEXT
        # ====================================================

        for index, article in enumerate(
            articles,
            1
        ):

            content = (
                article.get(
                    "content"
                )
                or article.get(
                    "summary"
                )
                or ""
            )


            # Prevent extremely large articles
            # from consuming the complete context.
            content = content[:12000]


            context += f"""
ARTICLE {index}

Title:
{article.get("title", "")}

Source:
{article.get("source", "")}

Published:
{article.get("published", "")}

URL:
{article.get("url", "")}

Article Content:
{content}

==================================================
"""


        # ====================================================
        # PROMPT
        # ====================================================

        prompt = f"""
You are a professional senior news editor.

The requested topic is:

{topic}

The application collected recent articles
from multiple news publishers.

Your job is to analyze ONLY the supplied
article material.

IMPORTANT RULES:

1. Do NOT invent facts.
2. Do NOT invent news stories.
3. Do NOT invent URLs.
4. Do NOT use your pretrained knowledge
   to create additional current events.
5. Only make claims supported by the
   supplied article content.
6. Group articles reporting the same
   underlying event.
7. Identify important developments.
8. Compare coverage across sources.
9. Preserve original URLs.
10. Clearly identify source names.

Create a professional news research report.

Return this structure:

# Latest News: {topic}

## Top Stories

For every important unique story:

### [Headline]

**Sources:** ...

**Published:** ...

**Summary:**

Write a concise but informative summary.

**Key Takeaways:**

- ...
- ...
- ...

**Original Sources:**

- URL

---

# Overall Summary

Explain the current situation surrounding
{topic} based ONLY on the supplied articles.

# Major Trends

- ...
- ...
- ...

# Cross-Source Analysis

Explain whether multiple publishers are
reporting the same major events.

Mention important differences in coverage
when they exist.

SOURCE MATERIAL:

{context}
"""


        # ====================================================
        # GEMINI REQUEST WITH RETRY
        # ====================================================

        for attempt in range(4):

            try:

                response = (
                    self.client
                    .models
                    .generate_content(

                        model=GEMINI_MODEL,

                        contents=prompt,

                        config=(
                            types
                            .GenerateContentConfig(
                                temperature=0.1,
                                max_output_tokens=7000
                            )
                        )
                    )
                )


                return response.text


            except Exception as exc:

                message = str(
                    exc
                ).lower()


                # --------------------------------------------
                # RATE LIMIT
                # --------------------------------------------

                if (
                    "429" in message
                    or
                    "resource_exhausted"
                    in message
                ):

                    if attempt < 3:

                        wait = 2 ** attempt

                        time.sleep(
                            wait
                        )

                        continue


                raise


        return None