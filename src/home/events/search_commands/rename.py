import argparse

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .decorators import search_command
from events.util import resolve

parser = argparse.ArgumentParser(
    prog="rename",
    description="Rename a field.",
)
parser.add_argument(
    "-f",
    "--from-field",
)
parser.add_argument(
    "-t",
    "--to-field",
)

@search_command(parser)
def rename(request, events, argv, environment):
    events = resolve(events)
    args = rename.parser.parse_args(argv[1:])
    for event in events:
        event[args.to_field] = event.pop(args.from_field)
        yield event
