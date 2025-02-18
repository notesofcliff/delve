import argparse
import logging

from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict

from .decorators import search_command
from events.util import resolve
from events.models import (
    BaseEvent,
)
from events.validators import (
    QuerySetOrListOfDictsOrEvents
)

parser = argparse.ArgumentParser(
    prog="drop_fields",
    description="Remove the specified fields from the result set.",
)
parser.add_argument(
    "fields",
    nargs="+",
    help="Field to drop if present from all events."
)

@search_command(
    parser,
    input_validators=[
        QuerySetOrListOfDictsOrEvents,
    ]
)
def drop_fields(request, events, argv, environment):
    args = drop_fields.parser.parse_args(argv[1:])
    log = logging.getLogger(__name__)
    fields = args.fields
    log.debug(f"Found fields: {fields}")
    events = resolve(events)

    for event in events:
        for field in fields:
            log.debug(f"Checking event for field: {field}")
            try:
                event.pop(field)
            except:
                pass
        yield event
