import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

select_related_parser = argparse.ArgumentParser(
    prog="select_related",
    description="Perform a SQL join and include the fields of the related object in the QuerySet",
) 
select_related_parser.add_argument(
    "related_fields",
    nargs="*",
    help="The related fields to include in the QuerySet",
)

@search_command(select_related_parser)
def select_related(request, events, argv, environment):
    """
    Perform a SQL join and include the fields of the related object in the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        QuerySet: A QuerySet with the related fields included.
    """
    log = logging.getLogger(__name__)
    log.info("In select_related")
    args = select_related_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"select_related can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.select_related(*args.related_fields)
