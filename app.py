import streamlit as st
import people_also_ask
import pandas as pd

st.set_page_config(page_title="Gap Hunter", page_icon="Vx")

st.title("Google Gap Hunter")
st.markdown("### Extract High-Value Questions (PAA) instantly.")

keyword = st.text_input("Target Keyword", placeholder="e.g. Crypto Trading")
limit = st.slider("Number of Questions", min_value=10, max_value=50, value=20)

if st.button("Start Mining"):
    if keyword:
        try:
            with st.spinner(f"Mining data for: {keyword}..."):
                questions = people_also_ask.get_related_questions(keyword, limit)
                
                if questions:
                    df = pd.DataFrame(questions, columns=["Content Gaps"])
                    
                    st.success(f"Found {len(df)} unique questions!")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Data (CSV)",
                        data=csv,
                        file_name=f"{keyword.replace(' ', '_')}_gaps.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No PAA questions found. Try a broader keyword.")
                    
        except Exception as e:
            st.error(f"Connection Error: {e}")
    else:
        st.error("Please enter a keyword.")
      
