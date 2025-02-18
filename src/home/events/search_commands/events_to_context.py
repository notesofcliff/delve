import sys
import logging
import argparse
import inspect
import traceback
from types import GeneratorType
from itertools import chain
from io import StringIO

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

# from .util import cast
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="events_to_context",
    description="Put the current result set into the local "
                "context for use in jinja templating.",
)
parser.add_argument(
    "-z", "--return-empty",
    action="store_true",
    help="If specified, events received will be loaded into "
         "the local context and an empty list will be returned. "
         "By default, events received will be returned after "
         "processing."
)

@search_command(parser)
def events_to_context(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.info(f"Received argv: {argv}")
    args = events_to_context.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")
    events = resolve(events)
    environment["events"] = events
    if args.return_empty:
        return []
    return events

