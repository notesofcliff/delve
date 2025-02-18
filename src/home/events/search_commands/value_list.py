import argparse
import logging 

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve
from events.models import (
    Query,
    Event,
)

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="value_list",
    description="Reduce the result set to include the values from a given field",
)
parser.add_argument(
    "field",
    # nargs="+",
    help="The fields to extract the values from",
)

@search_command(parser)
def value_list(request, events, argv, environment):
    log = logging.getLogger(__name__)
    args = value_list.parser.parse_args(argv[1:])
    log.info(f"Found args: {args}")
    events = resolve(events)

    for event in events:
        ret = event.get(args.field, "")
        log.info(f"Found ret: {ret}")
        yield ret
