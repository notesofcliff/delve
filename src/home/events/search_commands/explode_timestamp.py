import argparse
import logging
from itertools import chain
from datetime import (
    datetime,
    date,
    time,
)

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="explode",
    description="Extract the available fields in a timestamp field "
                "and add them as fields to the event with the optional prefix",
)
parser.add_argument(
    "--prefix",
    default="",
    help="String to be prefixed to the name of the fields "
         "that the operation creates"
)
parser.add_argument(
    "field",
    help="A field with a timestamp as the value. All available fields from "
         "the timestamp (year, month, day, hour, etc) will be added to the event",
)

@search_command(parser)
def explode_timestamp(request, events, argv, environment):
    args = explode_timestamp.parser.parse_args(argv[1:])
    log = logging.getLogger(__name__)
    field = args.field
    log.debug(f"Found {field=}")
    events = resolve(events)
    for event in events:
        log.debug(f"Found {event=}")
        
        if field in event:
            log.debug(f"{field=} present in {event=}")
            value = event.pop(field, None)
            log.debug(f"After pop: {event=}")
            if isinstance(value, datetime):
                event.update(
                    {
                        f"{args.prefix}year": value.year,
                        f"{args.prefix}month": value.month,
                        f"{args.prefix}day": value.day,
                        f"{args.prefix}hour": value.hour,
                        f"{args.prefix}minute": value.minute,
                        f"{args.prefix}second": value.second,
                        f"{args.prefix}microsecond": value.microsecond,
                    }
                )
                log.debug(f"Event after update: {event}")
                yield event
            elif isinstance(value, date):
                event.update(
                    {
                        f"{args.prefix}year": value.year,
                        f"{args.prefix}month": value.month,
                        f"{args.prefix}day": value.day,
                    }
                )
                log.debug(f"Event after update: {event}")
                yield event
            elif isinstance(value, time):
                event.update(
                    {
                        f"{args.prefix}hour": value.hour,
                        f"{args.prefix}minute": value.minute,
                        f"{args.prefix}second": value.second,
                        f"{args.prefix}microsecond": value.microsecond,
                    }
                )
                log.debug(f"Event after update: {event}")
                yield event
            elif value is None:
                log.debug(f"Found {value=}, removing field.")
                yield event
            else:
                log.debug(f"value {value} was not a dictionary")
                event.update({field: value})
                yield event
        else:
            yield event
