import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

latest_parser = argparse.ArgumentParser(
    prog="latest",
    description="Return the latest object in the QuerySet based on the given field",
)
latest_parser.add_argument(
    "field",
    help="The field to use for determining the latest object",
)

@search_command(latest_parser)
def latest(request, events, argv, environment):
    """
    Return the latest object in the QuerySet based on the given field.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        Model: The latest object in the QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In latest")
    args = latest_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"latest can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.latest(args.field)
