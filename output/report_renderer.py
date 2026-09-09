def render_article_cards(
    articles
):
    """
    Render raw source articles as
    Markdown suitable for Streamlit.
    """

    output = ""


    for index, article in enumerate(
        articles,
        1
    ):

        output += f"""
### {index}. {article["title"]}

**Source:** {article["source"]}

**Published:** {article["published"]}

{article.get("summary", "")}

🔗 [Read Original Article]({article["url"]})

---
"""


    return output