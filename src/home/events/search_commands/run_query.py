import re
import argparse
import logging

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.models import Query
from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="run_query",
    description="Run a named query. If any events are received, the results of "
                 "the query are appended to the events received.",
)
parser.add_argument(
    "name",
)

@search_command(parser)
def run_query(request, events, argv, environment):
    log = logging.getLogger(__name__)
    events = resolve(events)
    args = run_query.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")
    name = args.name
    log.debug(f"found name: {name}")
    try:
        query = Query.objects.get(name=name)
    except Query.DoesNotExist:
        log.exception("Named query does not exist for specified user.")
        raise
    new_events = query.resolve(request=request, events=events, context=environment)
    # for event in events:
    #     log.debug(f"Found event: {event}")
    #     yield event
    if events:
        if isinstance(new_events, list):
            # for event in new_events:
            return events + new_events
        else:
            return events + [new_events]
    else:
        return new_events
