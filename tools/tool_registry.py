from typing import Any, Callable, Dict

from models.core import ToolArgument, ToolDefinition
from tools.create_invoice import create_invoice
from tools.find_events import find_events
from tools.search_flights import search_flights

find_events_tool = ToolDefinition(
    name="FindEvents",
    description="Find upcoming events to travel to a given city (e.g., 'New York City') and a date or month. "
    "It knows about events in North America only (e.g. major North American cities). "
    "It will search 1 month either side of the month provided. "
    "Returns a list of events. ",
    arguments=[
        ToolArgument(
            name="city",
            type="string",
            description="Which city to search for events",
        ),
        ToolArgument(
            name="month",
            type="string",
            description="The month to search for events (will search 1 month either side of the month provided)",
        ),
    ],
)


search_flights_tool = ToolDefinition(
    name="SearchFlights",
    description="Search for return flights from an origin to a destination within a date range (dateDepart, dateReturn). "
    "You are allowed to suggest dates from the conversation history, but ALWAYS ask the user if ok.",
    arguments=[
        ToolArgument(
            name="origin",
            type="string",
            description="Airport or city (infer airport code from city and store)",
        ),
        ToolArgument(
            name="destination",
            type="string",
            description="Airport or city code for arrival (infer airport code from city and store)",
        ),
        ToolArgument(
            name="dateDepart",
            type="ISO8601",
            description="Start of date range in human readable format, when you want to depart",
        ),
        ToolArgument(
            name="dateReturn",
            type="ISO8601",
            description="End of date range in human readable format, when you want to return",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of the user's desire to search flights, and to confirm the details "
            + "before moving on to the next step",
        ),
    ],
)

create_invoice_tool = ToolDefinition(
    name="CreateInvoice",
    description="Generate an invoice for the items described for the total inferred by the conversation history so far. Returns URL to invoice.",
    arguments=[
        ToolArgument(
            name="amount",
            type="float",
            description="The total cost to be invoiced. Infer this from the conversation history.",
        ),
        ToolArgument(
            name="tripDetails",
            type="string",
            description="A description of the item details to be invoiced, inferred from the conversation history.",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to create an invoice",
        ),
    ],
)


# Dictionary mapping tool names to their handler functions
TOOL_HANDLERS: Dict[str, Callable[..., Any]] = {
    "SearchFlights": search_flights,
    "CreateInvoice": create_invoice,
    "FindEvents": find_events,
}


def get_handler(tool_name: str) -> Callable[..., Any]:
    """Get the handler function for a given tool name.

    Args:
        tool_name: The name of the tool to get the handler for.

    Returns:
        The handler function for the specified tool.

    Raises:
        ValueError: If the tool name is not found in the registry.
    """
    if tool_name not in TOOL_HANDLERS:
        raise ValueError(f"Unknown tool: {tool_name}")

    return TOOL_HANDLERS[tool_name]
