Overview

This project implements a real-time sentiment analysis and alert system. It leverages web scraping, natural language processing (NLP), and a real-time alert mechanism to monitor public sentiment from various online sources. The system extracts data, analyzes sentiment using VADER and BERT, detects anomalies using Hidden Markov Models (HMM), and sends real-time alerts via Server-Sent Events (SSE).

## Features

-   **Web Scraping:** Extracts real-time data from news websites, social media, and blogs using Beautiful Soup.
-   **Sentiment Analysis:**
    -   Lexicon-based analysis using VADER for quick sentiment classification.
    -   Deep learning-based analysis using BERT for context-aware sentiment classification.
-   **Anomaly Detection:** Uses Hidden Markov Models (HMM) to detect sudden shifts in sentiment patterns.
-   **Real-Time Alerts:** Sends instant alerts via Server-Sent Events (SSE) when anomalies are detected.
-   **Data Storage:** Stores structured data in PostgreSQL for efficient retrieval and analysis.
-   **Interactive Dashboard:** Provides a user-friendly interface to visualize real-time sentiment trends and anomaly alerts using React.js.
