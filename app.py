import streamlit as st
from graph_flow import run_literature_flow
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import io

# Set page config
st.set_page_config(page_title="Literature Scout", layout="wide")



st.title("🧬 Literature Scout")
st.header("An intelligent agentic system to automatically scout, summarise, and present the latest scientific literature.")
st.markdown("**Literature Scout takes the top 1000 papers from Europe PMC based on your query sorted by number of descending number of citations**")
st.markdown("---")

# User input
query = st.text_input("Enter a gene, disease, or pathway:")

if st.button("Run Literature Scout") and query:
    with st.spinner(f"🔍 Searching literature for '{query}'..."):
        state = run_literature_flow(query)

    st.success("✅ Literature Scout completed!")

    st.markdown("---")

    # Use columns for better layout
    col1, col2 = st.columns([2, 1])

    # Left column: report
    with col1:
        st.header("📄 Report")

        # Full report
        st.markdown(state["report_markdown"], unsafe_allow_html=True)

        md_content = state["report_markdown"]
        md_bytes = md_content.encode("utf-8")
        md_buffer = io.BytesIO(md_bytes)

        # Download button
        st.download_button(
            label="⬇️ Download Report as Markdown",
            data=md_buffer,
            file_name=f"{query.replace(' ', '_')}_literature_report.md",
            mime="text/markdown"
        )


    with col2:
        st.header("📈 Number of Papers per Year")
        st.write("##")

        years = [int(paper["year"]) for paper in state["search_results"] if paper.get("year")]
        df_years = pd.DataFrame(years, columns=["year"])

        if not df_years.empty:
            chart = alt.Chart(df_years).mark_bar().encode(
                x="year:O",
                y="count()",
                tooltip=["year", "count()"]
            ).properties(width=300)

            st.altair_chart(chart)
        else:
            st.info("No publication year data available for chart.")





