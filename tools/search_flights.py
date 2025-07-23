import json
import os
import random

import requests
from dotenv import load_dotenv


def search_airport(query: str) -> list:
    """
    Returns a list of matching airports/cities from sky-scrapper's searchAirport endpoint.
    """
    load_dotenv(override=True)
    api_key = os.getenv("RAPIDAPI_KEY", "YOUR_DEFAULT_KEY")
    api_host = os.getenv("RAPIDAPI_HOST_FLIGHTS", "sky-scrapper.p.rapidapi.com")

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
    }

    # Sanitize the query to ensure it is URL-safe
    print(f"Searching for: {query}")
    url = f"https://{api_host}/api/v1/flights/searchAirport"
    params = {"query": query, "locale": "en-US"}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: API responded with status code {response.status_code}")
            print(f"Response: {response.text}")
            return []

        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response")
        print(f"Response: {response.text}")
        return []


def search_flights_real_api(
    args: dict,
) -> dict:  # rename to search_flights to use the real API
    """
    1) Looks up airport/city codes via search_airport.
    2) Finds the first matching skyId/entityId for both origin & destination.
    3) Calls the flight search endpoint with those codes.
    """
    date_depart = args.get("dateDepart")
    date_return = args.get("dateReturn")
    origin_query = args.get("origin", "")
    dest_query = args.get("destination", "")

    # Step 1: Resolve skyIds
    origin_candidates = search_airport(origin_query)
    destination_candidates = search_airport(dest_query)

    if not origin_candidates or not destination_candidates:
        return {"error": "No matches found for origin/destination"}

    origin_params = origin_candidates[0]["navigation"]["relevantFlightParams"]
    dest_params = destination_candidates[0]["navigation"]["relevantFlightParams"]

    origin_sky_id = origin_params["skyId"]  # e.g. "LOND"
    origin_entity_id = origin_params["entityId"]  # e.g. "27544008"
    dest_sky_id = dest_params["skyId"]  # e.g. "NYCA"
    dest_entity_id = dest_params["entityId"]  # e.g. "27537542"

    # Step 2: Call flight search with resolved codes
    load_dotenv(override=True)
    api_key = os.getenv("RAPIDAPI_KEY", "YOUR_DEFAULT_KEY")
    api_host = os.getenv("RAPIDAPI_HOST_FLIGHTS", "sky-scrapper.p.rapidapi.com")

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
    }

    url = f"https://{api_host}/api/v2/flights/searchFlights"
    params = {
        "originSkyId": origin_sky_id,
        "destinationSkyId": dest_sky_id,
        "originEntityId": origin_entity_id,
        "destinationEntityId": dest_entity_id,
        "date": date_depart,
        "returnDate": date_return,
        "cabinClass": "economy",
        "adults": "1",
        "sortBy": "best",
        "currency": "USD",
        "market": "en-US",
        "countryCode": "US",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        json_data = response.json()
    except requests.RequestException as e:
        return {"error": f"Request error: {e}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

    itineraries = json_data.get("data", {}).get("itineraries", [])
    if not itineraries:
        return json_data  # Return raw response for debugging if itineraries are empty

    formatted_results = []
    seen_carriers = set()

    for itinerary in itineraries:
        legs = itinerary.get("legs", [])
        if len(legs) >= 2:
            # Extract outbound and return flight details
            outbound_leg = legs[0]
            return_leg = legs[1]

            # Get the first segment for flight details
            outbound_flight = outbound_leg.get("segments", [{}])[0]
            return_flight = return_leg.get("segments", [{}])[0]

            # Extract flight details
            outbound_carrier = outbound_flight.get("operatingCarrier", {}).get(
                "name", "N/A"
            )
            outbound_carrier_code = outbound_flight.get("operatingCarrier", {}).get(
                "alternateId", ""
            )
            outbound_flight_number = outbound_flight.get("flightNumber", "N/A")
            outbound_flight_code = (
                f"{outbound_carrier_code}{outbound_flight_number}"
                if outbound_carrier_code
                else outbound_flight_number
            )

            return_carrier = return_flight.get("operatingCarrier", {}).get(
                "name", "N/A"
            )
            return_carrier_code = return_flight.get("operatingCarrier", {}).get(
                "alternateId", ""
            )
            return_flight_number = return_flight.get("flightNumber", "N/A")
            return_flight_code = (
                f"{return_carrier_code}{return_flight_number}"
                if return_carrier_code
                else return_flight_number
            )

            # Check if carrier is unique
            if outbound_carrier not in seen_carriers:
                seen_carriers.add(outbound_carrier)  # Add to seen carriers
                formatted_results.append(
                    {
                        "outbound_flight_code": outbound_flight_code,
                        "operating_carrier": outbound_carrier,
                        "return_flight_code": return_flight_code,
                        "return_operating_carrier": return_carrier,
                        "price": itinerary.get("price", {}).get("raw", 0.0),
                    }
                )

            # Stop after finding 3 unique carriers
            if len(formatted_results) >= 3:
                break

    return {
        "origin": origin_query,
        "destination": dest_query,
        "currency": "USD",
        "results": formatted_results,
    }


def generate_smart_flights(origin: str, destination: str) -> list:
    """
    Generate realistic flight options with smart pricing based on origin and destination.
    """
    # Common airlines for different regions
    airlines_by_region = {
        "domestic_us": [
            {"name": "American Airlines", "code": "AA"},
            {"name": "United Airlines", "code": "UA"},
            {"name": "Delta Airlines", "code": "DL"},
            {"name": "Southwest Airlines", "code": "WN"},
        ],
        "domestic_canada": [
            {"name": "Air Canada", "code": "AC"},
            {"name": "WestJet", "code": "WS"},
        ],
        "us_canada": [
            {"name": "American Airlines", "code": "AA"},
            {"name": "United Airlines", "code": "UA"},
            {"name": "Delta Airlines", "code": "DL"},
            {"name": "Air Canada", "code": "AC"},
        ],
        "international": [
            {"name": "American Airlines", "code": "AA"},
            {"name": "United Airlines", "code": "UA"},
            {"name": "Delta Airlines", "code": "DL"},
        ],
    }

    # Determine route type and base pricing
    origin_lower = origin.lower()
    dest_lower = destination.lower()

    # US cities from find_events_data.json
    us_cities = [
        # Major cities with events
        "new york",
        "los angeles",
        "chicago",
        "houston",
        "philadelphia",
        "phoenix",
        "san antonio",
        "san diego",
        "dallas",
        "san jose",
        "austin",
        "jacksonville",
        "fort worth",
        "columbus",
        "charlotte",
        "san francisco",
        "indianapolis",
        "seattle",
        "denver",
        "washington",
        "boston",
        "el paso",
        "nashville",
        "detroit",
        "oklahoma city",
        "portland",
        "las vegas",
        "louisville",
        "baltimore",
        "milwaukee",
        "albuquerque",
        "tucson",
        "fresno",
        "sacramento",
        "kansas city",
        "mesa",
        "atlanta",
        "colorado springs",
        "raleigh",
        "omaha",
        "miami",
        "long beach",
        "virginia beach",
        "oakland",
        "minneapolis",
        "tulsa",
        "arlington",
        "new orleans",
        "wichita",
        "cleveland",
        "tampa",
        # Common airport codes
        "lax",
        "sfo",
        "nyc",
        "jfk",
        "ord",
        "mia",
        "dfw",
        "atl",
        "den",
        "sea",
        "bos",
        "phx",
        "las",
        "dtw",
        "msp",
        "stl",
        "tpa",
        "mco",
        "iad",
        "bwi",
        "pdx",
        "san",
        "smf",
        "sjc",
        "oak",
        "rno",
        "slc",
        "mke",
        "msy",
        "sat",
        "aus",
        "iah",
        "dal",
        "okc",
        "tul",
        "lit",
        "mem",
        "bna",
        "rdu",
        "clt",
        "gso",
        "jax",
        "fll",
        "pbi",
        "rsw",
        "tus",
        "abq",
        "elp",
        "cos",
        "dsm",
        "oma",
        "ict",
        "cvg",
        "cle",
        "cmh",
        "ind",
        "sdf",
    ]

    # Canadian cities
    canadian_cities = [
        "toronto",
        "yyz",
        "montreal",
        "yul",
        "vancouver",
        "yvr",
        "calgary",
        "yyc",
        "ottawa",
        "yow",
        "edmonton",
        "yeg",
        "winnipeg",
        "ywg",
        "quebec",
        "yqb",
        "hamilton",
        "yhm",
    ]

    is_origin_us = any(city in origin_lower for city in us_cities)
    is_dest_us = any(city in dest_lower for city in us_cities)
    is_origin_canada = any(city in origin_lower for city in canadian_cities)
    is_dest_canada = any(city in dest_lower for city in canadian_cities)

    # Determine airline pool and base price
    if is_origin_us and is_dest_us:
        # US domestic
        airline_pool = airlines_by_region["domestic_us"]
        base_price = random.randint(200, 800)
    elif is_origin_canada and is_dest_canada:
        # Canada domestic
        airline_pool = airlines_by_region["domestic_canada"]
        base_price = random.randint(150, 600)
    elif (is_origin_us and is_dest_canada) or (is_origin_canada and is_dest_us):
        # US-Canada routes
        airline_pool = airlines_by_region["us_canada"]
        base_price = random.randint(250, 700)
    else:
        # General international
        airline_pool = airlines_by_region["international"]
        base_price = random.randint(800, 1500)

    # Generate 3-4 flight options
    num_flights = random.randint(3, 4)
    results = []
    used_airlines = set()

    for i in range(num_flights):
        # Pick unique airline
        available_airlines = [a for a in airline_pool if a["name"] not in used_airlines]
        if not available_airlines:
            available_airlines = airline_pool  # Reset if we run out

        airline = random.choice(available_airlines)
        used_airlines.add(airline["name"])

        # Generate flight numbers
        outbound_num = random.randint(100, 999)
        return_num = random.randint(100, 999)

        # Price variation (cheaper airlines get lower prices)
        price_multiplier = 1.0
        if "Southwest" in airline["name"] or "WestJet" in airline["name"]:
            price_multiplier = 0.7

        # Add some random variation
        price_variation = random.uniform(0.9, 1.1)
        final_price = round(base_price * price_multiplier * price_variation, 2)

        results.append(
            {
                "operating_carrier": airline["name"],
                "outbound_flight_code": f"{airline['code']}{outbound_num}",
                "price": final_price,
                "return_flight_code": f"{airline['code']}{return_num}",
                "return_operating_carrier": airline["name"],
            }
        )

    # Sort by price
    results.sort(key=lambda x: x["price"])
    return results


def search_flights(args: dict) -> dict:
    """
    Search for flights. Uses real API if RAPIDAPI_KEY is available, otherwise generates smart mock data.
    """
    load_dotenv(override=True)
    api_key = os.getenv("RAPIDAPI_KEY")

    origin = args.get("origin")
    destination = args.get("destination")

    if not origin or not destination:
        return {"error": "Both origin and destination are required"}

    # If API key is available, use the real API
    if api_key and api_key != "YOUR_DEFAULT_KEY":
        return search_flights_real_api(args)

    # Otherwise, generate smart mock data
    results = generate_smart_flights(origin, destination)

    return {
        "currency": "USD",
        "destination": destination,
        "origin": origin,
        "results": results,
    }
