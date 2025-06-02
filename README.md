# Delve - Enterprise Data Analytics Platform

**NOTICE**: Delve is in Alpha pre-release. Please try it out and provide feedback of any issues or missing features you encounter, but production use is discouraged at the moment.

## License

Delve is licensed under the GNU Affero General Public License v3 (AGPL-3.0).

This means:
- You are free to use, modify, and distribute this software, provided that any network-accessible modifications are also made available under the same license.
- The full license text is available in the [LICENSE](./LICENSE) file and at [https://www.gnu.org/licenses/agpl-3.0.html](https://www.gnu.org/licenses/agpl-3.0.html).

If you deploy a modified version of Delve on a server and allow users to interact with it over a network, you must also make the source code of your modified version available to those users.

For more information, see the [GNU AGPL FAQ](https://www.gnu.org/licenses/agpl-3.0-faq.html).

Please use the Issues section of this repository for feature requests, bug reports, and general feedback.

## Overview

Delve is an enterprise-grade platform for ingesting, analyzing, and deriving insights from any data source. Key capabilities include:

- **Data Integration**
  - REST API endpoints
  - Syslog receiver (UDP/TCP/TLS)
  - File monitoring and ingestion
  - Direct uploads
  
- **Analysis & Visualization**
  - Interactive search interface
  - Pipeline-based query language
  - Custom dashboards
  - Real-time alerts
  
- **Enterprise Features**
  - Role-based access control
  - Custom app development
  - API-first architecture
  - Extensible search commands
  - Scheduled tasks and automation

# Installation

1. Download one of the pre-built zip files from the [releases page](https://github.com/DelveCorp/delve/releases/).
2. Unzip the file in the desired location.
3. That's it!

# Initial Setup

After installation, setup can be as simple or as complex as you need.

The simplest setup involves using the default settings. The default settings are designed to be most useful to someone who is looking to quickly ingest some data (like log files or a REST API) and would like to search, transform, correlate, store, or otherwise interact with that data.

This use-case can be quite handy if you need to quickly troubleshoot an issue or would like to crawl a REST API for information.

To start using Delve with the simplest setup, use the following commands:

```bash
# Copy the example settings and urls files
cp ./delve/example-settings.py ./delve/settings.py
cp ./delve/example-urls.py ./delve/urls.py

# Create the database
./dl migrate

# Run the tests
./dl test

# Create an admin user
./dl createsuperuser

# Start serving the web UI
./dl serve

# In another window, you can start the task runner
./dl qcluster
```

## Documentation

- [Admin Manual](./src/home/doc/admin/index.md): Deployment, configuration, and system administration
- [User Manual](./src/home/doc/user/index.md): Search syntax, dashboards, and data analysis
- API Documentation: Available at `/api/docs` after installation

# Configuration

Configuration settings are located in `$DELVE_HOME/delve/settings.py`.

On a fresh install, there is no settings.py or urls.py. This is done to prevent overwriting a user's settings.py or urls.py if the install package is used as an update. So, if you are using the default configuration, you must copy the files `./delve/example-settings.py` and `./delve/example-urls.py` like in the command above. 

All Delve-specific settings are prefixed with `DELVE`.

The other settings in `settings.py` are specific to Django and the Django Rest Framework and can be found throughout the file.

# Development

In order to run Delve directly from the repo for development purposes,
use the following commands to perform standard tasks:

```bash
git clone $REPO_DIR    # TODO
cd delve

# Provision backend db, python requirements, etc
cd src
cd home

# Optionally, clear out old data
find . -type d -name __pycache__ -exec rm -fr {} ';'
rm -fr .venv
rm db.sqlite3
rm -fr staticfiles/*

# provision python venv, install Python dependencies and collect static assets
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r ..\..\windows-requirements.txt
python manage.py collectstatic --no-input

# Bundle frontend dependencies
cd ..
cd ..
npx webpack --config webpack.config.js
npx webpack --config dltable-webpack.config.js
npx webpack --config dlchart-webpack.config.js

# Copy frontend assets
mkdir src\home\staticfiles\js\
cp dist/staticfiles/dl-explore.js src/home/staticfiles/js/dl-explore.js
cp dist/staticfiles/dl-explore.js.LICENSE.txt src/home/staticfiles/js/dl-explore.js.LICENSE.txt

cp dist/staticfiles/dl-chart.js src/home/staticfiles/js/dl-chart.js
cp dist/staticfiles/dl-chart.js.LICENSE.txt src/home/staticfiles/js/dl-chart.js.LICENSE.txt

cp dist/staticfiles/dl-table.js src/home/staticfiles/js/dl-table.js
cp dist/staticfiles/dl-table.js.LICENSE.txt src/home/staticfiles/js/dl-table.js.LICENSE.txt

cp dist/main.css src/home/staticfiles/css/main.css
cp dist/*.woff src/home/staticfiles/css/
cp dist/*.woff2 src/home/staticfiles/css/

# Create database, admin user and start the server
cd src
cd home
python manage.py migrate
python manage.py createsuperuser
python manage.py serve
```
