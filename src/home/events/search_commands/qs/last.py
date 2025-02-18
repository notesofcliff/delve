import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

last_parser = argparse.ArgumentParser(
    prog="last",
    description="Return the last object in the QuerySet",
)

@search_command(last_parser)
def last(request, events, argv, environment):
    """
    Return the last object in the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        Model instance: The last object in the QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In last")
    args = last_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"last can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.last()
