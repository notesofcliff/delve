import logging
import argparse

from django.db.models.query import QuerySet

from events.search_commands.decorators import search_command

delete_parser = argparse.ArgumentParser(
    prog="delete",
    description="Delete the objects in the QuerySet",
)

@search_command(delete_parser)
def delete(request, events, argv, environment):
    """
    Delete the objects in the QuerySet.

    Args:
        request: The HTTP request object.
        events: The QuerySet to operate on.
        argv: List of command-line arguments.
        environment: Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        tuple: The number of objects deleted and a dictionary with the number of deletions per object type.
    """
    log = logging.getLogger(__name__)
    log.info("In delete")
    args = delete_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"delete can only operate on QuerySets like "
            "the output of the search command"
        )
    
    log.debug(f"Received {args=}")
    return events.delete()
