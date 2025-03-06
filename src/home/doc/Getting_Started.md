# Getting Started
## Overview
Flashlight is a versatile and powerful platform for ingesting, transforming, and searching through structured, unstructured, and semi-structured data. It allows for interactive searches, dashboards, alerts, and more.

## Key Features
- Ingest data from various sources
- Transform and normalize data
- Powerful search capabilities
- Interactive dashboards and visualizations
- Alerts and notifications
- Extensible and customizable

## Use Cases
- Log analysis and monitoring
- Data exploration and visualization
- Real-time alerting and notifications
- API data crawling and analysis
- Troubleshooting and debugging

## Project Goals
- Provide a user-friendly interface for data exploration
- Enable quick and efficient data ingestion and transformation
- Offer powerful search and filtering capabilities
- Support interactive and customizable dashboards
- Facilitate real-time alerting and notifications

## Installation
1. Download one of the pre-built zip files from the [releases page](#).
2. Unzip the file in the desired location.
3. Follow the setup instructions to get started.

## Quick Start Guide
To start using Flashlight with the simplest setup, use the following commands:

``` { .bash use_pygments=true noclasses=true pygments_style=github-dark  }
# Create settings and url files from the examples
cp ./flashlight/example-settings.py ./flashlight/settings.py
cp ./flashlight/example-urls.py ./flashlight/urls.py

# Run the tests
fl test

# Create the database
fl migrate

# Create an admin user
fl createsuperuser

# Start serving the web UI
fl serve

# Start the task scheduler
fl qcluster

# If you are on Windows, you can use the following command from the flashlight directory to install Flashlight supervisor service to handle the server, qcluster and other flashlight services (from an Administrator Command prompt).
./python/$PYTHON_VERSION/python ./service.py install
# After the service is installed, use Windows Services app to configure and start the service or optionally use the service.py command look at this command to see the options available
./python/$PYTHON_VERSION/python ./service.py /?
```

## Browsing the documentation

In your browser, go to `https://localhost:8000/docs/index` to see the documentation.

## Configuration
Most configuration is found in the flashlight settings.py file (`./flashlight/settings.py`).

Most of this configuration is [Django configuration](https://docs.djangoproject.com/en/5.1/topics/settings/)

Flashlight specific settings are prefixed with `FLASHLIGHT_` and here is quick reference a list of them:

* **FLASHLIGHT_AUTORELOAD**: If True, python source code changes will result in a reload of the server to affect the new code 
* **FLASHLIGHT_SERVER_HOST**: The host on which to serve Flashlight web ui (must also be in ALLOWED_HOSTS setting)
* **FLASHLIGHT_SERVER_PORT**: The TCP port on which to serve Flashlight web ui
* **FLASHLIGHT_SERVER_LOG_STDOUT**: If True send HTTP server logging to stdout
* **FLASHLIGHT_MAX_REQUEST_BODY_SIZE**: The size in bytes for request body size
* **FLASHLIGHT_MAX_REQUEST_HEADER_SIZE**: The max size in bytes for request headers
* **FLASHLIGHT_SSL_PRIVATE_KEY**: The TLS Private Key (in pem format) to use for TLS
* **FLASHLIGHT_SSL_CERTIFICATE**: The TLS Certificate (in pem format) to use for TLS
* **FLASHLIGHT_SSL_MODULE**: The SSL module to use with the web server
* **FLASHLIGHT_SOCKET_TIMEOUT**: The number of seconds to wait for sockets to be established
* **FLASHLIGHT_SOCKET_QUEUE_SIZE**: The number of connections to allow to queue before being rejected
* **FLASHLIGHT_ACCEPTED_QUEUE_TIMEOUT**: How long to wait for an HTTP request to wait to be accepted before timing out
* **FLASHLIGHT_SERVER_MAX_THREADS**: The max number of threads to spawn to handle web requests.
* **FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE**: If True, the default, flashlight will run field extraction functions on events based on sourcetype when the events are created
* **FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE**: If True, the default, flashlight will run processor functions on events based on sourcetype when the events are created
* **FLASHLIGHT_ENABLE_EXTRACTIONS_ON_UPDATE**: If True, the default, flashlight will run field extraction functions on events based on sourcetype when the events are updated
* **FLASHLIGHT_ENABLE_PROCESSORSS_ON_UPDATE**: If True, the default, flashlight will run processor functions on events based on sourcetype when the events are updated
* **FLASHLIGHT_STRICT_VALIDATION**: (Experimental) If enabled, type checks will be performed on the values passed between search commands can cause crashes
* **FLASHLIGHT_DOCUMENTATION_DIRECTORY**: The directory where the flashlight documentation will be served from
* **FLASHLIGHT_EXTRACTION_MAP**: A mapping of sourcetype to field extraction function to be called on each event with the specified sourcetype
* **FLASHLIGHT_PROCESSOR_MAP**: A mapping of sourcetype and processor function to be called on each event with the specified sourcetype
* **FLASHLIGHT_NAV_MENU**: A mapping of title and view to add to the side nav of the flashlight web ui
* **FLASHLIGHT_SEARCH_COMMANDS**: A mapping of search commands to their implementations
* **Q_CLUSTER**: Not specific to Flashlight, but is the task scheduler used by flashlight
* **FLASHLIGHT_SERVICE_COMMANDS**: The commands specifying the processes for the Flashlight Supervisor Service to spawn and keep alive
* **FLASHLIGHT_SERVICE_INTERVAL**: The number of seconds to sleep before the next check on the processes for the Flashlight Supervisor Service

## Basic Concepts
- **Events**: Events are the basic unit of data in Flashlight
- **Queries**: Queries are how events are retrieved, transformed, visualized and more
- **Ingestion**: The process of importing data from various sources.
- **Field Extraction / Preprocessing**: The process of identifying and extracting specific fields from your data and preprocessing them.
- **Search**: The ability to query and filter data.
- **Custom Apps**: Creating custom Flashlight applications to isolate related data and code.
- **Alerts**: Notifications based on specific conditions.

### Events

Events, in Flashlight, are designed to store arbitrary, text-based data.

Events are stored in a database and consist of a few indexed fields:

* created
* index
* source
* host

In addition to the above indexed fields, Flashlight also contains a JSON Field called
`extracted_fields` used to store information extracted from the Event.

Events can be created through the Flashlight REST API, or they can be created through queries
(with the use of some search commands) either interactively or on a scheduled basis. 

### Queries

Queries, in flashlight, are designed to retrieve, transform and store data.

A Query can be ephemeral or it can be persisted to the database.

In either case, a Query will have a field called `text`. The value of the `text` field
determines the pipeline through which the Events will be passed through using search commands.

Queries use a pipeline syntax where commands are chained together using the `|` operator, similar to command-line shells.

> In cases where a pipe `|` is needed for an argument or within a Jinja2 template tag or filter, you can escape the pipe operator by doubling the pipe character `||`.

Let's take a look at an example:

```bash
search --last-15-minutes index=default
```

This query uses one search command, `search`. The `search` search command is used to retrieve Events
from the database. In this instance it will retrieve all `Events` created in the last 15 minutes with `index` set to `default`.

#### Difference between Events and events

When talking about Queries in Flashlight, we can distinguish between `Event` instances which are `Event`s stored in the database, and 'events' as the unit of data passed between search commands within the context of a Query execution.

Let's take a look at an example:

```bash
search --last-15-minutes index=default
| select extracted_fields
| explode extracted_fields
```

In this example, we start with the same result set that was produced with the previous query, but
now the results of the `search` search command have been passed to the `select` search command.

The `select` search command is used to select which fields from the events to keep. The result of
this `select` will be that all fields other than `extracted_fields` will be dropped.

The `explode` search command is used to take a field which contains Key, Value pairs and expand that object to several fields, one for each key-value pair at the top.

So, as you can see, the 'events' passed between the search commands can contain fields other than
those of the `Event` instances.

### Ingestion
Ingestion is the process of importing data from various sources into Flashlight. This can include log files, REST APIs, databases, and more. Flashlight is very versatile with ingesting data, offering several methods to get data into the platform. The ingestion interface allows you to configure and manage data sources, ensuring that data is imported efficiently and accurately.

#### Flashlight's REST API
Flashlight provides a REST API for data ingestion, allowing you to programmatically send data to the platform. This method is ideal for integrating with other applications and services that generate data. 

You can browse the REST API. Most endpoints can be found when browsing to `/api/`, including an endpoint to create a Query, but there is one additional endpoint, `/api/query`, which will resolve a Query and return the results.

#### File-tail Utility
The file-tail utility allows you to ingest data from log files in real-time. This utility monitors specified log files and streams new entries into Flashlight as they are written.

#### Syslog (UDP/TCP/TLS)
Flashlight supports Syslog for data ingestion over UDP, TCP, and TCP over TLS. This method is commonly used for collecting logs from network devices, servers, and other infrastructure components.

#### Through Searches (Interactive and Scheduled)
You can also ingest data through searches, both interactive and scheduled. This method allows you to define search queries that retrieve data from external sources and import it into Flashlight on a schedule or on-demand.

### Field Extraction / Preprocessing
Field extraction is the process of identifying and extracting specific fields from your data. Flashlight supports both index-time and search-time field extractions.

#### Index-time Field Extractions
Index-time field extractions are performed by specifying a parser function for a particular sourcetype of event in `settings.py` under the `FLASHLIGHT_EXTRACTION_MAP`. These field extractions are applied as data is ingested and are persisted to the database under the Event's `extracted_fields` field.

#### Search-time Field Extractions
Search-time field extractions are performed using search commands. These extractions are very versatile and allow you to dynamically extract fields during a search. Search-time field extractions are not usually persisted to the database, but they can be if needed. This method provides flexibility in querying and analyzing data without modifying the underlying data storage.

#### Preprocessing
Preprocessing in Flashlight is similar to index-time field extractions. These preprocessing rules are defined in `settings.py` under the `FLASHLIGHT_PROCESSOR_MAP` and are executed based on the `sourcetype` of the event.

Preprocessing functions are called as an event with the corresponding `sourcetype` is being indexed. This can be useful for sending alerts in real time.

### Search
Searches can be done through the REST API at the `/api/query/` URL or they can be done through the web UI at the `/explore` URL.

Search functionality not only allows you to query and filter your data to find specific information, but also can perform a number of other functions such as:

* Performing an HTTP request
* Reading from an uploaded file
* Creating Events

Flashlight supports a wide variety of search commands and allows you to create your own custom search commands in Python and register them in `settings.py` under `FLASHLIGHT_SEARCH_COMMANDS`.

### Custom Apps
Flashlight allows you to write your own custom apps. Custom apps allow you to group related data and code. Custom apps enable:

* Storing data in its own separate database table
* Custom data permissions
* Custom search commands
* Custom Dashboards
* Adding custom REST API endpoints
* Much more

Flashlight apps are also Django Apps, so all of [their documentation](https://docs.djangoproject.com/en/5.1/ref/applications/) applies in addition to our own.

### Alerts
Flashlight provides two methods for implementing alerts: search-based alerts using the `send_email` command and processor-based alerts using the `FLASHLIGHT_PROCESSOR_MAP`.

#### Email Configuration
First, configure email settings in your `settings.py` file:

```python
# filepath: /flashlight/settings.py
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587  # Common ports are 587 (TLS) or 465 (SSL)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = 'Flashlight Alerts <alerts@your-domain.com>'
```

For development, you can use the file-based backend:
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'  # Change this to your preferred location
```

#### Search-based Alerts
To create an alert, you'll need to:

1. First, save your query using one of these methods:
   - **Explore UI**: Create and test your query in `/explore`, then click "Save Query"
   - **Django Admin**: Navigate to `/admin/events/query/` and create a new Query
   - **REST API**: POST to `/api/queries/`

Example query to save:
```bash
search --last-15-minutes text__icontains=fail index=logs
| qs_values host
| qs_annotate count=Count(host)
| qs_order_by count
| qs_filter count__gt=100
| send_email to="team@example.com" subject="High Failure Rate Alert"
```

2. Schedule the saved query using Django Q:
   1. Ensure the Q cluster is running (`fl qcluster` or via Windows Service)
   2. Access the Django admin interface at `/admin/`
   3. Navigate to `Django Q > Scheduled tasks`
   4. Click "Add Scheduled task"
   5. Configure the schedule:
      ```python
      Name: "High Error Rate Alert"
      Func: "events.util.run_query"
      Hook: None
      Args: '["High Error Rate Alert"]'  # Use your saved query name here
      Schedule Type: CRON
      Cron: */15 * * * *  # Runs every 15 minutes
      ```
   6. Set additional options:
      - `Repeats`: -1 for infinite repetition
      - `Next Run`: When the schedule should start
      - `Cluster`: Leave as default

Note: For Windows installations using the Flashlight service, make sure the service is running to process scheduled tasks (ie. make sure a `qcluster` command is included FLASHLIGHT_SERVICE_COMMANDS). You can check the service status in Windows Services (services.msc).

#### Processor-based Alerts
For immediate alerts when specific events are ingested, use the `FLASHLIGHT_PROCESSOR_MAP`:

```python
# filepath: /flashlight/settings.py
def alert_on_critical_error(event):
    from django.core.mail import send_mail
    
    if 'CRITICAL' in event.upper():
        send_mail(
            subject='Critical Error Detected',
            message=f'Critical error in event: {event.id}',
            from_email='alerts@your-domain.com',
            recipient_list=['team@example.com'],
        )

FLASHLIGHT_PROCESSOR_MAP = {
    'error_logs': alert_on_critical_error,
    'security_events': 'myapp.processors.security_alert_processor',
}
```

The processor function is called whenever an event with the matching sourcetype is created or updated. This allows for real-time alerting based on event content.

Remember that `FLASHLIGHT_ENABLE_PROCESSORS_ON_CREATE` and `FLASHLIGHT_ENABLE_PROCESSORS_ON_UPDATE` must be set to `True` in `settings.py` for processors to work.
