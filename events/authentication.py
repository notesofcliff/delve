# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

"""
Bearer-JWT authentication for machine ingestion (Delve audit feeds).

A DRF ``BaseAuthentication`` that validates a Keycloak-issued access token
presented as ``Authorization: Bearer <jwt>``. The feed shippers obtain this
token from the ``delve-ingest`` client-credentials client and POST audit events
to ``ingress/``; this class is what lets those POSTs authenticate without a
browser session.

Design notes:
  * JWT/JWKS verification is NOT hand-rolled. We reuse mozilla-django-oidc's
    ``OIDCAuthenticationBackend`` (already a dependency for human SSO) to fetch
    and cache the realm JWKS, match the signing key, enforce that the token's
    ``alg`` equals the configured ``DELVE_INGEST_SIGN_ALGO`` (so ``alg=none`` is
    rejected), and verify the signature.
  * The OIDC backend's ``verify_token`` only checks the signature, so this class
    additionally enforces ``exp`` and that ``azp``/``aud`` names the
    ``delve-ingest`` audience — a token minted for a different client is
    rejected even if its signature is valid.
  * Entirely env-gated: when ``DELVE_INGEST_ENABLED`` is falsey ``authenticate``
    returns ``None`` immediately, preserving Delve's air-gapped default. The
    class can stay registered in ``DEFAULT_AUTHENTICATION_CLASSES`` unconditionally.
  * Returning ``None`` (rather than raising) for non-Bearer requests lets the
    existing Basic/Session authenticators handle interactive callers unchanged.
"""

import logging
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

log = logging.getLogger(__name__)


class _IngestTokenVerifier(OIDCAuthenticationBackend):
    """mozilla-django-oidc backend configured for the ``delve-ingest`` issuer.

    Reuses the library's JWKS retrieval + JWS signature verification, but reads
    its configuration from the ``DELVE_INGEST_*`` settings instead of the
    human-SSO ``OIDC_RP_*`` settings, so the machine path is independent of (and
    works without) human SSO.
    """

    def __init__(self):
        # Deliberately bypass super().__init__(): it eagerly reads the human-SSO
        # OIDC_OP_*/OIDC_RP_* settings and raises ImproperlyConfigured when they
        # are unset (i.e. when human SSO is off). The machine path needs only the
        # JWKS endpoint, the expected signing algorithm, and JWKS-based key
        # lookup — everything below.
        self.OIDC_OP_JWKS_ENDPOINT = settings.DELVE_INGEST_JWKS_URL
        self.OIDC_RP_SIGN_ALGO = settings.DELVE_INGEST_SIGN_ALGO
        # Audience the token must be for; also stands in for OIDC_RP_CLIENT_ID in
        # any library code path that references it.
        self.OIDC_RP_CLIENT_ID = settings.DELVE_INGEST_AUDIENCE
        # Force asymmetric JWKS verification: no shared secret, no preset key.
        self.OIDC_RP_CLIENT_SECRET = None
        self.OIDC_RP_IDP_SIGN_KEY = None

    def get_settings(self, attr, *args):
        # retrieve_matching_jwk() fetches the JWKS over HTTPS and reads
        # OIDC_VERIFY_SSL via get_settings(); point it at the ingest issuer CA so
        # the fetch is trusted independently of the human-SSO OIDC_VERIFY_SSL.
        if attr == 'OIDC_VERIFY_SSL':
            ca_file = getattr(settings, 'DELVE_INGEST_CA_FILE', '') or ''
            return ca_file if ca_file else True
        # Machine tokens have no nonce; never require one.
        if attr == 'OIDC_USE_NONCE':
            return False
        return OIDCAuthenticationBackend.get_settings(attr, *args)


class IngestJWTAuthentication(BaseAuthentication):
    """Authenticate ``Authorization: Bearer <keycloak-jwt>`` for ingestion."""

    keyword = b'bearer'

    def authenticate(self, request):
        if not getattr(settings, 'DELVE_INGEST_ENABLED', False):
            return None

        header = get_authorization_header(request).split()
        if not header or header[0].lower() != self.keyword:
            # Not a Bearer credential — defer to Basic/Session auth.
            return None
        if len(header) == 1:
            raise AuthenticationFailed('Invalid bearer header: no credentials provided.')
        if len(header) > 2:
            raise AuthenticationFailed('Invalid bearer header: token may not contain spaces.')

        token = header[1].decode('utf-8', 'replace')
        claims = self._verify(token)
        user = self._service_user()
        return (user, token)

    def authenticate_header(self, request):
        # Drives the WWW-Authenticate header so failures are 401, not 403.
        return 'Bearer realm="delve-ingest"'

    # -- verification ---------------------------------------------------------

    def _verify(self, token):
        verifier = _IngestTokenVerifier()
        try:
            claims = verifier.verify_token(token)
        except AuthenticationFailed:
            raise
        except Exception as exc:
            # SuspiciousOperation (bad alg / signature / JWKS), JWT decode
            # errors (incl. expired in PyJWT-backed builds), network errors, etc.
            log.warning('Delve ingest bearer-JWT verification failed: %s', exc)
            raise AuthenticationFailed('Bearer token verification failed.')

        if not isinstance(claims, dict):
            raise AuthenticationFailed('Bearer token has no claims.')

        self._check_audience(claims)
        self._check_expiry(claims)
        return claims

    def _check_audience(self, claims):
        expected = settings.DELVE_INGEST_AUDIENCE
        azp = claims.get('azp')
        aud = claims.get('aud', [])
        if isinstance(aud, str):
            aud = [aud]
        if azp != expected and expected not in aud:
            raise AuthenticationFailed('Bearer token azp/aud does not name delve-ingest.')

    def _check_expiry(self, claims):
        # mozilla-django-oidc's verify_token does not enforce exp (some builds
        # do via PyJWT, some don't), so enforce it here unconditionally.
        exp = claims.get('exp')
        if exp is None:
            raise AuthenticationFailed('Bearer token missing exp.')
        try:
            exp = float(exp)
        except (TypeError, ValueError):
            raise AuthenticationFailed('Bearer token has a malformed exp.')
        leeway = float(getattr(settings, 'DELVE_INGEST_LEEWAY', 30))
        now = datetime.now(tz=timezone.utc).timestamp()
        if exp + leeway < now:
            raise AuthenticationFailed('Bearer token has expired.')

    # -- identity -------------------------------------------------------------

    def _service_user(self):
        """Resolve (creating once) the local service user ingested events are
        attributed to. It is a plain active user — not staff/superuser — so it
        owns ``Event`` rows without granting any interactive privilege."""
        UserModel = get_user_model()
        username = getattr(settings, 'DELVE_INGEST_USERNAME', 'delve-ingest')
        user, _ = UserModel.objects.get_or_create(
            username=username,
            defaults={'is_active': True},
        )
        if not user.is_active:
            raise AuthenticationFailed('Ingest service user is disabled.')
        return user
