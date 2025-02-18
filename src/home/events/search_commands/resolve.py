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

from events.util import resolve as resolve_events
# from .util import cast
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="resolve",
    description="Resolve the result set. This will unwrap any "
                "generators or QuerySets.",
)

@search_command(parser)
def resolve(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.info(f"Received argv: {argv}")
    args = resolve.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")
    events = resolve_events(events)
    return events
