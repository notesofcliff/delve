# User Guide

## Using the Web UI
The web UI provides an intuitive interface for interacting with your data.

The web UI consists of the following pieces:

* The Browsable REST API
* The Documentation
* The Explore UI
* The Admin UI

## Ingesting Data
Flashlight supports data ingestion from various sources, including log files, REST APIs, syslog and more. Flashlight is very versatile with ingesting data, offering several methods to get data into the platform. Use the ingestion interface to configure and start data ingestion.

### Flashlight's REST API
Flashlight provides a REST API for data ingestion, allowing you to programmatically send data to the platform. This method is ideal for integrating with other applications and services that generate data.

You can browse the REST API. Most endpoints can be found when browsing to `/api/`, including an endpoint to create a Query, but there is one additional endpoint, `/api/query`, which will resolve a Query and return the results.

To create a new Event, POST a JSON document with the keys below to `/api/events`. The JSON document must have the following keys:

* **text**: The text of the Event.
* **index**: The index for the Event.
* **host**: The host to associate with the Event.
* **source**: The source to associate with the Event.
* **sourcetype**: The sourcetype to associate with the Event.

If you are sending multiple events at a time, the it should be in the form of a JSON Array of objects each having the above keys.

### File-tail Utility
The file-tail utility allows you to ingest data from log files in near real-time. This utility monitors specified log files and sends new entries to Flashlight as they are written. This is particularly useful for continuously monitoring log files for new data.

For efficiency, the file-tail utility is seperate from the main flashlight server. This means that you must run it in a seperate process. The file-tail utility sends Events to the Flashlight REST API. Please follow the steps in the Usage section properly.

#### Usage
The file-tail utility is a command-line tool that can be used to monitor log files and send new entries to Flashlight. Below are the steps to use the file-tail utility:

1. Open a terminal or command prompt.
2. Navigate to the Flashlight directory
3. Execute `set-env.bat` (windows) or `source set-env` (linux/Mac)
4. Execute `python utilities/cli/tail-files.py --help`
5. Run the script with the appropriate arguments.

#### Command-line Arguments
The `tail-files.py` script accepts the following command-line arguments:

* `--server`: The scheme, host, and port of the Flashlight server (default: `http://localhost:8000`).
* `--no-verify`: If specified, TLS hostname verification will be disabled.
* `-i, --index`: The index in which to store the event (default: `default`).
* `-H, --host`: The host to associate with the event (default: `localhost`).
* `-t, --sourcetype`: The sourcetype to associate with the event (default: `plaintext`).
* `-u, --username`: The username to use for authentication (if omitted, you will be prompted).
* `-p, --password`: The password to use for authentication (if omitted, you will be prompted).
* `-v, --verbose`: Increase verbosity of log output.
* `-l, --log-file`: The file to which logs will be written (default: `log/tail-files.log`).
* `-d, --delay`: The number of seconds to sleep between API POST requests (default: `1`).
* `--batch-size`: The number of events to send to the Flashlight server per request (default: `1000`).
* `--max-queue-size`: The maximum number of events waiting to be uploaded to Flashlight (default: `10000`).
* `patterns`: Glob patterns matching files to monitor (quote this to prevent shell expansion).

#### Example Usage
Here are some example commands to use the file-tail utility:

```bash
# Basic usage with default settings
python tail-files.py "/path/to/logfile.log"

# Specify a custom index
python tail-files.py --index "my_index" "/path/to/logfile.log"

# Specify a custom sourcetype
python tail-files.py --sourcetype "my_sourcetype" "/path/to/logfile.log"

# Disable TLS hostname verification for the flashlight server
python tail-files.py --no-verify --server "https://flashlight.example.com" "/path/to/logfile.log"

# provide username and password for authentication to prevent being prompted
python tail-files.py --username "myuser" --password "mypassword" "/path/to/logfile.log"

# Slightly Increase verbosity of log output
python tail-files.py -v "/path/to/logfile.log"

# Most verbose log output
python tail-files.py -vvvvvv "/path/to/logfile.log"

# Monitor multiple log files using glob patterns
python tail-files.py "/var/log/*.log"
```

#### Additional Information
The file-tail utility maintains the position of the last read entry in each monitored log file. This information is stored in a JSON file (`utilities/_data/tail-files.json`) to ensure that the utility can resume from where it left off in case of a restart.

The utility batches events to improve performance. You can configure the batch size and the maximum queue size using the `--batch-size` and `--max-queue-size` arguments, respectively.

