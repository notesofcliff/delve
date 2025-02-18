import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions, generate_keyword_args

aggregate_parser = argparse.ArgumentParser(
    prog="aggregate",
    description="Perform aggregation on the result set",
) 
aggregate_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The field/expression to aggregate from the result set",
)

@search_command(aggregate_parser)
def aggregate(request, events, argv, environment):
    """
    Perform aggregation on the result set.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        dict: A dictionary of aggregated values.
    """
    log = logging.getLogger(__name__)
    log.info("In aggregate")
    args = aggregate_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"aggregate can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    positional_args, keyword_args = generate_keyword_args(parsed_expressions)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.aggregate(**keyword_args)
