# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

import argparse
import json
import csv
from typing import Any

import xmltodict

from events.models import (
    FileUpload,
)

from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="read_file",
    description="Read an uploaded file in as events.",
)
parser.add_argument(
    "filename",
    help="The uploaded file to read in.",
)
parser.add_argument(
    "--allow-escape",
    action="store_true",
    help="Allow automatic escaping file contents. ",
)
csv_choices = [f"csv:{dialect}" for dialect in csv.list_dialects()]
csv_choices.extend(["csv", "json", "jsonl", "xml"])
csv_choices = tuple(csv_choices)
parser.add_argument(
    "--parse",
    choices=csv_choices,
    help="If specified, must be a supported option. File contents "
         "will be parsed according to the format specified.",
)


def _normalize_csv_cell(value: Any) -> Any:
    """Normalize CSV cell values by trimming whitespace and surrounding quotes.

    Args:
        value: The parsed CSV cell value.

    Returns:
        The normalized cell value. Non-string values are returned unchanged.
    """
    if not isinstance(value, str):
        return value

    stripped = value.strip()
    stripped = stripped.strip('"').strip("'")
    return stripped


def _normalize_csv_row(row: dict[str, Any]) -> dict[str, Any]:
    """Normalize a CSV row by cleaning column names and cell values.

    Args:
        row: The row dictionary produced by ``csv.DictReader``.

    Returns:
        A normalized row with stripped keys and cleaned values.
    """
    normalized_row: dict[str, Any] = {}
    for key, value in row.items():
        normalized_key = _normalize_csv_cell(key)
        if normalized_key is None:
            continue
        normalized_row[normalized_key] = _normalize_csv_cell(value)
    return normalized_row

@search_command(parser)
def read_file(request, events, argv, environment):
    # import magic
    if events:
        raise ValueError("read_file must be the first search command")
    args = read_file.parser.parse_args(argv[1:])
    filename = args.filename
    file_object = FileUpload.objects.get(
        user=request.user,
        title=filename,
    )

    if args.parse:
        _format = args.parse
        if _format.startswith("csv"):
            try:
                dialect = _format.split(":", 1)[1]
            except IndexError:
                dialect = "excel"
            with file_object.content.open("r") as f:
                reader = csv.DictReader(f, dialect=dialect, skipinitialspace=True)
                for row in reader:
                    normalized_row = _normalize_csv_row(row)
                    yield {
                        "title": file_object.title,
                        "url": file_object.content.url,
                    **normalized_row
                }
        elif _format == "json":
            content = json.load(file_object.content)
            if isinstance(content, (str, int, dict)):
                yield {
                    "title": file_object.title,
                    "url": file_object.content.url,
                    "content": content,
                }
            else:
                for item in content:
                    yield {
                        "title": file_object.title,
                        "url": file_object.content.url,
                        **item
                    }
        elif _format == "jsonl":
            import json
            for line in file_object.content:
                try:
                    content = json.loads(line)
                except:
                    if args.allow_escape:
                        try:
                            content = json.loads(line.replace("\\", "\\\\"))
                        except:
                            content = [line.decode()]
                    else:
                        content = [line.decode()]
                if isinstance(content, (str, int, dict)):
                    yield {
                        "title": file_object.title,
                        "url": file_object.content.url,
                        "content": content,
                    }
                else:
                    for item in content:
                        yield {
                            "title": file_object.title,
                            "url": file_object.content.url,
                            'content': item,
                        }
        elif _format == "xml":
            dict_repr = xmltodict.parse(file_object.content, process_namespaces=False)
            yield json.loads(json.dumps(dict_repr))
        else:
            raise ValueError(f"Format {_format} is unsupported.")
    else:
        yield {
            "title": file_object.title,
            "url": file_object.content.url,
            "content": list(file_object.content),
        }
