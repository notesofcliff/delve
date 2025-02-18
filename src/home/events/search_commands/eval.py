import logging
import argparse
import re


from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .util import cast
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="eval",
    description="Set the value of a field on each event."
)
parser.add_argument(
    "expressions",
    nargs="+",
    help="Provide one or more expressions to evaluate",
)

@search_command(parser)
def eval(request, events, argv, environment):
    log = logging.getLogger(__name__)
    events = resolve(events)
    log.info(f"Received argv: {argv}")
    args = eval.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")
    ret = []
    for event in events:
        log.debug(f"Found event: {event}")
        for expression in args.expressions:
            log.info(f"Found expression: {expression}")
            lhs, rhs = expression.split("=", 1)
            log.info(f"Found lhs, rhs: {lhs}, {rhs}")
            if rhs.startswith("$"):
                rhs_symbol = rhs.replace("$", "")
                if rhs_symbol in event:
                    event[lhs] = cast(event[rhs_symbol])
                else:
                    event[lhs] = cast(rhs)    
            else:
                event[lhs] = cast(rhs)
        yield event
