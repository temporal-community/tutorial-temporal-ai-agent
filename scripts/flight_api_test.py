import json

from tools.search_flights import search_flights

if __name__ == "__main__":
    # Suppose user typed "new" for New York, "lon" for London
    flights = search_flights(
        {
            "origin": "AUS",
            "destination": "SYD",
            "dateDepart": "2026-04-26",
            "dateReturn": "2026-05-04",
        }
    )
    print(json.dumps(flights, indent=2))
