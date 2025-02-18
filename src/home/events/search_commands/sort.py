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
    prog="sort",
    description="Sort the result set by the given fields",
)
parser.add_argument(
    "-d", "--descending",
    action="store_true",
    help="If specified, sorting will be done in descending order",
)
parser.add_argument(
    nargs="*",
    dest="fields",
)

@search_command(parser)
def sort(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.debug(f"Found events: {events}")
    args = sort.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")

    events = resolve(events)

    if not args.fields:
        log.info("No fields specified, using default sort")
        return sorted(
            events,
            reverse=args.descending,
        )
    else:
        log.debug(f"Sorting by fields: {args.fields}")
        events.sort(
            reverse=args.descending,
            key=itemgetter(*args.fields),
        )

    return events
