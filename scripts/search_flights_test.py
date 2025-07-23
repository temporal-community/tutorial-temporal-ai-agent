import json

from tools.search_flights import search_flights

if __name__ == "__main__":
    # Suppose user typed "new" for New York, "lon" for London
    flights = search_flights(
        {
            "origin": "HOU",
            "destination": "AUS",
            "dateDepart": "2025-09-20",
            "dateReturn": "2025-09-22",
        }
    )
    print(json.dumps(flights, indent=2))
