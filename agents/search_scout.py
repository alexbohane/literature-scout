from utils.europe_pmc_api import europe_pmc_api_call
from typing import TypedDict, List, Dict

def search_scout_agent(state: Dict) -> Dict:
    print("[SearchScoutAgent] Querying Europe PMC...")

    papers = europe_pmc_api_call(state["query"])
    state["search_results"] = papers

    query = state["query"]

    state.setdefault("messages", [])
    state["messages"].append({
        "role": "assistant",
        "content": f"SearchScoutAgent found {len(papers)} papers for query: {query}."
    })

    return state
