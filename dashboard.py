import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="SQL Quality Analytics", 
    page_icon="📊", 
    layout="wide"
)

st.title("📊 SQL Quality Analytics Dashboard")
st.caption("Enterprise monitoring log tracking query health, common flaws, and organizational performance indexes.")
st.write("---")

if not os.path.exists("reviews.csv"):
    st.info("No data repository found yet. Run an evaluation cycle on the main portal to start tracking history logs.")
else:
    df = pd.read_csv("reviews.csv")
    
    if df.empty:
        st.warning("The performance database log sheet is currently blank.")
    else:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # KPI Metrics Cards centered inside bordered columns
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="Mean Code Quality Index", value=f"{round(df['Score'].mean(), 1)} / 100")
        with m_col2:
            st.metric(label="Total Queries Evaluated", value=f"{len(df)} Run Cycles")
        with m_col3:
            st.metric(label="Average Vulnerabilities Logged", value=f"{round(df['Issue_Count'].mean(), 1)}")
            
        st.write("---")

        # Layout Split for Graphic Analytics panels
        chart_col1, chart_col2 = st.columns(2, gap="medium")
        
        with chart_col1:
            st.subheader("📈 Performance Trajectory Curve")
            fig_trend = px.line(
                df, x="Date", y="Score", markers=True,
                labels={"Score": "Quality Rating", "Date": "Timestamp"},
                template="plotly_white"
            )
            fig_trend.update_layout(yaxis_range=[0, 105])
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with chart_col2:
            st.subheader("🔍 Identified Flaw Distribution")
            fig_dist = px.bar(
                df, x="Date", y="Issue_Count",
                labels={"Issue_Count": "Flaw Volumetrics"},
                template="plotly_white",
                color="Score",
                color_continuous_scale=px.colors.sequential.Bluered_r
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        # Clear structured dataframe history table at base
        st.write("---")
        st.subheader("📋 Centralized Optimization Log Sheet")
        st.dataframe(df, use_container_width=True)