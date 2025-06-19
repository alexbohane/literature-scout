from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")


def synthesiser_agent(state: Dict) -> Dict:
    print("[SynthesiserAgent] Summarising abstracts...")

    # abstracts = [
    #     paper["abstract"] for paper in state["search_results"] if paper.get("abstract")
    # ]

    # print(abstracts[:5])  # Print first 5 abstracts for debugging

    # abstracts_text = "\n\n".join(abstracts[:50])  # Limit to top N abstracts

    papers = [
        paper for paper in state["search_results"]
        if paper.get("abstract") and paper.get("doi")][:30]  # Trim if needed for token limit

    # Format abstracts with citation context
    formatted_abstracts = []
    for i, paper in enumerate(papers, 1):
        author = paper['author_string'].split(',')[0].strip().split()[0] + " et al."
        year = paper.get("year", "n.d.")
        doi = paper.get("doi")
        citation_label = f"[{author}, {year}]"
        doi_link = f"https://doi.org/{doi}" if doi else "N/A"
        formatted = (
            f"[{i}] {paper['title']}\n"
            f"Authors: {paper['author_string']}\n"
            f"Year: {year}\n"
            f"DOI: {doi_link}\n"
            f"CitationLabel: {citation_label}\n"
            f"Abstract:\n{paper['abstract']}"
        )
        formatted_abstracts.append(formatted)


    abstracts_text = "\n\n".join(formatted_abstracts)




    system_message = SystemMessage(content="""
    You are a scientific summariser agent.
    You will receive a list of scientific abstracts, each with a unique ID, citation label, and DOI.
    Your task is to synthesise **overall key findings and current trends** across the entire set of papers.

    Write 4-6 bullet points summarising:
    - Major themes
    - Repeated findings
    - Novel methods
    - Emerging areas

    When a specific point is supported by one or more papers, cite 1-3 of the **most relevant** papers in-line using this format:
    - [Author, Year] — based on the CitationLabel provided

    Only cite when necessary, and **do not cite every point**. Keep it readable and human-like.

    Do not invent citations. Use only those from the abstracts provided.
    """)

    human_message = HumanMessage(content=f"Here is the list of abstracts:\n\n{abstracts_text}")

    summary = llm.invoke([system_message, human_message])

    state.setdefault("messages", [])
    state["messages"].extend([
    {"role": "system", "content": system_message.content},
    {"role": "human", "content": human_message.content},
    {"role": "assistant", "content": summary.content}])

    state["summarised_findings"] = summary.content


    return state

