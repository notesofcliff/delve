import logging
import argparse
from typing import Any, Dict, List

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.search_commands.decorators import search_command
from events.search_commands.util import has_permission_for_model

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
def select_related(request: HttpRequest, events: QuerySet, argv: List[str], environment: Dict[str, Any]) -> QuerySet:
    """
    Perform a SQL join and include the fields of the related object in the QuerySet.

    Args:
        request (HttpRequest): The HTTP request object.
        events (QuerySet): The QuerySet to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

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
    event_model = events.query.model
    related_models = event_model._meta.related_objects
    related_models = [related_model.related_model for related_model in related_models]
    related_models = {related_model.__name__: related_model for related_model in related_models}
    for related_field in args.related_fields:
        if related_field not in related_models:
            raise ValueError(f"Related field {related_field} not found in {event_model.__name__}")
        else:
            model = related_models[related_field]
            if not has_permission_for_model('view', model, request):
                raise PermissionError("Permission denied")

    log.debug(f"Received {args=}")
    return events.select_related(*args.related_fields)
