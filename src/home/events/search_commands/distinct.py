import argparse
import logging
from collections import defaultdict

from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="distinct",
    description="Return one event with fields containing the unique values "
                "of the specified fields.",
)
parser.add_argument(
    nargs="+",
    dest="fields",
)

@search_command(parser)
def distinct(request, events, argv, environment):
    events = resolve(events)
    args = distinct.parser.parse_args(argv[1:])
    logging.debug(f"Found args: {args}")
    ret_dict = defaultdict(set)
    for event in events:
        for field in args.fields:
            item = event
            for segment in field.split("__"):
                try:
                    item = item[segment]
                except KeyError:
                    item = None
            if item is not None:
                ret_dict[field].add(item)
    return [{
        key: list(value)
        for key, value in ret_dict.items()
    }]
