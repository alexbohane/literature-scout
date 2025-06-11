import streamlit as st
from graph_flow import run_literature_flow
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import io

# Set page config
st.set_page_config(page_title="🧬 Literature Scout", layout="wide")

# Inject CSS from styles.css
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject Google Font Lato
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Lato', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title and Description
st.title("🧬 Literature Scout")
st.markdown(
    """
    An **intelligent agentic system** to automatically **scout, summarise**, and **present** the latest scientific literature.

    _Literature Scout takes the top **1000 papers** from Europe PMC based on your query, sorted by **number of citations**._
    """
)
st.markdown("---")

# Compact input box + button side by side
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input("🔍 Enter a gene, disease, or pathway to scout the literature:")

with col2:
    st.markdown("")  # Add space for alignmen
    run_clicked = st.button("🚀 Run Literature Scout", use_container_width=True)

# If button clicked
if run_clicked and query:
    with st.spinner(f"🔍 Searching literature for '**{query}**'..."):
        state = run_literature_flow(query)

    st.success("✅ Literature Scout completed!")

    # Add space and separator
    st.markdown("##")
    st.markdown("---")

    # Two columns for report and chart
    col1, col2 = st.columns([3, 2])

    # Left column: Report
    with col1:
        st.header("📄 Literature Report")
        st.markdown(state["report_markdown"], unsafe_allow_html=True)

        # Download Report
        md_content = state["report_markdown"]
        md_bytes = md_content.encode("utf-8")
        md_buffer = io.BytesIO(md_bytes)

        st.download_button(
            label="⬇️ Download Report as Markdown",
            data=md_buffer,
            file_name=f"{query.replace(' ', '_')}_literature_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Right column: Chart
    with col2:
        st.header("📈 Publication Trends")
        st.caption("Number of papers published per year based on your search results:")

        # Process years
        years = [int(paper["year"]) for paper in state["search_results"] if paper.get("year")]
        df_years = pd.DataFrame(years, columns=["year"])

        if not df_years.empty:
            chart = (
                alt.Chart(df_years)
                .mark_bar(color="#4e79a7")
                .encode(
                    x=alt.X("year:O", title="Year"),
                    y=alt.Y("count()", title="Number of Papers"),
                    tooltip=["year", "count()"]
                )
                .properties(width=400, height=300)
                .interactive()
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("⚠️ No publication year data available for chart.")

# Footer / Instructions
st.markdown("---")
st.caption("Built by Alex Bohane - Owkin Technical Assessment 2025")
