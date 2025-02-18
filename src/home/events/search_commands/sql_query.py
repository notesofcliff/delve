import logging
import argparse
import json
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

import records

from events.util import resolve

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="sql_query",
    description="Perform a SQL query against the specified database.",
)
parser.add_argument(
    "connection_string",
    help="The database connection string, "
         "(ie. mysql+pymysql://user:pass@some_mariadb/dbname)",
)
parser.add_argument(
    "sql_query",
    help="The SQL query to issue."
)
# parser.add_argument(
#     "params",
#     nargs="*",
#     help="The params to interpolate into query, should be in form of KEY=VALUE"
# )

@search_command(parser)
def sql_query(request, events, argv, environment):
    log = logging.getLogger(__name__)
    events = resolve(events)
    if events:
        raise ValueError(f"sql_query must be the first command in the Query")
    log.debug(f"Parsing args")
    args = sql_query.parser.parse_args(argv[1:])
    log.debug(f"Found sql query: '{args.sql_query}'")
    # params = {key: value for key, value in (param.split("=", 1) for param in args.params)}
    log.debug("Finished parsing args, connecting to database")
    db = records.Database(args.connection_string)
    log.debug("Querying the database")
    rows = db.query(args.sql_query)
    log.debug("returning results")
    return json.loads(rows.export('json') )
