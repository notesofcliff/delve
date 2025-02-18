import argparse
import sys
import logging
import inspect
from itertools import chain
from types import GeneratorType
from io import StringIO


from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .util import cast
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="transpose",
    description="Invert the result set",
)

@search_command(parser)
def transpose(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.debug(f"Found events: {events}")
    if isinstance(events, QuerySet):
        log.debug(f"Casting matching events, detected {type(events)}")
        events = list(events.values())
    elif isinstance(events, GeneratorType) or inspect.isgeneratorfunction(events):
        log.debug(f"Casting matching events, detected {type(events)}({events})")
        log.debug("swapping stdout and stderr")
        orig_stderr = sys.stderr
        orig_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        try:
            events = list(events)
        except Exception as exception:
            log.critical(f"Unhandled exception occurred, {exception}")
            raise
        finally:
            log.debug("replacing original stdout and stderr")
            sys.stderr = orig_stderr
            sys.stdout = orig_stdout
    if not isinstance(events[0], dict):
        raise ValueError("Transpose only works for QuerySets and Lists of Dicts.")

    args = parser.parse_args(argv[1:])
    log.info(f"Found args: {args}")

    keys = set(chain.from_iterable(events))
    log.debug(f"Found keys: {keys}")
    for item in events:
        # Add None to fill any missing values
        if isinstance(item, dict):
            try:
                item.update({key: item.get(key, None) for key in keys})
            except:
                log.debug(f"Found item: {type(item)}({item})")
                raise
    ret = []
    for key in keys:
        item = {
            "key": key,
        }
        for index, value in enumerate([event.get(key) for event in events]):
            item[str(index)] = value
        ret.append(item)
    return ret