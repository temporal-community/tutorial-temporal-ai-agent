from typing import List

import tools.tool_registry as tool_registry
from models.core import AgentGoal

goal_event_flight_invoice = AgentGoal(
    id="goal_event_flight_invoice",
    category_tag="travel-flights",
    agent_name="Australia and New Zealand Event Flight Booking",
    agent_friendly_description="Book a trip to a city in Australia or New Zealand around the dates of events in that city.",
    tools=[
        tool_registry.find_events_tool,
        tool_registry.search_flights_tool,
        tool_registry.create_invoice_tool,
    ],
    description="Help the user gather args for these tools in order: "
    "1. FindEvents: Find an event to travel to "
    "2. SearchFlights: search for a flight around the event dates "
    "3. CreateInvoice: Create a simple invoice for the cost of that flight ",
    starter_prompt="Welcome me, give me a description of what you can do, then ask me for the details you need to do your job.",
    example_conversation_history="\n ".join(
        [
            "user: I'd like to travel to an event",
            "agent: Sure! Let's start by finding an event you'd like to attend. I know about events in Australia and New Zealand cities. Could you tell me which city and month you're interested in?",
            "user: sydney in may please",
            "agent: Great! Let's find an events in Sydney in May.",
            "user_confirmed_tool_run: <user clicks confirm on FindEvents tool>",
            "tool_result: { 'event_name': 'Vivid Sydney', 'event_date': '2023-05-01' }",
            "agent: Found an event! There's Vivid Sydney on May 1 2025, ending on May 14 2025. Would you like to search for flights around these dates?",
            "user: Yes, please",
            "agent: Let's search for flights around these dates. Could you provide your departure city?",
            "user: San Francisco",
            "agent: Thanks, searching for flights from San Francisco to Sydney around 2023-02-25 to 2023-02-28.",
            "user_confirmed_tool_run: <user clicks confirm on SearchFlights tool>"
            'tool_result: results including {"flight_number": "CX101", "return_flight_number": "CX102", "price": 850.0}',
            "agent: Found some flights! The cheapest is CX101 for $850. Would you like to generate an invoice for this flight?",
            "user_confirmed_tool_run: <user clicks confirm on CreateInvoice tool>",
            'tool_result: { "status": "success", "invoice": { "flight_number": "CX101", "amount": 850.0 }, invoiceURL: "https://example.com/invoice" }',
            "agent: Invoice generated! Here's the link: https://example.com/invoice",
        ]
    ),
)
# Add the goals to a list for more generic processing, like listing available agents
goal_list: List[AgentGoal] = []
goal_list.append(goal_event_flight_invoice)
