import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

reverse_parser = argparse.ArgumentParser(
    prog="reverse",
    description="Reverse the order of the QuerySet",
)

@search_command(reverse_parser)
def reverse(request, events, argv, environment):
    """
    Reverse the order of the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A reversed QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In reverse")
    args = reverse_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"reverse can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.reverse()
