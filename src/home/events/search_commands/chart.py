import logging
import argparse
from itertools import (
    groupby
)

from django.db.models.query import QuerySet

from events.validators import ListOfDicts
from events.util import resolve

# from .util import ensure_list
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="chart",
    description="Return the JSON data to configure a Chart.js chart.",
)
parser.add_argument(
    "-t",
    "--type",
    default="bar",
    choices=(
        "bar",
        "line",
    ),
    help="The type of chart to make",
)
parser.add_argument(
    "-x",
    "--x-field",
    help="The field to plot on the X axis"
)
parser.add_argument(
    "-y",
    "--y-field",
    help="The field to plot on the Y axis"
)
parser.add_argument(
    "-b",
    "--by-field",
    help="The field to split into series",
)
parser.add_argument(
    "--time-x",
    choices=(
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "quarter",
        "year",
    ),
    help="If specified, the data of the x axis will be treated as time"
)

@search_command(
    parser,
    input_validators=[
        ListOfDicts,
    ]
)
def chart(request, events, argv, environment):
    log = logging.getLogger(__name__)
    log.info("In search_command chart")
    args = chart.parser.parse_args(argv[1:])
    events = resolve(events)

    if args.by_field is not None:
        log.debug(f"Found by_field: {args.by_field}")
        datasets = []
        log.debug(f"sorting events by by_field")
        events.sort(
            key=lambda x: x[args.by_field]
        )
        log.debug(f"Grouping by: {args.by_field}")
        for label, data_list in groupby(events, lambda x: x[args.by_field]):
            log.debug(f"Appending data for {label}")
            datasets.append(
                {
                    "label": label,
                    "data": [
                        {
                            args.x_field: data.get(args.x_field),
                            args.y_field: data.get(args.y_field),
                        } for data in data_list
                    ],
                }
            )
        log.debug("Done grouping data")
        data = {"datasets": datasets}
    else:
        log.debug("args.by_field is None")
        data = {
            "labels": [event[args.x_field] for event in events],
            "datasets": [
                {
                    "label": args.y_field,
                    "data": events,
                }
            ]
        }
    log.debug(f"Building response")
    ret = {
        "visualization": "chartjs",
        "type": args.type,
        "data": data,
        "options": {
            "plugins": {
                # "colors": {
                #     "forceOverride": True
                # }
           },
            "parsing": {
                "xAxisKey": args.x_field,
                "yAxisKey": args.y_field,
            },
        },
    }
    if args.time_x:
        log.debug(f"Found time_x: {args.time_x}")
        ret["options"]["scales"] = {
            "x": {
                "type": "time",
                "time": {
                    "unit": args.time_x,
                    "displayFormats": {
                        "minute": "MM-DD HH:mm:SS",
                        "hour":  "MM-DD HH",
                        "day": "YY-MM-DD",
                        "week": "YY-MM-DD",
                        "month": "YY-MM",
                        "quarter": "YY-MM",
                        "year": "yyyy",
                    },
                },
                "ticks": {
                    "source": "data"
                },
            },
        }
    return ret
