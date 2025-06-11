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
    abstracts = [
        paper["abstract"] for paper in state["search_results"] if paper.get("abstract")
    ]
    abstracts_text = "\n\n".join(abstracts[:50])  # Limit to top N abstracts



    system_message = SystemMessage(content="""
    You are a scientific summariser agent.
    You will be given a list of scientific abstracts.
    Summarise the key findings clearly and concisely in plain bullet points.
    Focus on the main contributions, results, and implications of the research.
    Include the current trends and developments in the field in bullet point format.
    Do not include any citations or references.
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

