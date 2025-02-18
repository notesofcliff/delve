"""Issue an HTTP request to retrieve data
"""
from urllib.parse import urlparse
import datetime
import argparse
import logging
import json 

from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings

import requests

from .decorators import search_command
from events.models import Event

parser = argparse.ArgumentParser(
    prog="request",
    description="Make an HTTP request."
)
parser.add_argument(
    "method",
    default="GET",
    choices=(
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ),
    help="The method for the request. (default GET)"
)
parser.add_argument(
    "url",
    help="The url to send http request",
)
parser.add_argument(
    "--username",
    help="The user name to use for auth",
)
parser.add_argument(
    "--password",
    help="The password to use for auth"
)
parser.add_argument(
    "--kv-pairs",
    action="append",
    help="Add key-value pair to the querystring for GET "
            "requests and application/x-www-form-urlencoded for "
            "POST, PATCH and PUT requests. unless --json is passed, "
            "in which case application/json will be used",
)
parser.add_argument(
    "--json",
    action="store_true",
    help="If sending POST, PUT or PATCH requests, encode any key-value "
            "pair in the request body as json",
)
parser.add_argument(
    "--save-event",
    action="store_true",
    help="If specified, an event will be saved with the result of the request.",
)
parser.add_argument(
    "--extract-fields",
    action="store_true",
    help="If specified, fields will be extracted from events regardless of "
         "whether event was saved",
)
parser.add_argument(
    "--recent-ok",
    action="store_true",
    help="If specified, the latest event from the same user, host, uri and method "
         "will be returned as long as it is not older than the number of minutes "
         "specified by --recent-minutes",
)
parser.add_argument(
    "--recent-minutes",
    type=int,
    default=5,
    help="The max age, in minutes, for an event to be considered recent",
)
parser.add_argument(
    "-H",
    "--headers",
    action="append",
    help="Provide HTTP headers for the request, can be specified multiple times",
)
parser.add_argument(
    "-n",
    "--no-verify",
    action="store_true",
)

@search_command(parser)
def make_request(request, events, argv, environment ):
    log = logging.getLogger(__name__)

    # WARNING: argv may contain credentials DO NOT LOG
    # The log statements commented out below should not be 
    # uncommented under any circumstances, but can be of limited use
    # when debugging in a controlled environment
    log.debug(f"Received {len(argv)} items in argv")
    # log.debug(f"Received argv: {argv}")
    if "request" in argv:
        argv.pop(argv.index("request"))
    args = make_request.parser.parse_args(argv)
    # log.debug(f"Parsed args: {args}")
    headers = args.headers
    # log.debug(f"Found headers: {headers}")
    if headers:
        headers = {i.split('=', 1)[0]: i.split('=', 1)[1] for i in args.headers}
    else:
        headers = {}        
    # log.debug(f"Parsed headers: {headers}")
    body = {}
    if args.kv_pairs:
        log.debug(f"Found kv_pairs: {args.kv_pairs}")
        for kv_pair in args.kv_pairs:
            log.debug(f"Found kv_pair: {kv_pair}")
            key, value = kv_pair.split("=", 1)
            log.debug(f"Found key, value: {key}, {value}")
            body[key] = value

    kwargs = {
        "method": args.method,
        "url": args.url,
        "headers": headers,
        "verify": not args.no_verify,
    }
    log.debug(f"Built request kwargs: {kwargs}")
    # Warning DO NOT LOG kwargs AFTER THIS POINT
    if args.username and args.password:
        log.debug(f"Adding auth for {args.username}")
        kwargs.update(
            {
                "auth": (args.username, args.password),
            }
        )
    if body:
        if args.method == "GET":
            log.debug("Updating params")
            kwargs.update(
                {
                    "params": body
                }
            )
        elif args.method in ["POST", "PUT", "PATCH"]:
            if args.json:
                log.debug("Updating json body")
                kwargs.update(
                    {
                        "json": body,
                    }
                )
            else:
                log.debug("Updating body")
                kwargs.update(
                    {
                        "data": body,
                    }
                )

    parsed_url = urlparse(kwargs["url"])
    if args.recent_ok:
        events = Event.objects.filter(
            index="http.request",
            host=parsed_url.netloc,
            source=parsed_url.path,
            user=request.user,
            created__gt=timezone.now()-datetime.timedelta(minutes=args.recent_minutes)
        )
        if events.exists():
            event = events.order_by("-created").first()
            return [event]

    log.debug("Sending request")
    response = requests.request(**kwargs)
    log.debug(f"Received response: {response}")
    response_json = None
    event = None
    try:
        log.debug(f"Attempting to parse response as json")
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        log.debug("Json parsing failed, using text")
        event = Event(
            index="http.request",
            host=parsed_url.netloc,
            source=parsed_url.path,
            sourcetype="text",
            text=response.text,
            user=request.user,
        )
        if args.save_event:
            event.save()
        elif args.extract_fields:
            event.extract_fields()
        return [event]
    # if isinstance(response_json, list):
    #     log.debug(f"response_json is list, yielding items from the list")
    #     for item in response_json:
    #         log.debug(f"yielding item: {item}")
    #         if args.save_event:
    #             event = Event.objects.create(
    #                 index="http.request",
    #                 host="localhost",
    #                 source=kwargs["url"],
    #                 sourcetype="json",
    #                 text=json.dumps(item),
    #                 user=request.user,
    #             )
    #         yield item
    if response_json is None:
        log.debug(f"Found response_json to be empty")
        event = Event(
            index="http.request",
            host=parsed_url.netloc,
            source=parsed_url.path,
            sourcetype="text",
            text=response.text,
            user=request.user,
            extracted_fields={"status_code": response.status_code}
        )
        if args.save_event:
            event.save()
        elif args.extract_fields:
            event.extract_fields()
        return [event]
    else:
        log.debug(f"response_json found to be list, dict, scalar or other. Will yield as one unit")
        event = Event(
            index="http.request",
            host=parsed_url.netloc,
            source=parsed_url.path,
            sourcetype="json",
            text=json.dumps(response_json),
            user=request.user,
            extracted_fields={"status_code": response.status_code},
        )
        if args.save_event:
            event.save()
        elif args.extract_fields:
            event.extract_fields()
        return [event]
    # if event is None:
    #     pass
    # else:
    #     changed = False
    #     if settings.FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE:
    #         changed = True
    #         event.extract_fields()
    #     if settings.FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE:
    #         changed = True
    #         event.process()
    #     if changed:
    #         event.save()

