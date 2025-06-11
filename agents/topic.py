from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

def topics_agent(state: Dict) -> Dict:
    print("[TopicsAgent] Extracting key topics...")

    abstracts = [
        paper["abstract"] for paper in state["search_results"] if paper.get("abstract")
    ]
    abstracts_text = "\n\n".join(abstracts[:50])

    system_message = SystemMessage(content="""
    You are a scientific topics extraction agent.
    Given the following abstracts, extract the key research topics and concepts.
    List them as a simple bullet point list (one topic per line).
    """)

    human_message = HumanMessage(content=f"Here are the abstracts:\n\n{abstracts_text}")

    topics_response = llm.invoke([system_message, human_message])

    state["topics_themes"] = topics_response.content


    return state
