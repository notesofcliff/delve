import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions, generate_keyword_args

exclude_parser = argparse.ArgumentParser(
    prog="exclude",
    description="Exclude objects from the QuerySet with the provided expressions",
) 
exclude_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The field/expression to exclude objects from the QuerySet with",
)

@search_command(exclude_parser)
def exclude(request, events, argv, environment):
    """
    Exclude objects from the QuerySet with the provided expressions.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet with the specified objects excluded.
    """
    log = logging.getLogger(__name__)
    log.info("In exclude")
    args = exclude_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"exclude can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    positional_args, keyword_args = generate_keyword_args(parsed_expressions)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.exclude(**keyword_args)
