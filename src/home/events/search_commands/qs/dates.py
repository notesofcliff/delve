import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

dates_parser = argparse.ArgumentParser(
    prog="dates",
    description="Return a list of date objects representing all available dates in the QuerySet",
)
dates_parser.add_argument(
    "field",
    help="The field to retrieve dates from",
)
dates_parser.add_argument(
    "kind",
    choices=["year", "month", "week", "day"],
    help="The kind of dates to retrieve",
)
dates_parser.add_argument(
    "order",
    choices=["ASC", "DESC"],
    help="The order in which to retrieve the dates",
)

@search_command(dates_parser)
def dates(request, events, argv, environment):
    """
    Return a list of date objects representing all available dates in the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet of date objects.
    """
    log = logging.getLogger(__name__)
    log.info("In dates")
    args = dates_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"dates can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.dates(args.field, args.kind, args.order)
