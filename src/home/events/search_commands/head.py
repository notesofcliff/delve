import logging
import argparse

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .decorators import search_command
from events.util import resolve

parser = argparse.ArgumentParser(
    prog="head",
    description="Return the first n records of the result set",
)
parser.add_argument(
    "-n", "--number",
    type=int,
    default=10,
    help="Provide the number of events to return.",
)

@search_command(parser)
def head(request, events, argv, environment):
    log = logging.getLogger(__name__)
    events = resolve(events)
    log.debug(f"Received {len(events)} events")
    log.debug(f"Received argv: {argv}")
    if "head" in argv:
        argv.pop(argv.index("head"))
    args = head.parser.parse_args(argv)

    for item in events[:args.number]:
        yield item
