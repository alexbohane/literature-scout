import requests
from typing import List, Dict



def europe_pmc_api_call(query: str, max_results=1000) -> List[Dict]:
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    page_size = 100
    papers = []
    cursor_mark = "*"

    try:
        while len(papers) < max_results:
            params = {
                "query": f'(TITLE_ABS:("{query}") OR MESH_HEADING:("{query}")) AND PUB_YEAR:[2020 TO 2026] AND SRC:MED',
                "format": "json",
                "pageSize": page_size,
                "cursorMark": cursor_mark,
                "resultType": "core",
                "sort": "CITED desc"
            }

            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            results = data.get("resultList", {}).get("result", [])
            if not results:
                break



            for result in results:
                doi = result.get("doi", "")
                mesh_terms = []
                mesh_list = result.get("meshHeadingList", {}).get("meshHeading", [])
                for mesh_entry in mesh_list:
                    term = mesh_entry.get("descriptorName")
                    if term:
                        mesh_terms.append(term)
                if doi:
                    papers.append({
                        "title": result.get("title", ""),
                        "abstract": result.get("abstractText", ""),
                        "year": result.get("pubYear", ""),
                        "journal": result.get("journalTitle", ""),
                        "doi": doi,
                        "cited_by_count": int(result.get("citedByCount", "0")),
                        # "mesh_terms": mesh_terms,
                        "author_string": result.get("authorString", "")
                    })
                    if len(papers) >= max_results:
                        break

            cursor_mark = data.get("nextCursorMark")
            if not cursor_mark:
                break

    except requests.RequestException as e:
        print(f"Error calling Europe PMC API: {e}")

    return papers