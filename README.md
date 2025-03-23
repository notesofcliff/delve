# **IMPORTANT**

Flashlight is being released in a Public Alpha to guage user interest and to seek feedback on any requested features, bugs, use cases and custom apps being built.

You are free to use Flashlight for evaluation, development and even work during this public Alpha and the subsequent public Beta. When Flashlight reaches General Availability, you will need to purchase a license to use Flashlight. We will have individual plans starting at $20/month, larger Group plans starting at $50/month and larger Enterprise plans subject to negotiations.

Please use the Issues section of this repository to communicate with the project.

**Please Note** - The documentation is currently lacking. We are working on it. The documentation ships with Flashlight in the `doc` directory. It can also be found in this repository in `./src/home/doc`.

# Introduction

Flashlight is a versatile and powerful platform for ingesting, transforming, and searching through structured, unstructured, and semi-structured data. It allows for interactive searches, dashboards, alerts, and more.

# Documentation

For detailed documentation, please refer to the [Admin Manual](./src/home/doc/admin/index.md) or the [User Manual](./src/home/doc/user/index.md).

# Installation

1. Download one of the pre-built zip files from the [releases page](https://github.com/DelveCorp/flashlight/releases/).
2. Unzip the file in the desired location.
3. That's it!

# Initial Setup

After installation, setup can be as simple or as complex as you need.

The simplest setup involves using the default settings. The default settings are designed to be most useful to someone who is looking to quickly ingest some data (like log files or a REST API) and would like to search, transform, correlate, store, or otherwise interact with that data.

This use-case can be quite handy if you need to quickly troubleshoot an issue or would like to crawl a REST API for information.

To start using Flashlight with the simplest setup, use the following commands:

```bash
# Copy the example settings and urls files
cp ./flashlight/example-settings.py ./flashlight/settings.py
cp ./flashlight/example-urls.py ./flashlight/urls.py

# Create the database
./fl migrate

# Run the tests
./fl test

# Create an admin user
./fl createsuperuser

# Start serving the web UI
./fl serve

# In another window, you can start the task runner
./fl qcluster
```

# Configuration

Configuration settings are located in `$FLASHLIGHT_HOME/flashlight/settings.py`.

On a fresh install, there is no settings.py or urls.py. This is done to prevent overwriting a user's settings.py or urls.py if the install package is used as an update. So, if you are using the default configuration, you must copy the files `./flashlight/example-settings.py` and `./flashlight/example-urls.py` like in the command above. 

All Flashlight-specific settings are prefixed with `FLASHLIGHT`.

The other settings in `settings.py` are specific to Django and the Django Rest Framework and can be found throughout the file.

# Development

In order to run flashlight directly from the repo for development purposes,
use the following commands to start:

```bash
git clone $REPO_DIR    # TODO
cd flashlight

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
npx webpack --config fltable-webpack.config.js
npx webpack --config flchart-webpack.config.js

# Copy frontend assets
mkdir src\home\staticfiles\js\
cp dist/staticfiles/fl-explore.js src/home/staticfiles/js/fl-explore.js
cp dist/staticfiles/fl-explore.js.LICENSE.txt src/home/staticfiles/js/fl-explore.js.LICENSE.txt

cp dist/staticfiles/fl-chart.js src/home/staticfiles/js/fl-chart.js
cp dist/staticfiles/fl-chart.js.LICENSE.txt src/home/staticfiles/js/fl-chart.js.LICENSE.txt

cp dist/staticfiles/fl-table.js src/home/staticfiles/js/fl-table.js
cp dist/staticfiles/fl-table.js.LICENSE.txt src/home/staticfiles/js/fl-table.js.LICENSE.txt

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

