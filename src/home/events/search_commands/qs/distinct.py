import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

distinct_parser = argparse.ArgumentParser(
    prog="distinct",
    description="Return distinct records from the QuerySet",
) 
distinct_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The fields to consider for distinct records",
)

@search_command(distinct_parser)
def distinct(request, events, argv, environment):
    """
    Return distinct records from the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet with distinct records.
    """
    log = logging.getLogger(__name__)
    log.info("In distinct")
    args = distinct_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"distinct can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.distinct(*args.field_expressions)
