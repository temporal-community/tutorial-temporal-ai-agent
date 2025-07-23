import json

from tools.find_events import find_events

# Example usage
if __name__ == "__main__":
    search_args = {"city": "Austin", "month": "December"}
    results = find_events(search_args)
    print(json.dumps(results, indent=2))
