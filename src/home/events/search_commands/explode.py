import argparse
import logging
from itertools import chain

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="explode",
    description="Extract the nested JSON fields from an object and "
                "add them to the event. Also removes the original field.",
)
parser.add_argument(
    "--prefix",
    default="",
    help="String to be prefixed to the name of the fields "
            "that the explode operation creates"
)
parser.add_argument(
    "field",
    help="If field points to a JSON object, it's fields will be added "
    "to the event and the original field will be removed. "
    "Events without the specified fields will be omitted from the results"
)

@search_command(parser)
def explode(request, events, argv, environment):
    args = explode.parser.parse_args(argv[1:])
    log = logging.getLogger(__name__)
    field = args.field
    # log.info(f"Found field to explode: {field}")
    # if isinstance(events, QuerySet):
    #     log.debug(f"events is a QuerySet, converting to list of dicts")
    #     events = list(events.values())
    events = resolve(events)
    for event in events:
        log.debug(f"Found event: {event}")
        
        if field in event:
            log.debug(f"field {field} is present in event: {event}")
            value = event.pop(field, None)
            log.debug(f"Event after pop: {event}")
            if isinstance(value, dict):
                event.update(
                    {f"{args.prefix}{k}": v for k, v in value.items()}
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
