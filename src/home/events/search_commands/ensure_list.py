import argparse
import logging
from itertools import chain

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="ensure_list",
    description="Ensure that field contains a list. If any other type of value "
                "is in the specified field, it will be placed as a single"
                "item in a list",
)
parser.add_argument(
    "field",
    help="The list to ensure it is a list")

@search_command(parser)
def ensure_list(request, events, argv, environment):
    args = ensure_list.parser.parse_args(argv[1:])
    log = logging.getLogger(__name__)
    field = args.field
    # log.info(f"Found field to explode: {field}")
    events = resolve(events)
    for event in events:
        log.debug(f"Found event: {event}")
        if field in event:
            log.debug(f"field {field} is present in event: {event}")
            value = event.get(field)
            if not isinstance(value, list):
                event[field] = [value]
            yield event
        else:
            event[field] = [None]
            yield event
