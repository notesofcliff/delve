import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions

only_parser = argparse.ArgumentParser(
    prog="only",
    description="Load only the specified fields",
)
only_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The fields to load",
)

@search_command(only_parser)
def only(request, events, argv, environment):
    """
    Load only the specified fields.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet with only the specified fields loaded.
    """
    log = logging.getLogger(__name__)
    log.info("In only")
    args = only_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"only can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    return events.only(*parsed_expressions)
