import re
import argparse
import logging

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="rex",
    description="Use regular expressions to extract values from a field and store in extracted_fields",
)
parser.add_argument(
    "-f", "--field",
    default="text",
    help="The field to run the regular expression against"
)
parser.add_argument(
    nargs="+",
    dest="expressions",
)

@search_command(parser)
def rex(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.info("In search_command rex")
    events = resolve(events)
    args = rex.parser.parse_args(argv[1:])
    log.debug(f"Found args: {args}")
    expressions = [re.compile(expression) for expression in args.expressions]
    log.debug(f"found expressions: {expressions}")
    for event in events:
        log.debug(f"Found event: {event}")
        for expression in expressions:
            try:
                results = expression.search(event[args.field])
            except:
                results = expression.search(event[args.field].decode())
            log.debug(f"Found results: {results}")
            if results:
                event.update(results.groupdict())
        yield event
