import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions, generate_keyword_args

filter_parser = argparse.ArgumentParser(
    prog="filter",
    description="Filter the QuerySet with the provided expressions",
) 
filter_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The field/expression to filter the QuerySet with",
)

@search_command(filter_parser)
def filter(request, events, argv, environment):
    """
    Filter the QuerySet with the provided expressions.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A filtered QuerySet.
    """
    log = logging.getLogger(__name__)
    log.info("In filter")
    args = filter_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"filter can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    positional_args, keyword_args = generate_keyword_args(parsed_expressions)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.filter(*positional_args, **keyword_args)
