import argparse
from datetime import (
    datetime,
    timedelta,
)
import logging

from dateutil.parser import parse
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils import timezone

from events.models import Event
from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="mark_timestamp",
    description="Parse the given fields from strings to datetime objects. Useful for use with filter search_command",
)
parser.add_argument(
    "fields",
    nargs="+",
    help="Provide the fields you would like to parse as datetime",
)

@search_command(parser)
def mark_timestamp(request, events, argv, environment):
    log = logging.getLogger(__name__)
    # log.info(f"Received {len(events)} events")
    events = resolve(events)
    log.info(f"Received argv: {argv}")
    if "mark_timestamp" in argv:
        argv.pop(argv.index("mark_timestamp"))
    args = mark_timestamp.parser.parse_args(argv)
    log.info(f"Parsed args: {args}")
    for event in events:
        for field in args.fields:
            if field in event:
                if not isinstance(event[field], datetime):
                    event[field] = parse(event[field])
        yield event
