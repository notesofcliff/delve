import argparse
import logging

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .util import cast
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="set",
    description="Set environment variables."
)
parser.add_argument(
    nargs="+",
    dest="expressions",
)

@search_command(parser)
def set(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.debug(f"Found events: {events}")
    args = set.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")
    for expression in args.expressions:
        log.debug(f"Found expression: {expression}")
        key, value = expression.split("=", 1)
        log.debug(f"Found key, value: {key}, {value}")
        environment[key] = cast(value)
    return events
