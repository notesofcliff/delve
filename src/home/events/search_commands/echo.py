import argparse
import logging

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .util import cast

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="echo",
    description="Return the given expressionsn as an event appended to the result set."
)
parser.add_argument(
    nargs="+",
    dest="expressions",
)

@search_command(parser)
def echo(request, events, argv, environment):
    log = logging.getLogger(__name__)
    args = echo.parser.parse_args(argv[1:])
    log.debug(f"Fount environment: {environment}")
    ret = []
    for expression in args.expressions:
        # expression = expression.format(**environment)
        log.debug(f"Found expression: {type(expression)}({expression})")
        ret.append(
            {
                "expression": expression,
            }
        )
    for event in events:
        yield event
    for item in ret:
        yield item