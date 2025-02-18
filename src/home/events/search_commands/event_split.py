import argparse
import logging

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="event_split",
    description="Attempt to split events into multiple events based on a field. "
                "Specified fields should contain a JSON Array.",
)
parser.add_argument(
    "split_field",
    help="If the specified split field points to a list, the "
            "events returned will be expanded with an event per item "
            "in the list. The fields of the events will be preserved "
            "with each new item having a copy of other fields' values."
)

@search_command(parser)
def event_split(request, events, argv, environment):
    log = logging.getLogger(__name__)
    if "event_split" in argv:
        argv.pop(argv.index("event_split"))
    log.debug(f"Found argv: {argv}")
    # print(f"Found events: {events}")
    args = event_split.parser.parse_args(argv)
    split_field = args.split_field
    log.debug(f"Found split_field: {split_field}")
    # if isinstance(events, QuerySet):
    #     events = list(events.values())
    log.debug("Resolving events")
    events = resolve(events)
    log.debug("Successfully resolved events")
    for event in events:
        item = event
        log.debug(f"Resolving split_field: {split_field}")
        for segment in split_field.split("__"):
            log.debug(f"Found segment: {segment}")
            try:
                item = item[segment]
                log.debug("Found value: {item}")
            except KeyError:
                log.debug(f"segment {segment} missing from item: {item}")
                item = None
        if isinstance(item, list):
            for element in item:
                _event = event.copy()
                _event[split_field] = element
                yield _event
        elif isinstance(item, dict):
            for key, element in item.items():
                _event = event.copy()
                _event[split_field] = element
                _event[f"{split_field}_key"] = key
                yield _event
        else:
            log.warning(f"Expected list for split field ({split_field}) for event. Got {item}, this event will be kept unchanged.")
            yield event