### Syslog (UDP\TCP\TCPw/TLS)
Flashlight supports Syslog for data ingestion over UDP, TCP, and TCP with TLS. This method is commonly used for collecting logs from network devices, servers, and other infrastructure components.

#### Usage
The syslog-receiver utility is a command-line tool that can be used to receive syslog messages and send them to Flashlight. Below are the steps to use the syslog-receiver utility:

1. Open a terminal or command prompt.
2. Navigate to the Flashlight directory.
3. Execute `set-env.bat` (Windows) or `source set-env` (Linux/Mac).
4. Execute `python utilities/cli/syslog-receiver.py --help`.
5. Run the script with the appropriate arguments.

#### Command-line Arguments
The `syslog-receiver.py` script accepts the following command-line arguments:

* `--server`: The scheme, host, and port of the Flashlight server (default: `http://localhost:8000`).
* `--no-verify`: If specified, TLS hostname verification will be disabled.
* `-i, --index`: The index in which to store the event (default: `default`).
* `-H, --host`: The host to associate with the event (default: the IP address of the client).
* `-s, --source`: The source to associate with the event (default: `text/syslog`).
* `-t, --sourcetype`: The sourcetype to associate with the event (default: `text/syslog`).
* `-u, --username`: The username to use for authentication (if omitted, you will be prompted).
* `-p, --password`: The password to use for authentication (if omitted, you will be prompted).
* `--line-ending`: The type of line endings to expect (`linux`, `macos`, `windows`).
* `--udp`: If specified, will listen for UDP messages.
* `--tcp`: If specified, will listen for TCP messages.
* `--tcp-port`: The TCP port to listen on (default: `1514`).
* `--tcp-cert`: If this and `--tcp-key` are specified, the TCP listener will use TLS.
* `--tcp-key`: If this and `--tcp-cert` are specified, the TCP listener will use TLS.
* `--udp-port`: The UDP port to listen on (default: `2514`).
* `--hostname`: The hostname (or IP) to listen on.
* `-v, --verbose`: Increase verbosity of log output.
* `-l, --log-file`: The file to which logs will be written (default: `log/syslog-receiver-<pid>.log`).
* `--batch-size`: The number of events to send to the Flashlight server per request (default: `10000`).
* `--max-queue-size`: The maximum number of events waiting to be uploaded to Flashlight (default: `10000`).

#### Example Usage
Here are some example commands to use the syslog-receiver utility:

```bash
# Basic usage with default settings for UDP
python syslog-receiver.py --udp

# Basic usage with default settings for TCP
python syslog-receiver.py --tcp

# Basic usage with default settings for TCP and UDP
python syslog-receiver.py --tcp --udp

# Listen on a custom port for TCP
python syslog-receiver.py --tcp --tcp-port 9514

# Specify a custom index and sourcetype for UDP
python syslog-receiver.py --udp --index "my_index" --sourcetype "my_sourcetype"

# Specify a custom index and sourcetype for TCP
python syslog-receiver.py --tcp --index "my_index" --sourcetype "my_sourcetype"

# Use TLS for TCP with specified certificate and key
python syslog-receiver.py --tcp --tcp-cert "/path/to/cert.pem" --tcp-key "/path/to/key.pem"

# Disable TLS hostname verification for the Flashlight server
python syslog-receiver.py --no-verify --server "https://flashlight.example.com" --tcp

# Provide username and password for authentication to prevent being prompted
python syslog-receiver.py --username "myuser" --password "mypassword" --udp

# Lowest verbosity of log output (less than default)
python syslog-receiver.py -v --udp

# Most verbose log output (more than default)
python syslog-receiver.py -vvvvvv --udp
```

#### Additional Information
The syslog-receiver utility supports both UDP, TCP or both at once for receiving syslog messages. You can specify the supported protocols using the `--udp` or `--tcp` arguments. If you want to use TLS for TCP, you need to provide the certificate and key files using the `--tcp-cert` and `--tcp-key` arguments.

The utility batches events to improve performance. You can configure the batch size and the maximum queue size using the `--batch-size` and `--max-queue-size` arguments, respectively.

### Upload a File Directly
Flashlight allows direct file uploads for data ingestion, facilitating one-time or batch data imports from various file formats. The upload interface enables users to select and upload files, which are subsequently processed and ingested into the platform.

By default, users are restricted to accessing their own file uploads.

#### Methods of Upload
Files can be uploaded using the following methods:

