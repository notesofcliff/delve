---
title: Delve
---

# Delve

Delve is a powerful, extensible platform for ingesting, transforming, and
searching structured, unstructured, and semi-structured data. It is designed
for easy local development, robust production deployments, and seamless
integration with modern tools and containerization workflows.

## What Delve provides

- **Ingestion:** collect data from diverse sources — REST API, file tail,
  syslog, and scheduled queries.
- **Transformation:** normalize incoming data with custom pipelines and
  pluggable parsers.
- **Search:** a shell-pipeline-style query language filters, transforms, and
  aggregates events.
- **Dashboards:** build interactive dashboards and visualizations from saved
  searches.
- **Alerting:** trigger notifications from search results or as events are
  ingested.
- **Extensibility:** Delve apps are Django apps, so custom models, search
  commands, parsers, and processors extend the platform without forking it.

## Where to start

- New to Delve? Start with the [User Guide](user/index.md), beginning at
  [Getting Started](user/Getting_Started.md).
- Installing or operating a Delve deployment? See the
  [Admin Guide](admin/index.md), beginning at
  [Installation and Setup](admin/Installation_and_Setup.md).
- Building a custom Delve app, search command, or parser? See the
  [App Developer Guide](user/App_Developer_Guide.md) and the
  [Python API reference](reference/python-api.md).

## License

Delve is licensed under the GNU Affero General Public License v3.0
(AGPL-3.0). See the repository `LICENSE` file for details.
