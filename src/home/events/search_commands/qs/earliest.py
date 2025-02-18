import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

earliest_parser = argparse.ArgumentParser(
    prog="earliest",
    description="Return the earliest object in the QuerySet based on the given field",
)
earliest_parser.add_argument(
    "field",
    help="The field to use for determining the earliest object",
)

@search_command(earliest_parser)
def earliest(request, events, argv, environment):
    """
    Return the earliest object in the QuerySet based on the given field.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        Model: The earliest object in the QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In earliest")
    args = earliest_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"earliest can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.earliest(args.field)
