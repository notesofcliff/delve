import logging
import argparse
import re


from django.db.models.manager import Manager
from django.db.models.query import QuerySet


from .util import cast
from .decorators import search_command
from events.validators import QuerySetOrListOfDicts
from events.util import resolve

lookup_map = {
    "exact": lambda lhs, rhs: lhs == rhs,
    "iexact": lambda lhs, rhs: lhs.lower() == rhs.lower(),
    "contains": lambda lhs, rhs: rhs in lhs,
    "icontains": lambda lhs, rhs: rhs.lower() in lhs.lower(),
    "in": lambda lhs, rhs: lhs in rhs,
    "gt": lambda lhs, rhs: lhs > rhs,
    "gte": lambda lhs, rhs: lhs >= rhs,
    "lt": lambda lhs, rhs: lhs < rhs,
    "lte": lambda lhs, rhs: lhs <= rhs,
    "ne": lambda lhs, rhs: lhs != rhs,
    "eq": lambda lhs, rhs: lhs == rhs,
    "startswith": lambda lhs, rhs: lhs.startswith(rhs),
    "istartswith": lambda lhs, rhs: lhs.lower().startswith(rhs.lower()),
    "endswith": lambda lhs, rhs: lhs.endswith(rhs),
    "iendswith": lambda lhs, rhs: lhs.lower().endswith(rhs.lower),
    "isnull": lambda lhs, rhs: lhs is None if rhs is True else lhs is not None,
    "regex": lambda lhs, rhs: re.search(rhs, lhs),
    "iregex": lambda lhs, rhs: re.search(rhs, lhs, re.I),
    # "range": ,
    # "date": lambda
    # "year": lambda lhs, rhs: lhs.year,
    # "month": lambda lhs, rhs: lhs.month,
    # "day": lambda lhs, rhs: lhs.day,
    # "weekday": lambda lhs, rhs: lhs.weekday,
    # "hour": lambda lhs, rhs: lhs.hour,
    # "minute": lambda lhs, rhs: lhs.minute,
    # "second": lambda lhs, rhs: lhs.second,
}

def resolve_field_lookup(expression, item):
    log = logging.getLogger(__name__)
    if "__" not in expression or not expression.endswith(tuple([i for i in lookup_map.keys()])):
        log.debug(f"Found expression: {expression}, appending lookup.")
        expression = f"{expression}__exact"
        log.debug(f"Expression modified to: {expression}")
    ret = item
    log.debug(f"Found ret: {ret}")
    for subexpr in expression.split("__")[:-1]:
        log.debug(f"ret: {ret}, subexpr: {subexpr}")
        try:
            ret = ret[subexpr]
        except KeyError:
            ret = None
            continue
        log.debug(f"Built ret: {ret}")
    return expression.split("__")[-1], ret

parser = argparse.ArgumentParser(
    prog="filter",
    description="Reduce the result set by removing events that don't meet the specified criteria.",
)
parser.add_argument(
    "terms",
    nargs="*",
    help="Provide one or more search terms, "
            "must be in the form KEY=VALUE where key "
            "is a reference to a field and VALUE is the value. "
            "For KEY, django field lookups are (kind of) supported.",
)
parser.add_argument(
    "--no-cast",
    action="store_true",
    help="If specified, the value will not be cast to a type "
            "before completing the test",
)

@search_command(
    parser,
    # input_validators=[
    #     QuerySetOrListOfDicts,
    # ]
)
def filter(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.debug(f"Received {events} events")
    events = resolve(events)
    log.debug(f"Resolved events: {events}")
    # if isinstance(events, (Manager, QuerySet)):
    #     events = list(events.values())
    log.debug(f"Received argv: {argv}")
    if "filter" in argv:
        argv.pop(argv.index("filter"))
    args = filter.parser.parse_args(argv)
    log.debug(f"Found args: {args}")

    for event in events:
        log.debug(f"Found event: {event}")
        allowed = True
        for term in args.terms:
            # lhs = left-hand side, rhs right-hand side
            log.debug(f"Found term: {term}")
            expression, rhs = term.split("=")
            if expression.startswith("!"):
                negate = True
                expression = expression.lstrip("!")
            else:
                negate = False
            log.debug(f"Found expression: {expression}, rhs: {rhs}")
            predicate, lhs = resolve_field_lookup(expression=expression, item=event)
            log.debug(f"Found predicate: {predicate}, lhs: {lhs}")
            if predicate not in lookup_map:
                raise ValueError(f"Sorry, {predicate} is not a valid lookup, please choose one of {lookup_map.keys()}")
            predicate = lookup_map[predicate]
            log.debug(f"predicate resolved: {predicate}")

            if not args.no_cast:
                rhs = cast(rhs)
                log.debug(f"Cast rhs: {rhs} to {type(rhs)}")
            # lhs = cast(lhs)
            if negate:
                if predicate(lhs, rhs):
                    log.debug(f"negated {predicate}({lhs}, {rhs}) returned: {predicate(lhs, rhs)}")
                    allowed = False
                    break
            else:
                if not predicate(lhs, rhs):
                    log.debug(f"{predicate}({lhs}, {rhs}) returned: {predicate(lhs, rhs)}")
                    allowed = False
                    break
        if allowed:
            yield event
