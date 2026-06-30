# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

"""Ship Keycloak Tier-1 audit events into Delve via a scheduled DB query.

Reads the Keycloak ``event_entity`` (login/user events) and
``admin_event_entity`` (admin operations) tables directly — structured rows,
not parsed stdout — and POSTs new rows to Delve's ``/api/events/`` endpoint.

Why a DB query rather than tailing ``jboss-logging`` stdout: the rows are
already structured, and the table carries a monotonic ``event_time`` we can use
as a durable high-water mark. A cursor (per table: last ``event_time`` + ``id``
tie-break) is persisted to ``--cursor-file`` and advanced after each successful
ship, so restarts/reschedules neither re-ingest nor skip. On first run with no
cursor we start from "now" to avoid backfilling the entire history.

Auth mirrors tail-files.py: a Keycloak ``delve-ingest`` client-credentials
bearer token, fetched lazily and refreshed before expiry.

Intended to run from the Delve image (psycopg2 + requests are already present).
"""

import os
import sys
import json
import time
import logging
import argparse
import threading

import requests
import psycopg2
import psycopg2.extras

log = logging.getLogger("keycloak-events")

# (table, time-column, source label). Both ship under sourcetype keycloak_event.
TABLES = (
    ("event_entity", "event_time", "keycloak_event_entity"),
    ("admin_event_entity", "admin_event_time", "keycloak_admin_event_entity"),
)


