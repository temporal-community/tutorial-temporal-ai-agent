import json
from datetime import date, datetime
from pathlib import Path


def find_events(args: dict) -> dict:
    search_city = args.get("city", "").lower()
    search_month = args.get("month", "").capitalize()

    file_path = Path(__file__).resolve().parent / "data" / "find_events_data.json"
    if not file_path.exists():
        return {"error": "Data file not found."}

    try:
        month_number = datetime.strptime(search_month, "%B").month
    except ValueError:
        return {"error": "Invalid month provided."}

    # Helper to wrap months into [1..12]
    def get_adjacent_months(m):
        prev_m = 12 if m == 1 else (m - 1)
        next_m = 1 if m == 12 else (m + 1)
        return [prev_m, m, next_m]

    valid_months = get_adjacent_months(month_number)
    current_date = date.today()

    matching_events = []
    with open(file_path) as f:
        data = json.load(f)
    for city_name, events in data.items():
        if search_city and search_city not in city_name.lower():
            continue

        for event in events:
            date_from = datetime.strptime(event["dateFrom"], "%Y-%m-%d").date()
            date_to = datetime.strptime(event["dateTo"], "%Y-%m-%d").date()

            # Check if event has already passed and adjust year if needed
            if date_from < current_date:
                # Increment year by 1 for both dates
                date_from = date_from.replace(year=current_date.year + 1)
                date_to = date_to.replace(year=current_date.year + 1)

            # If the event's start or end month is in our valid months
            if date_from.month in valid_months or date_to.month in valid_months:
                # Add metadata explaining how it matches
                if date_from.month == month_number or date_to.month == month_number:
                    month_context = "requested month"
                elif (
                    date_from.month == valid_months[0]
                    or date_to.month == valid_months[0]
                ):
                    month_context = "previous month"
                else:
                    month_context = "next month"

                matching_events.append(
                    {
                        "city": city_name,
                        "eventName": event["eventName"],
                        "dateFrom": date_from.strftime("%Y-%m-%d"),
                        "dateTo": date_to.strftime("%Y-%m-%d"),
                        "description": event["description"],
                        "month": month_context,
                    }
                )

    # Add top-level metadata if you wish
    return {
        "note": f"Returning events from {search_month} plus one month either side (i.e., {', '.join(datetime(2025, m, 1).strftime('%B') for m in valid_months)}).",
        "events": matching_events,
    }
