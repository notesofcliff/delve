import logging
import argparse
from functools import wraps
from typing import Optional, List

import pydantic

def search_command(parser: argparse.ArgumentParser, input_validators: Optional[List[pydantic.BaseModel]]=None):
    def _decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            log = logging.getLogger(__name__)
            log.debug(f"Found args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            # log.debug(f"Found result: {result}")
            return result
        inner.parser = parser
        inner.input_validators = input_validators
        return inner
    return _decorator

