import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command
from ._util import parse_field_expressions, generate_keyword_args

explain_parser = argparse.ArgumentParser(
    prog="explain",
    description="Generate an execution plan for the QuerySet",
)
explain_parser.add_argument(
    "--format",
    help="The format of the execution plan",
)
explain_parser.add_argument(
    "options",
    nargs="*",
    help="Additional options for the execution plan",
)

@search_command(explain_parser)
def explain(request, events, argv, environment):
    """
    Generate an execution plan for the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        str: The execution plan.
    """
    log = logging.getLogger(__name__)
    log.info("In explain")
    args = explain_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"explain can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    parsed_options = parse_field_expressions(args.options)
    log.debug(f"Parsed options: {parsed_options}")
    positional_args, keyword_args = generate_keyword_args(parsed_options)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.explain(format=args.format, **keyword_args)