class ClientCredentialsAuth(requests.auth.AuthBase):
    """Attach a refreshed Keycloak client-credentials bearer token (see tail-files.py)."""

    def __init__(self, token_url, client_id, client_secret, verify=True, leeway=30):
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._verify = verify
        self._leeway = leeway
        self._lock = threading.Lock()
        self._token = None
        self._expiry = 0.0

    def _fetch(self):
        response = requests.post(
            self._token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
            verify=self._verify,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        self._token = payload["access_token"]
        self._expiry = time.time() + float(payload.get("expires_in", 60))

    def __call__(self, request):
        with self._lock:
            if not self._token or time.time() >= (self._expiry - self._leeway):
                self._fetch()
            token = self._token
        request.headers["Authorization"] = f"Bearer {token}"
        return request


def parse_argv(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    # Delve target.
    parser.add_argument("--server", default=os.environ.get("DELVE_SERVER", "http://localhost:8000"),
                        help="Delve scheme/host/port, e.g. https://delve.armory.local")
    parser.add_argument("--index", default=os.environ.get("DELVE_KC_INDEX", "keycloak"))
    parser.add_argument("--sourcetype", default=os.environ.get("DELVE_KC_SOURCETYPE", "keycloak_event"))
    parser.add_argument("--host", default=os.environ.get("DELVE_KC_HOST", "keycloak"),
                        help="The host value associated with shipped events.")
    parser.add_argument("--ca-file", default=os.environ.get("DELVE_INGEST_CA_FILE") or None,
                        help="CA bundle to verify TLS for Delve and the token endpoint.")
    parser.add_argument("--no-verify", action="store_true",
                        help="Disable TLS verification (development only).")
    # Bearer auth.
    parser.add_argument("--token-url", default=os.environ.get("DELVE_INGEST_TOKEN_URL"))
    parser.add_argument("--client-id", default=os.environ.get("DELVE_INGEST_CLIENT_ID"))
    parser.add_argument("--client-secret", default=os.environ.get("DELVE_INGEST_CLIENT_SECRET"))
    # Keycloak DB.
    parser.add_argument("--db-host", default=os.environ.get("DELVE_KC_DB_HOST"))
    parser.add_argument("--db-port", default=os.environ.get("DELVE_KC_DB_PORT", "5432"))
    parser.add_argument("--db-name", default=os.environ.get("DELVE_KC_DB_NAME", "keycloak"))
    parser.add_argument("--db-user", default=os.environ.get("DELVE_KC_DB_USER"))
    parser.add_argument("--db-password", default=os.environ.get("DELVE_KC_DB_PASSWORD"))
    parser.add_argument("--db-sslmode", default=os.environ.get("DELVE_KC_DB_SSLMODE", "prefer"))
    # Cursor + scheduling.
    parser.add_argument("--cursor-file", default=os.environ.get("DELVE_KC_CURSOR_FILE", "/var/lib/delve-keycloak/cursor.json"),
                        help="Persisted high-water mark; must live on durable storage.")
    parser.add_argument("--interval", type=int, default=int(os.environ.get("DELVE_KC_INTERVAL", "30")),
                        help="Seconds between polls. 0 runs a single pass and exits.")
    parser.add_argument("--batch-size", type=int, default=int(os.environ.get("DELVE_KC_BATCH", "500")))
    parser.add_argument("-v", "--verbose", action="count", default=0)
    return parser.parse_args(argv)


def load_cursor(path):
    try:
        with open(path, "r") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return {}
    except (ValueError, OSError) as exc:
        log.warning("Could not read cursor file %s (%s); starting fresh.", path, exc)
        return {}


def save_cursor(path, cursor):
    # Write-then-rename so a crash mid-write can't corrupt the cursor.
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    tmp = f"{path}.tmp"
    with open(tmp, "w") as handle:
        json.dump(cursor, handle)
    os.replace(tmp, path)


def fetch_new_rows(conn, table, time_col, last_time, last_id, batch_size):
    """Return rows strictly after (last_time, last_id), ordered for a stable cursor."""
    query = (
        f"SELECT * FROM {table} "
        f"WHERE {time_col} > %(t)s OR ({time_col} = %(t)s AND id > %(i)s) "
        f"ORDER BY {time_col} ASC, id ASC "
        f"LIMIT %(limit)s"
    )
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, {"t": last_time, "i": last_id, "limit": batch_size})
        return cur.fetchall()


def post_batch(session, url, events):
    response = session.post(url, json=events, timeout=60)
    response.raise_for_status()
    return response


def ship_table(conn, session, url, args, cursor, table, time_col, source):
    state = cursor.get(table) or {}
    last_time = state.get("time", args._start_time)
    last_id = state.get("id", "")
    total = 0
    while True:
        rows = fetch_new_rows(conn, table, time_col, last_time, last_id, args.batch_size)
        if not rows:
            break
        events = [
            {
                "index": args.index,
                "host": args.host,
                "source": source,
                "sourcetype": args.sourcetype,
                # psycopg2.extras.Json default handles datetimes/Decimals safely.
                "text": json.dumps(row, default=str),
            }
            for row in rows
        ]
        post_batch(session, url, events)
        # Advance the cursor only after Delve has accepted the batch.
        last_time = rows[-1][time_col]
        last_id = rows[-1]["id"]
        cursor[table] = {"time": last_time, "id": last_id}
        save_cursor(args.cursor_file, cursor)
        total += len(rows)
        if len(rows) < args.batch_size:
            break
    if total:
        log.info("Shipped %d rows from %s (cursor now time=%s id=%s).", total, table, last_time, last_id)
    return total


def build_session(args):
    if args.no_verify:
        verify = False
    elif args.ca_file:
        verify = args.ca_file
    else:
        verify = True
    missing = [name for name, value in (
        ("--token-url", args.token_url),
        ("--client-id", args.client_id),
        ("--client-secret", args.client_secret),
    ) if not value]
    if missing:
        raise ValueError(f"bearer auth requires: {', '.join(missing)}")
    session = requests.Session()
    session.verify = verify
    session.auth = ClientCredentialsAuth(
        token_url=args.token_url,
        client_id=args.client_id,
        client_secret=args.client_secret,
        verify=verify,
    )
    return session


def main(argv=None):
    args = parse_argv(sys.argv[1:] if argv is None else argv)
    logging.basicConfig(
        level=max(logging.DEBUG, logging.WARNING - args.verbose * 10),
        format="%(levelname)s %(name)s %(message)s",
    )
    for required in ("db_host", "db_user", "db_password"):
        if not getattr(args, required):
            raise ValueError(f"missing required DB setting: --{required.replace('_', '-')}")

    # First-run high-water mark: start from "now" (epoch millis) so we ship only
    # new events, never the whole table. Keycloak stores *_time as epoch millis.
    args._start_time = int(time.time() * 1000)

    url = f"{args.server}/api/events/"
    session = build_session(args)

    while True:
        cursor = load_cursor(args.cursor_file)
        try:
            conn = psycopg2.connect(
                host=args.db_host, port=args.db_port, dbname=args.db_name,
                user=args.db_user, password=args.db_password, sslmode=args.db_sslmode,
            )
            conn.set_session(readonly=True, autocommit=True)
            try:
                for table, time_col, source in TABLES:
                    ship_table(conn, session, url, args, cursor, table, time_col, source)
            finally:
                conn.close()
        except Exception:
            log.exception("Keycloak event ship pass failed; will retry next interval.")
        if args.interval <= 0:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        logging.getLogger("keycloak-events").exception("Fatal error")
        sys.exit(1)
