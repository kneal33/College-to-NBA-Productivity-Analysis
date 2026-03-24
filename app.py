import streamlit as st
import pandas as pd
import altair as alt

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="NBA College Analyzer",
    layout="wide"
)

# -----------------------
# Title
# -----------------------
st.title("🏀 NBA College Production Dashboard")
st.markdown("Which colleges produce the best NBA players?")

# -----------------------
# Load data
# -----------------------
df = pd.read_csv("college_overall_scores.csv")

# -----------------------
# Top controls (NOT sidebar)
# -----------------------
col1, col2 = st.columns([1, 1])

with col1:
    top_n = st.slider("Top N Colleges", 5, 25, 10)

with col2:
    metric = st.selectbox(
        "Select Metric",
        ["DEF_IMPACT", "TS_PCT", "EFG_PCT", "AST_TOV", "REB"]
    )

# -----------------------
# Rankings
# -----------------------
top_colleges = df.sort_values("OVERALL_SCORE", ascending=False).head(top_n)

# -----------------------
# KPI Cards
# -----------------------
col1, col2, col3 = st.columns(3)

col1.metric("🏆 Top College", top_colleges.iloc[0]["college"])
col2.metric("Best Score", round(top_colleges.iloc[0]["OVERALL_SCORE"], 3))
col3.metric("Total Colleges", len(df))

st.markdown("---")

# -----------------------
# Overall Chart (SIMPLER)
# -----------------------
st.subheader("🏆 Best Colleges Overall")

chart = alt.Chart(top_colleges).mark_bar(color="#4C78A8").encode(
    x=alt.X("OVERALL_SCORE", title="Overall Score"),
    y=alt.Y("college", sort="-x", title="")
)

st.altair_chart(chart, use_container_width=True)

# -----------------------
# Metric Chart (SIMPLER)
# -----------------------
st.subheader(f"📊 Top Colleges by {metric}")

metric_rank = df.sort_values(metric, ascending=False).head(top_n)

metric_chart = alt.Chart(metric_rank).mark_bar(color="#54A24B").encode(
    x=alt.X(metric, title=metric),
    y=alt.Y("college", sort="-x", title="")
)

st.altair_chart(metric_chart, use_container_width=True)

# -----------------------
# Optional table (collapsed)
# -----------------------
with st.expander("See Data Table"):
    st.dataframe(top_colleges, use_container_width=True)

# -----------------------
# Footer
# -----------------------
st.caption("Metrics are normalized and aggregated at the college level.")