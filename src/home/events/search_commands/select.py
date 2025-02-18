import argparse
import logging
import inspect
from types import GeneratorType

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="select",
    description="Remove all but the specified fields from all events."
)
parser.add_argument(
    nargs="+",
    dest="fields",
)

@search_command(parser)
def select(request, events, argv, environment):
    log = logging.getLogger(__name__)
    args = select.parser.parse_args(argv[1:])
    log.warning(f"Found args: {args}")
    if isinstance(events, GeneratorType) or inspect.isgeneratorfunction(events) or isinstance(events, list):
        log.debug("Found events to be list or generator function.")
        for event in events:
            # log.warning(f"Found event with fields: {event.keys()}")
            row = {}
            for field in args.fields:
                item = event
                for segment in field.split("__"):
                    log.debug(f"Trying segment: {segment}")
                    try:
                        item = item[segment]
                        log.debug(f"Found segment {segment}: {item}")
                    except KeyError:
                        log.warning(f"Received KeyError, field {segment} not in {item}")
                        item = None
                    except TypeError:
                        item = getattr(item, segment)
                row[field] = item
                log.debug(f"row[field]: {row[field]}")
            # if not all(value for value in row.values()):
            #     pass
            # else:
            log.debug(f"Yielding row: {row}")
            yield row
    elif isinstance(events, QuerySet):
        # for field in args.fields:
        #     events = events.exclude(**{f"{field}__isnull": True})
        log.debug(f"Found events to be instance of QuerySet.")
        for row in list(events.values(*args.fields)):
            log.debug(f"Yielding row: {row}")
            yield row
    else:
        log.warning(f"Found type(events): {type(events)}")
