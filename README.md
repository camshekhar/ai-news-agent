# 📰 AI News Research Agent

A modular AI-powered news research application that discovers
recent news from multiple sources, retrieves the original articles,
extracts their content, and uses Gemini to produce a consolidated
research report.

---

# Architecture

The project follows a modular / microservice-ready architecture:

```text
                    ┌─────────────────┐
                    │  Streamlit UI   │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   News Gatherer     │
                  └──────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        Google News         BBC            CNBC
             RSS             RSS            RSS
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    Article Fetcher
                             │
                             ▼
                   Content Extractor
                             │
                             ▼
                      Deduplicator
                             │
                             ▼
                     Topic Filter
                             │
                             ▼
                  Gemini AI Analyzer
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
             Streamlit Report       PDF Report