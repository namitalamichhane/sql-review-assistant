import streamlit as st
import pandas as pd
from datetime import datetime
from sql_analyzer import analyze_query
from scoring import calculate_score
from recommendations import get_recommendations
from ai_explainer import generate_ai_explanation

# Page Configuration for a modern, wide appearance
st.set_page_config(
    page_title="SQL Review Assistant", 
    page_icon="🖥️", 
    layout="wide"
)

# App Title & Subtitle with a clean divider
st.title("🖥️ AI SQL Review Assistant")
st.caption("Maximize performance, identify architectural risks, and eliminate security flaws automatically.")
st.write("---")

# Layout: Split the screen into a left input column and a right output column
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📝 Query Input")
    query = st.text_area(
        "Enter your SQL statement below:",
        height=280,
        placeholder="SELECT * FROM users WHERE status = 'active'..."
    )
    
    # A prominent button with an accent color layout
    analyze_clicked = st.button("Analyze Query Structure", type="primary", use_container_width=True)

with col_output:
    st.subheader("📊 Review Analysis")
    
    if analyze_clicked:
        if query.strip() == "":
            st.error("Please paste a SQL query first to initiate the analysis pipeline.")
        else:
            # Execute backend evaluation pipelines
            issues = analyze_query(query)
            score = calculate_score(issues)
            recs = get_recommendations(issues)
            
            # KPI Score Callout Card
            st.metric(label="Calculated SQL Quality Score", value=f"{score} / 100")
            
            if not issues:
                st.success("Excellent! No obvious anti-patterns, structural risks, or security flaws detected.")
            else:
                # Group findings into clean, interactive tab views
                tab1, tab2, tab3 = st.tabs(["⚠️ Issues & AI Insights", "💡 Recommended Actions", "🔍 Input Syntax Verification"])
                
                with tab1:
                    st.write("The following items require engineering attention:")
                    for issue in issues:
                        st.error(issue)
                        
                        # Interactive dropdown for local AI context explanation
                        with st.expander("View Architectural Reason & Impact"):
                            with st.spinner("Retrieving engineering guidelines..."):
                                ai_insight = generate_ai_explanation(issue)
                                st.write(ai_insight)
                
                with tab2:
                    st.write("Follow these prescriptions to optimize your query layout:")
                    for rec in recs:
                        st.info(rec)
                        
                with tab3:
                    st.write("Parsed structural formatting:")
                    # Beautifully formats and highlights the SQL text automatically
                    st.code(query, language="sql")
            
            # --- PERSISTENT LOGGING ---
            new_data = {
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Score": [score],
                "Issue_Count": [len(issues)],
                "Query_Length": [len(query)]
            }
            new_df = pd.DataFrame(new_data)
            try:
                new_df.to_csv("reviews.csv", mode="a", index=False, header=not pd.io.common.file_exists("reviews.csv"))
            except Exception as e:
                st.sidebar.error(f"History tracking error: {e}")
    else:
        # State showing when the user hasn't clicked anything yet
        st.info("Input a SQL query statement on the left panel and click analyze to populate the optimization review metrics.")