* **REST API**: Perform a POST request to `/api/files/` with the file included as a multipart/form-encoded payload.
* **Explore UI**: Click the "File Uploads" button at the top of the page to reveal the file upload form.
* **Admin UI**: Click "File Uploads" on the left-hand side.

#### Reading Uploaded Files
Once a file is uploaded, it can be read into a search using the `read_file` command. For example, if a file is named "example.xml", it can be read into a search with the following command:

```bash
read_file example.xml
```

By default, `read_file` returns the contents of the file in the `content` field as an array of lines. To parse the XML, use the following command:

```bash
read_file --parse xml example.xml
```

#### Parse Options
The following parse options are currently available:

* `csv`
* `json`
* `jsonl`
* `xml`

### Searching (Interactive and Scheduled)
Flashlight supports both interactive and scheduled searches, allowing users to define search queries that retrieve data from external sources and import it into Flashlight on a regular basis or on-demand. Interactive searches are performed manually, while scheduled searches run automatically at specified intervals.

#### Search Commands
Flashlight provides several built-in search commands to retrieve, parse, and transform data. Some of the key search commands include:

* `search`: Retrieve data through Flashlight, including the models of registered apps.
* `request`: Perform an HTTP request and return the data.
* `read_file`: Retrieve data from an uploaded file.

Custom search commands can also be defined to retrieve, parse, and/or transform data.

Check the [Search Command Reference](Search_Command_Reference.md) for a list of all search commands included with Flashlight.

Custom or third-party Flashlight apps can also define search commands, but all search commands must be configured in `settings.py` under `FLASHLIGHT_SEARCH_COMMANDS` in order to be used.

#### Example Usage
Here are some example commands to use the search functionality:

```bash
# Basic search to retrieve data from the flashlight database  
search --index default text__icontains="error"

# Perform an HTTP request and return the data
request GET https://api.example.com/data

# Retrieve data from an uploaded file
read_file example.xml
```

#### make_events Command
The `make_events` command allows you to generate events based on the current result set and index them into the Flashlight database. This command is useful for creating new events from existing data or external sources.

##### Command-line Arguments
The `make_events` command accepts the following command-line arguments:

* `-i, --index`: The index to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-o, --host`: The host to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-s, --source`: The source to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-t, --sourcetype`: The sourcetype to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-S, --save`: If specified, the events will be saved.
* `-d, --drop`: If specified, provide the name of a field to drop before creating the events.

##### Example Usage
Here are some example commands to use the `make_events` command:

```bash
# Generate events with default settings
make_events

# Specify a custom index and host
make_events --index "custom_index" --host "custom_host"

# Drop specific fields before creating events
make_events --drop "field1" --drop "field2"

# Save the generated events
make_events --save
```

## Searching, Filtering and More
Flashlight provides a comprehensive search interface that supports a wide range of search commands and the ability to define custom search commands. These commands are categorized into four types: Data Sources, Queryset Transformations, Generic Transformations, and Visualization Commands.

### Data Sources
Data source commands are used to pull data into your results. These commands retrieve data from various sources and integrate it into the Flashlight platform.

#### Example Commands
* `search`: Retrieve data through Flashlight, including the models of registered apps.
* `request`: Perform an HTTP request and return the data.
* `read_file`: Retrieve data from an uploaded file.

### Queryset Transformations
Queryset transformation commands act on Django Querysets (such as the output of the `search` command) and expose Queryset methods. These commands allow you to directly affect the SQL statements before they are executed, resulting in faster performance.

#### Example Commands
* `qs_filter`: Filter the queryset based on specified criteria.
* `qs_explain`: Explain the queryset execution plan.
* `qs_latest`: Retrieve the latest entry in the queryset.
* `qs_first`: Retrieve the first entry in the queryset.
* `qs_earliest`: Retrieve the earliest entry in the queryset.
* `qs_count`: Count the number of entries in the queryset.

### Generic Transformations
Generic transformation commands modify data from a source command in some way. These commands are designed to be versatile and work well with diverse sets of data, although they may be slower than their `qs_` counterparts.

#### Example Commands
* `rename`: Rename fields in the result set.
* `replace`: Replace values in the result set.
* `rex`: Extract fields using regular expressions.
* `dedup`: Remove duplicate entries from the result set.
* `sort`: Sort the result set based on specified criteria.

### Visualization Commands
Visualization commands take a result set and generate a table, chart, or other visualization. These commands help you to display your data in a meaningful and interactive way.

#### Example Commands
* `chart`: Generate a chart based on the result set.
* `table`: Generate a table based on the result set.

