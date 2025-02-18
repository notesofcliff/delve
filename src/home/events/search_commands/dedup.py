import argparse
import logging
import inspect
from types import GeneratorType
from itertools import chain
from operator import itemgetter, attrgetter, methodcaller

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .util import cast
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="dedup",
    description="Deduplicate the result set based on the "
                 "optional fields. First matching item is kept. "
                 "(events should be sorted prior to calling this)",
)
parser.add_argument(
    nargs="*",
    dest="fields",
)

@search_command(parser)
def dedup(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.debug(f"Found events: {events}")
    args = dedup.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")

    events = resolve(events=events)

    if not args.fields:
        log.info("No fields specified, using default comparison")
        ret = []
        last_event = None
        for event in events:
            if event == last_event:
                pass
            else:
                ret.append(event)
                last_event = event
    else:
        log.debug(f"Deduplicating by fields: {args.fields}")
        last_event = None
        ret = []
        for event in events:
            new_event = {field: event.get(field) for field in args.fields}
            if new_event == last_event:
                log.debug(f"Removing event: {new_event}, considered equal to {last_event}")
                pass
            else:
                ret.append(event)
                last_event = new_event
    return ret
