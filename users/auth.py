# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

"""
Keycloak OIDC authentication backend for Delve.

Extends mozilla-django-oidc's ``OIDCAuthenticationBackend`` to map the Keycloak
``groups`` claim onto Django's ``is_staff`` / ``is_superuser`` flags and to keep
the user's Django group membership in sync with the claim. This is only wired in
when ``DELVE_OIDC_ENABLED`` is truthy (see ``delve/settings.py``); ModelBackend
remains the fallback so a local superuser still works.

Group → role mapping (armory shared-realm convention):
  armory-admins    → superuser (is_superuser + is_staff)
  armory-operators → staff     (is_staff)
  armory-viewers   → read-only (no admin access)
"""

from django.conf import settings
from django.contrib.auth.models import Group
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class DelveOIDCBackend(OIDCAuthenticationBackend):
    """Map Keycloak group membership to Delve/Django roles."""

    def _groups_from_claims(self, claims):
        """Return the list of group names from the configured groups claim."""
        claim = getattr(settings, 'DELVE_OIDC_GROUPS_CLAIM', 'groups')
        groups = claims.get(claim, []) or []
        if isinstance(groups, str):
            groups = [groups]
        # Keycloak group paths can be emitted as '/armory-admins'; normalize.
        return [g.lstrip('/') for g in groups]

    def _apply_role_mapping(self, user, claims):
        """Set is_staff/is_superuser and sync Django groups from the claim."""
        group_names = self._groups_from_claims(claims)

        admin_group = getattr(settings, 'DELVE_OIDC_ADMIN_GROUP', 'armory-admins')
        staff_group = getattr(settings, 'DELVE_OIDC_STAFF_GROUP', 'armory-operators')

        is_superuser = admin_group in group_names
        # Admins and operators both reach the Django admin; viewers do not.
        is_staff = is_superuser or (staff_group in group_names)

        changed = False
        if user.is_superuser != is_superuser:
            user.is_superuser = is_superuser
            changed = True
        if user.is_staff != is_staff:
            user.is_staff = is_staff
            changed = True
        if changed:
            user.save(update_fields=['is_superuser', 'is_staff'])

        # Mirror the OIDC groups into Django groups so per-object/permission
        # checks that key off group names keep working. Membership is fully
        # driven by the IdP each login (groups removed in Keycloak are removed
        # here too), but we never touch the local 'Users' group the signal adds.
        desired = [
            Group.objects.get_or_create(name=name)[0] for name in group_names
        ]
        managed_prefix_groups = user.groups.exclude(name='Users')
        user.groups.remove(*managed_prefix_groups)
        if desired:
            user.groups.add(*desired)

        return user

    def create_user(self, claims):
        user = super().create_user(claims)
        return self._apply_role_mapping(user, claims)

    def update_user(self, user, claims):
        user = super().update_user(user, claims)
        return self._apply_role_mapping(user, claims)
