from itertools import groupby
from operator import itemgetter
from statistics import mean

from events.util import resolve
from events.search_commands.util import cast

def add_avg_parser_arguments(avg_parser):
    avg_parser.add_argument(
        "--by",
        nargs="+",
        help="If specified, the average returned will be by the specified field",
    )
    avg_parser.add_argument(
        "--as-field",
        default="avg",
        help="If specified, the average will be stored as the specified field",
    )
    avg_parser.add_argument(
        "field",
        help="The field to average",
    )

def avg(events, args, environment):
    events = resolve(events)
    if args.by:
        ret = []
        events.sort(key=itemgetter(*args.by))
        for key, event_group in groupby(events, key=itemgetter(*args.by)):
            event_group = list(event_group)
            average = mean((event.get(args.field) for event in event_group))
            for event in event_group:
                ret.append(
                    {args.as_field: average, **event}
                )
        return ret
    else:
        average = mean((event.get(args.field) for event in events))
        return [{args.as_field: average, **event} for event in events]

