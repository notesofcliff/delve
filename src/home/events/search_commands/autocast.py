import logging
import argparse
import re


from django.db.models.manager import Manager
from django.db.models.query import QuerySet


from .util import cast
from .decorators import search_command
from events.validators import QuerySetOrListOfDicts
from events.util import resolve

parser = argparse.ArgumentParser(
    prog="autocast",
    description="Attempt to cast fields to types based on their values."
)
parser.add_argument(
    "fields",
    nargs="*",
    help="Provide one or more fields to autocast",
)


# def resolve_field_lookup(expression, item):
#     log = logging.getLogger(__name__)
#     ret = item
#     log.info(f"Found ret: {ret}")
#     for subexpr in expression.split("__")[:-1]:
#         log.debug(f"ret: {ret}, subexpr: {subexpr}")
#         ret = ret[subexpr]
#         log.debug(f"Built ret: {ret}")
#     return ret

@search_command(
    parser,
    input_validators=[
        QuerySetOrListOfDicts,
    ],
)
def autocast(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.info("In search_command autocast")
    events = resolve(events)
    log.debug(f"Received argv: {argv}")
    if "autocast" in argv:
        argv.pop(argv.index("autocast"))
    args = autocast.parser.parse_args(argv)

    ret = []
    for event in events:
        log.debug(f"Found event: {event}")
        for field in args.fields:
            # lhs = left-hand side, rhs right-hand side
            log.debug(f"Found field: {type(field)}({field})")
            event[field] = cast(event[field])
            log.debug(f"New type of field: {type(field)}({field})")
        yield event
