import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

exists_parser = argparse.ArgumentParser(
    prog="exists",
    description="Check if any records exist in the QuerySet",
)

@search_command(exists_parser)
def exists(request, events, argv, environment):
    """
    Check if any records exist in the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        bool: True if any records exist, False otherwise.
    """
    log = logging.getLogger(__name__)
    log.info("In exists")
    args = exists_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"exists can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.exists()
