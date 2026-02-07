import streamlit as st
import people_also_ask
import pandas as pd
import altair as alt
import utils

@st.cache_data
def get_related_questions_cached(keyword, limit):
    return people_also_ask.get_related_questions(keyword, limit)

st.set_page_config(page_title="Gap Hunter", page_icon="Vx", layout="wide")

st.title("Google Gap Hunter")
st.markdown("### Extract High-Value Questions (PAA) instantly.")

# Sidebar
st.sidebar.header("Settings")
demo_mode = st.sidebar.checkbox("Demo Mode", value=False, help="Use mock data for testing.")

# Equation Display
with st.expander("How we calculate Question Value"):
    st.latex(r'''
        Score = 10 \cdot \log(\text{Word Count} + 1) + 5 \cdot \text{Type Score} + 5 \cdot (1 - |\text{Sentiment}|)
    ''')
    st.caption("We prioritize longer, specific questions with high-intent keywords (How/Why) and neutral/negative sentiment (pain points).")

keyword = st.text_input("Target Keyword", placeholder="e.g. Crypto Trading")
limit = st.slider("Number of Questions", min_value=10, max_value=50, value=20)

if st.button("Start Mining"):
    if keyword:
        try:
            with st.spinner(f"Mining data for: {keyword}..."):
                questions = []
                if demo_mode:
                    questions = utils.mock_questions(keyword, limit)
                else:
                    try:
                        questions = people_also_ask.get_related_questions(keyword, limit)
                    except Exception:
                        st.warning("API Error. Falling back to mock data.")
                        questions = utils.mock_questions(keyword, limit)

                if not questions:
                    st.info("No questions found from API. Showing mock data for demonstration.")
                    questions = utils.mock_questions(keyword, limit)
                
                if questions:
                    # Analysis
                    clusters = utils.cluster_questions(questions)

                    rows = []
                    for idx, q in enumerate(questions):
                        score = utils.calculate_value_score(q)
                        sentiment = utils.analyze_sentiment(q)
                        rows.append({
                            "Question": q,
                            "Value Score": score,
                            "Sentiment": round(sentiment, 2),
                            "Cluster": f"Group {clusters[idx] + 1}"
                        })

                    df = pd.DataFrame(rows)
                    df = df.sort_values(by="Value Score", ascending=False)
                    
                    st.success(f"Found {len(df)} unique questions!")

                    # Metric
                    avg_score = df["Value Score"].mean()
                    col1, col2 = st.columns(2)
                    col1.metric("Average Value Score", f"{avg_score:.2f}")
                    col2.metric("Top Cluster", df["Cluster"].mode()[0])

                    st.dataframe(df, use_container_width=True)
                    
                    # Visualization
                    st.subheader("Visual Analysis")
                    tab1, tab2 = st.tabs(["Value Map", "Cluster Distribution"])

                    with tab1:
                        chart = alt.Chart(df).mark_circle(size=60).encode(
                            x='Sentiment',
                            y='Value Score',
                            color='Cluster',
                            tooltip=['Question', 'Value Score', 'Sentiment', 'Cluster']
                        ).interactive()
                        st.altair_chart(chart, use_container_width=True)

                    with tab2:
                        bar = alt.Chart(df).mark_bar().encode(
                            x='Cluster',
                            y='count()',
                            color='Cluster'
                        )
                        st.altair_chart(bar, use_container_width=True)

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Data (CSV)",
                        data=csv,
                        file_name=f"{keyword.replace(' ', '_')}_gaps.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No PAA questions found. Try a broader keyword.")
                    
        except Exception:
            st.error("An unexpected error occurred. Please try again later.")
    else:
        st.error("Please enter a keyword.")
