from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any, Optional
from agents.search_scout import search_scout_agent
from agents.synthesiser import synthesiser_agent
from agents.topic import topics_agent
from agents.presenter import presenter_agent
from dotenv import load_dotenv
from langgraph.constants import START, END



load_dotenv()


# Define state
class LiteratureState(TypedDict):
    query: str
    search_results: List[Dict]
    summarised_findings: str
    report_markdown: str
    # topics_themes: str
    messages: List[Dict[str, Any]]

# Define flow
def run_literature_flow(query: str) -> LiteratureState:
    initial_state = {
        "query": query,
        "search_results": [],
        "summarised_findings": "",
        "report_markdown": "",
        # "topics_themes": "",
        "messages": [],
    }

    flow = StateGraph(LiteratureState)

    flow.add_node("SearchScoutAgent", search_scout_agent)
    flow.add_node("SynthesiserAgent", synthesiser_agent)
    flow.add_node("PresenterAgent", presenter_agent)
    # flow.add_node("TopicsAgent", topics_agent)

    flow.add_edge(START, "SearchScoutAgent")
    flow.add_edge("SearchScoutAgent", "SynthesiserAgent")
    flow.add_edge("SynthesiserAgent", "PresenterAgent")
    flow.add_edge("PresenterAgent", END)

    built_flow = flow.compile()
    final_state = built_flow.invoke(initial_state)

    png_data = built_flow.get_graph().draw_mermaid_png()
    with open("agent_graph.png", "wb") as f:
        f.write(png_data)
    return final_state
