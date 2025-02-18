import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

using_parser = argparse.ArgumentParser(
    prog="using",
    description="Select the database to use for the QuerySet",
)
using_parser.add_argument(
    "alias",
    help="The alias of the database to use",
)

@search_command(using_parser)
def using(request, events, argv, environment):
    """
    Select the database to use for the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet using the specified database.
    """
    log = logging.getLogger(__name__)
    log.info("In using")
    args = using_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"using can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.using(args.alias)
