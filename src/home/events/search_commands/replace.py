import re
import argparse

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="replace",
    description="Replace text matching a regular expression with a provided string.",
)
parser.add_argument(
    "-f",
    "--field",
)
parser.add_argument(
    "expression",
)
parser.add_argument(
    "replacement",
)

@search_command(parser)
def replace(request, events, argv, environment):
    events = resolve(events)
    args = replace.parser.parse_args(argv[1:])
    field = args.field
    expression = re.compile(args.expression)
    replacement = args.replacement
    for event in events:
        event[field] = expression.sub(replacement, event[field])
        yield event
