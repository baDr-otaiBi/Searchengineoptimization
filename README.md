# Google Gap Hunter 🔍

**Google Gap Hunter** is an advanced SEO tool designed to extract high-value content opportunities from Google's "People Also Ask" (PAA) section. It goes beyond simple extraction by applying smart algorithms to analyze, score, and cluster questions, helping content creators prioritize topics that matter.

## 🚀 Key Features

*   **PAA Mining**: Automatically extracts related questions for any target keyword using `people_also_ask`.
*   **Smart Scoring**: Calculates a "Value Score" for each question to identify high-intent, low-competition opportunities.
*   **Sentiment Analysis**: Detects user sentiment to highlight informational queries (typically neutral) or pain points.
*   **Topic Clustering**: Uses Machine Learning (TF-IDF + K-Means) to group similar questions into thematic clusters.
*   **Visual Analytics**: Interactive charts (Altair) to visualize value distribution and topic spread.
*   **Demo Mode**: Includes a built-in demo mode with mock data for testing without API calls.
*   **CSV Export**: Download your analysis for use in Excel or other SEO tools.

## 🧠 How It Works

The core of Gap Hunter is its **Value Score** algorithm, which prioritizes questions based on three factors:

$$
Score = 10 \cdot \log(\text{Word Count} + 1) + 5 \cdot \text{Type Score} + 5 \cdot (1 - |\text{Sentiment}|)
$$

1.  **Length (Logarithmic)**: Longer questions are often more specific (long-tail) and easier to target.
2.  **Question Type**: We assign higher scores to "How" and "Why" questions (informational/transactional intent) over simple "What" questions.
3.  **Sentiment**: We prioritize neutral questions (informational queries), as high-intent SEO questions often lack strong positive or negative emotion.

## 🛠️ Installation

### Option 1: Using Pip (Standard)

1.  Clone the repository:
    ```bash
    git clone https://github.com/baDr-otaiBi/Searchengineoptimization.git
    cd Searchengineoptimization
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```

### Option 2: Using Conda (Recommended for Isolation)

1.  Create the environment:
    ```bash
    conda env create -f environment.yml
    ```
2.  Activate the environment:
    ```bash
    conda activate base
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```

## 📖 Usage

1.  **Enter a Keyword**: Type a broad topic (e.g., "Crypto Trading", "Vegan Recipes").
2.  **Select Limit**: Choose how many questions to mine (10-50).
3.  **Start Mining**: Click the button. The app will fetch data from Google.
    *   *Note: If the API fails or is blocked, the app automatically falls back to Mock Data (Demo Mode).*
4.  **Analyze**:
    *   **Value Map**: See the scatter plot of Sentiment vs. Value.
    *   **Clusters**: See which topics are most common.
5.  **Download**: Get the full report as a CSV file.

## 📂 Project Structure

*   `app.py`: Main Streamlit application file (UI and Logic flow).
*   `utils.py`: Helper functions for Scoring, Sentiment Analysis, and Clustering.
*   `requirements.txt`: Python dependencies.
*   `environment.yml`: Conda environment configuration.
*   `tests/`: Unit tests for the utility functions.

## 🧪 Testing

Run the test suite to verify the logic:

```bash
pytest tests
```

---
**Note**: This tool relies on the `people_also_ask` library, which scrapes Google. Heavy usage may lead to temporary IP blocks. Use responsibly or enable "Demo Mode" for testing UI features.
