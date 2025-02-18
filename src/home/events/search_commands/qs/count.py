import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

count_parser = argparse.ArgumentParser(
    prog="count",
    description="Return the number of records in the QuerySet",
)

@search_command(count_parser)
def count(request, events, argv, environment):
    """
    Return the number of records in the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        int: The number of records in the QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In count")
    args = count_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"count can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.count()
