# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

"""Tests for the read_file search command."""

from typing import Any
from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from events.models import FileUpload, Query


class ReadFileTests(APITestCase):
    """Validate CSV parsing behavior for ``read_file`` command."""

    def setUp(self, *args: Any, **kwargs: Any) -> None:
        """Create a test user for query execution and file ownership."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testuser",
        )
        self.user.save()
        super().setUp(*args, **kwargs)

    def test_read_file_csv_strips_spaced_quoted_headers_and_values(self) -> None:
        """CSV parsing should normalize quoted headers and space-padded values."""
        csv_content = "\n".join(
            [
                '"LatD", "LatM", "LatS", "NS", "LonD", "LonM", "LonS", "EW", "City", "State"',
                '   41,    5,   59, "N",     80,   39,    0, "W", "Youngstown", OH',
                '   43,   37,   48, "N",     89,   46,   11, "W", "Wisconsin Dells", WI',
            ]
        )
        file_upload = FileUpload.objects.create(
            title="cities.csv",
            content=ContentFile(csv_content, name="cities.csv"),
            user=self.user,
        )

        query = Query(
            name="read csv",
            text="read_file cities.csv --parse csv",
            user=self.user,
        )
        results = query.resolve(request=MagicMock(user=self.user))

        self.assertEqual(file_upload.title, "cities.csv")
        self.assertEqual(len(results), 2)

        first_row = results[0]
        self.assertEqual(first_row["LatD"], "41")
        self.assertEqual(first_row["LatM"], "5")
        self.assertEqual(first_row["NS"], "N")
        self.assertEqual(first_row["City"], "Youngstown")
        self.assertEqual(first_row["State"], "OH")

        second_row = results[1]
        self.assertEqual(second_row["City"], "Wisconsin Dells")
        self.assertEqual(second_row["State"], "WI")
        self.assertNotIn('"LatD"', second_row)
        self.assertNotIn(' "LatM"', second_row)
