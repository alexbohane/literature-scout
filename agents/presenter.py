from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


llm = ChatOpenAI(model="gpt-4o", temperature=0.1)


def presenter_agent(state: Dict) -> Dict:
    print("[PresenterAgent] Generating Markdown report...")

    papers_sorted_by_citations = sorted(
        state["search_results"], key=lambda x: x.get("cited_by_count", 0), reverse=True
    )
    top_cited_papers = papers_sorted_by_citations[:5]

    papers_sorted_by_year = sorted(
        state["search_results"], key=lambda x: x.get("year", "0"), reverse=True
    )
    top_recent_papers = papers_sorted_by_year[:5]

    # Build tables
    def build_table(papers):
        table = "| Title | Year | Journal | Citations | Link (DOI) |\n"
        table += "|-------|------|---------|-----------|------------|\n"
        for paper in papers:
            doi_url = f"https://doi.org/{paper['doi']}" if paper["doi"] else "N/A"
            table += f"| {paper['title']} | {paper['year']} | {paper['journal']} | {paper['cited_by_count']} | [{doi_url}]({doi_url}) |\n"
        return table

    top_cited_table = build_table(top_cited_papers)
    top_recent_table = build_table(top_recent_papers)

    system_message = SystemMessage(content="""
    You are a scientific presenter agent.
    You will generate a Markdown report from a query, a summary of findings, and a list of papers.
    Structure the report clearly with the following sections. 
    """)

    human_message = HumanMessage(content=f"""

    ## Key Findings

    {state["query"]}

    {state["summarised_findings"]}

    ## Top Cited Papers

    {top_cited_table}

    ## Most Recent Popular Papers

    {top_recent_table}


    Markdown Report:
    """)

    markdown_report = llm.invoke([system_message, human_message])

    state.setdefault("messages", [])
    state["messages"].extend([
    {"role": "system", "content": system_message.content},
    {"role": "human", "content": human_message.content},
    {"role": "assistant", "content": markdown_report.content}])

    state["report_markdown"] = markdown_report.content

    return state
