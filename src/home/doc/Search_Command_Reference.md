## Search Command Reference

### autocast
The `autocast` command attempts to automatically cast fields to their appropriate data types based on their values. This can be useful for ensuring that fields are correctly typed for further processing and analysis.

#### Options
* `fields`: One or more fields to autocast. If no fields are specified, all fields will be considered for autocasting.

#### Example Usage
```bash
# Autocast specific fields
autocast field1 field2
```

#### Notes
The `autocast` command uses the `cast` utility function to determine the appropriate data type for each field. The command iterates over the specified fields and attempts to cast their values to the most suitable data type.

### chart
The `chart` command generates a chart based on the result set. It returns the JSON data required to configure a Chart.js chart.

#### Options
* `-t, --type`: The type of chart to generate (default: `bar`). Choices are `bar` and `line`.
* `-x, --x-field`: The field to plot on the X axis.
* `-y, --y-field`: The field to plot on the Y axis.
* `-b, --by-field`: The field to split into series.
* `--time-x`: If specified, the data on the X axis will be treated as time. Choices are `minute`, `hour`, `day`, `week`, `month`, `quarter`, and `year`.

#### Example Usage
```bash
# Generate a bar chart with specified X and Y fields
chart --type bar --x-field date --y-field count

# Generate a line chart with time-based X axis
chart --type line --x-field timestamp --y-field value --time-x day
```

#### Notes
The `chart` command uses the Chart.js library to generate charts. It supports various chart types and can handle time-based data on the X axis. The command groups data by the specified `by-field` if provided, and generates datasets accordingly.

### dedup
The `dedup` command removes duplicate entries from the result set based on the specified fields. If no fields are specified, the entire event is used for comparison. The first matching item is kept, and subsequent duplicates are removed. It is recommended to sort the events prior to using this command.

#### Options
* `fields`: One or more fields to use for deduplication. If no fields are specified, the entire event is used for comparison.

#### Example Usage
```bash
# Deduplicate based on specific fields
dedup field1 field2

# Deduplicate using the entire event for comparison
dedup
```

#### Notes
The `dedup` command iterates over the events and compares them based on the specified fields. If no fields are specified, the entire event is used for comparison. The command keeps the first matching item and removes subsequent duplicates. It is recommended to sort the events prior to using this command to ensure that the desired items are kept.

### distinct
The `distinct` command retrieves distinct values from the result set based on the specified fields. It returns one event with fields containing the unique values of the specified fields.

#### Options
* `fields`: One or more fields to use for retrieving distinct values.

#### Example Usage
```bash
# Retrieve distinct values based on specific fields
distinct field1 field2
```

#### Notes
The `distinct` command iterates over the events and collects unique values for the specified fields. It returns a single event where each specified field contains a list of unique values found in the result set.

### drop_fields
The `drop_fields` command removes specified fields from the result set. This can be useful for excluding unnecessary or sensitive information from the results.

#### Options
* `fields`: One or more fields to drop from all events.

#### Example Usage
```bash
# Drop specific fields from the result set
drop_fields field1 field2
```

#### Notes
The `drop_fields` command iterates over the events and removes the specified fields if they are present. If a field is not found in an event, it is simply ignored.

### echo
The `echo` command returns the given expressions as an event appended to the result set. This can be useful for debugging or adding static information to the results.

#### Options
* `expressions`: One or more expressions to echo.

#### Example Usage
```bash
# Echo specific expressions
echo "Hello, World!" "Test message"
```

#### Notes
The `echo` command appends the provided expressions as new events to the result set. Each expression is returned as a separate event with a single field named `expression`.

### ensure_list
The `ensure_list` command ensures that a specified field contains a list. If any other type of value is present in the specified field, it will be placed as a single item in a list.

#### Options
* `field`: The field to ensure is a list.

#### Example Usage
```bash
# Ensure the specified field is a list
ensure_list field1
```

#### Notes
The `ensure_list` command checks the specified field in each event. If the field is not already a list, it converts the value to a list containing the original value. If the field is not present, it sets the field to a list containing a single `None` value.

### eval
The `eval` command evaluates an expression and stores the result in a new field. This can be useful for creating new fields based on existing data or performing calculations.

#### Options
* `expressions`: One or more expressions to evaluate. Each expression should be in the format `field=value`.

#### Example Usage
```bash
# Evaluate expressions and store the results in new fields
eval field1=value1 field2=$existing_field
```

#### Notes
The `eval` command iterates over the events and evaluates the provided expressions. If the right-hand side of an expression starts with a dollar sign (`$`), it is treated as a reference to an existing field in the event. Otherwise, it is treated as a literal value. The result is stored in the specified field on the left-hand side of the expression.

### event_split
The `event_split` command attempts to split events into multiple events based on a specified field. The specified field should contain a JSON array.

#### Options
* `split_field`: The field to split. If the specified field points to a list, the events returned will be expanded with an event per item in the list. The fields of the events will be preserved with each new item having a copy of other fields' values.

#### Example Usage
```bash
# Split events based on a specified field
event_split split_field
```

#### Notes
The `event_split` command iterates over the events and splits them based on the specified field. If the field contains a list, each item in the list will be used to create a new event. If the field contains a dictionary, each key-value pair will be used to create a new event with an additional field for the key.

### events_to_context
The `events_to_context` command puts the current result set into the local context for use in Jinja templating.

#### Options
* `-z, --return-empty`: If specified, events received will be loaded into the local context and an empty list will be returned. By default, events received will be returned after processing.

#### Example Usage
```bash
# Put the current result set into the local context
events_to_context

# Put the current result set into the local context and return an empty list
events_to_context --return-empty
```

#### Notes
The `events_to_context` command loads the current result set into the local context for use in Jinja templating. If the `--return-empty` option is specified, an empty list will be returned instead of the events.

### explode
The `explode` command extracts the nested JSON fields from an object and adds them to the event. The original field is removed.

#### Options
* `--prefix`: String to be prefixed to the name of the fields that the explode operation creates.
* `field`: The field to explode. If the field points to a JSON object, its fields will be added to the event and the original field will be removed. Events without the specified field will be omitted from the results.

#### Example Usage
```bash
# Explode a nested JSON field
explode --prefix nested_ field
```

#### Notes
The `explode` command iterates over the events and extracts the nested JSON fields from the specified field. The extracted fields are added to the event with an optional prefix, and the original field is removed.

### explode_timestamp
The `explode_timestamp` command extracts the available fields in a timestamp field and adds them as fields to the event with an optional prefix.

#### Options
* `--prefix`: String to be prefixed to the name of the fields that the operation creates.
* `field`: A field with a timestamp as the value. All available fields from the timestamp (year, month, day, hour, etc.) will be added to the event.

#### Example Usage
```bash
# Explode a timestamp field
explode_timestamp --prefix ts_ field
```

#### Notes
The `explode_timestamp` command iterates over the events and extracts the available fields from the specified timestamp field. The extracted fields are added to the event with an optional prefix. If the field contains a `datetime`, `date`, or `time` object, the corresponding fields (year, month, day, hour, etc.) will be added to the event.

### filter
The `filter` command reduces the result set by removing events that do not meet the specified criteria. It supports various lookup operations to filter events based on field values.

#### Options
* `terms`: One or more search terms in the form `KEY=VALUE` where `KEY` is a reference to a field and `VALUE` is the value. Django field lookups are supported.
* `--no-cast`: If specified, the value will not be cast to a type before completing the test.

#### Example Usage
```bash
# Filter events based on specific criteria
filter field1=value1 field2__gt=value2
```

#### Notes
The `filter` command iterates over the events and applies the specified criteria to filter the result set. It supports various lookup operations such as `exact`, `contains`, `gt`, `lt`, and more. If the `--no-cast` option is specified, the value will not be cast to a type before completing the test.

### head
The `head` command returns the first N records of the result set. This can be useful for limiting the number of events returned.

#### Options
* `-n, --number`: The number of events to return (default: 10).

#### Example Usage
```bash
# Return the first 10 events
head --number 10
```

#### Notes
The `head` command iterates over the events and returns the specified number of events. By default, it returns the first 10 events.

### join
The `join` command joins the current result set to the results of another query. It supports various join types and allows you to specify the fields to join on.

#### Options
* `--last-15-minutes`: Filter events from the last 15 minutes.
* `--last-hour`: Filter events from the last hour.
* `--last-day`: Filter events from the last day.
* `--last-week`: Filter events from the last week.
* `--last-month`: Filter events from the last month.
* `--order-by`: Specify the fields to order the events by. Can be specified multiple times.
* `-t, --type`: The type of join to perform (default: `left`). Choices are `left`, `right`, `full`, and `inner`.
* `-f, --fields`: The fields to join on, specified in the format `LEFT_FIELD,RIGHT_FIELD`.
* `--model`: The model to query (default: `events.models.Event`).
* `terms`: One or more search terms in the form `KEY=VALUE` where `KEY` is a reference to a field and `VALUE` is the value.

#### Example Usage
```bash
# Perform a left join on specific fields
join --type left --fields field1,field2
```

#### Notes
The `join` command iterates over the events and joins them with the results of another query based on the specified fields. It supports various join types such as `left`, `right`, `full`, and `inner`. The command also allows you to filter and order the events based on the specified criteria.

### make_events
The `make_events` command generates events based on the current result set and indexes them into the Flashlight database. This command is useful for creating new events from existing data or external sources.

#### Options
* `-i, --index`: The index to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-o, --host`: The host to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-s, --source`: The source to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-t, --sourcetype`: The sourcetype to assign to the new events. You can use dollar sign notation to assign the value of a field.
* `-S, --save`: If specified, the events will be saved.
* `-d, --drop`: If specified, provide the name of a field to drop before creating the events.

#### Example Usage
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

#### Notes
The `make_events` command iterates over the events and generates new events based on the specified criteria. It allows you to assign custom values to the index, host, source, and sourcetype fields. The command also supports dropping specific fields before creating the events and saving the generated events to the database.

### mark_timestamp
The `mark_timestamp` command parses the given fields from strings to datetime objects. This is useful for use with the `filter` search command.

#### Options
* `fields`: One or more fields to parse as datetime.

#### Example Usage
```bash
# Parse specific fields as datetime
mark_timestamp field1 field2
```

#### Notes
The `mark_timestamp` command iterates over the events and parses the specified fields as datetime objects. This is useful for filtering events based on datetime criteria.

### read_file
The `read_file` command retrieves data from an uploaded file and processes it as events. This command supports various file formats and allows for parsing the file contents.

#### Options
* `filename`: The uploaded file to read in.
* `--allow-escape`: Allow automatic escaping of file contents.
* `--parse`: Specify the format to parse the file contents. Supported options are `csv`, `json`, `jsonl`, and `xml`.

#### Example Usage
```bash
# Read an uploaded file and parse it as JSON
read_file example.json --parse json
```

#### Notes
The `read_file` command retrieves the specified uploaded file and processes its contents as events. It supports various file formats and allows for parsing the file contents accordingly. If the `--allow-escape` option is specified, the command will automatically escape the file contents.

### rename
The `rename` command renames a field in the result set. This can be useful for standardizing field names or correcting field names.

#### Options
* `-f, --from-field`: The field to rename.
* `-t, --to-field`: The new name for the field.

#### Example Usage
```bash
# Rename a field in the result set
rename --from-field old_field --to-field new_field
```

#### Notes
The `rename` command iterates over the events and renames the specified field. The original field is removed, and the new field is added with the same value.

### replace
The `replace` command replaces text matching a regular expression with a provided string. This can be useful for cleaning or transforming data.

#### Options
* `-f, --field`: The field to apply the replacement to.
* `expression`: The regular expression to match.
* `replacement`: The string to replace the matched text with.

#### Example Usage
```bash
# Replace text in a field using a regular expression
replace --field field_name "pattern" "replacement"
```

#### Notes
The `replace` command iterates over the events and applies the specified regular expression to the specified field. The matched text is replaced with the provided replacement string.

### request
The `request` command performs an HTTP request and returns the data. This can be useful for retrieving data from external sources.

#### Options
* `method`: The HTTP method to use for the request (default: `GET`). Choices are `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`, and `HEAD`.
* `url`: The URL to send the HTTP request to.
* `--username`: The username to use for authentication.
* `--password`: The password to use for authentication.
* `--kv-pairs`: Add key-value pairs to the query string for `GET` requests or the request body for `POST`, `PATCH`, and `PUT` requests.
* `--json`: Encode key-value pairs in the request body as JSON for `POST`, `PUT`, and `PATCH` requests.
* `--save-event`: Save the result of the request as an event.
* `--extract-fields`: Extract fields from the events regardless of whether the event was saved.
* `--recent-ok`: Return the latest event from the same user, host, URI, and method if it is not older than the specified number of minutes.
* `--recent-minutes`: The maximum age, in minutes, for an event to be considered recent (default: 5).
* `-H, --headers`: Provide HTTP headers for the request.
* `-n, --no-verify`: Disable TLS hostname verification.

#### Example Usage
```bash
# Perform a GET request to a specified URL
request GET https://api.example.com/data

# Perform a POST request with JSON data
request POST https://api.example.com/data --json --kv-pairs key1=value1 key2=value2
```

#### Notes
The `request` command performs an HTTP request using the specified method and URL. It supports various options for authentication, headers, and request body data. The command can save the result of the request as an event and extract fields from the response.

### rex
The `rex` command uses regular expressions to extract values from a specified field and store them in `extracted_fields`. This can be useful for parsing and extracting specific information from text fields.

#### Options
* `-f, --field`: The field to run the regular expression against (default: `text`).
* `expressions`: One or more regular expressions to apply.

#### Example Usage
```bash
# Extract values from a field using regular expressions
rex --field message "pattern1" "pattern2"
```

#### Notes
The `rex` command iterates over the events and applies the specified regular expressions to the specified field. The extracted values are stored in `extracted_fields` for further processing and analysis.

### run_query
The `run_query` command runs a named query and appends the results to the current result set. This can be useful for reusing predefined queries and combining their results with other data.

#### Options
* `name`: The name of the query to run.

#### Example Usage
```bash
# Run a named query and append the results
run_query query_name
```

#### Notes
The `run_query` command retrieves the specified named query and executes it. The results of the query are appended to the current result set, allowing for further processing and analysis.

### search
The `search` command retrieves data from the Flashlight database based on specified criteria. It supports various filtering, ordering, and limiting options to refine the search results.

#### Options
* `--last-15-minutes`: Filter events from the last 15 minutes.
* `--last-hour`: Filter events from the last hour.
* `--last-day`: Filter events from the last day.
* `--last-week`: Filter events from the last week.
* `--last-month`: Filter events from the last month.
* `--order-by`: Specify the fields to order the events by. Can be specified multiple times.
* `--limit`: The limit for the number of results to return.
* `--offset`: The offset to start from in results to return (default: 0).
* `--latest-by`: Return the latest result by the given field.
* `--latest`: Return just the latest event.
* `--model`: The model to query (default: `events.models.Event`).
* `terms`: One or more search terms in the form `KEY=VALUE` where `KEY` is a reference to a field and `VALUE` is the value.

#### Example Usage
```bash
# Retrieve data from the Flashlight database
search --last-day --order-by timestamp field1=value1 field2__gt=value2
```

#### Notes
The `search` command retrieves data from the Flashlight database based on the specified criteria. It supports various filtering, ordering, and limiting options to refine the search results. The command can also retrieve the latest event or the latest result by a given field.

### select
The `select` command removes all but the specified fields from all events. This can be useful for narrowing down the result set to only the relevant fields.

#### Options
* `fields`: One or more fields to retain in the result set.

#### Example Usage
```bash
# Retain specific fields in the result set
select field1 field2 field3
```

#### Notes
The `select` command iterates over the events and retains only the specified fields. All other fields are removed from the result set, allowing for a more focused analysis of the data.

### set
The `set` command sets values in the local Jinja2 context. This can be useful for dynamically configuring the context during a search.

#### Options
* `expressions`: One or more expressions to set values in the local context. Each expression should be in the format `key=value`.

#### Example Usage
```bash
# Set values in the local context
set key1=value1 key2=value2
```

#### Notes
The `set` command iterates over the provided expressions and sets the corresponding values in the local Jinja2 context. The values are cast to their appropriate types using the `cast` utility function.

### sort
The `sort` command sorts the result set by the specified fields. This can be useful for ordering the events based on certain criteria.

#### Options
* `-d, --descending`: If specified, sorting will be done in descending order.
* `fields`: One or more fields to sort by.

#### Example Usage
```bash
# Sort events by specific fields in ascending order
sort field1 field2

# Sort events by specific fields in descending order
sort --descending field1 field2
```

#### Notes
The `sort` command iterates over the events and sorts them based on the specified fields. If no fields are specified, the events are sorted using the default comparison. The command supports both ascending and descending order.

### sql_query
The `sql_query` command performs a SQL query against the specified database. This can be useful for retrieving data directly from a database using SQL.

#### Options
* `connection_string`: The database connection string (e.g., `mysql+pymysql://user:pass@some_mariadb/dbname`).
* `sql_query`: The SQL query to execute.

#### Example Usage
```bash
# Perform a SQL query against a database
sql_query "mysql+pymysql://user:pass@some_mariadb/dbname" "SELECT * FROM table_name"
```

#### Notes
The `sql_query` command connects to the specified database using the provided connection string and executes the SQL query. The results are returned as a list of dictionaries, where each dictionary represents a row in the result set.

### table
The `table` command generates a table based on the result set. It returns the JSON configuration required to create a table using DataTables.

#### Options
* `-f, --fields`: The fields to include in the table.

#### Example Usage
```bash
# Generate a table with specific fields
table --fields field1 field2 field3
```

#### Notes
The `table` command iterates over the events and generates a table configuration based on the specified fields. If no fields are specified, all fields are included in the table. The command returns the JSON configuration required to create a table using DataTables.

Please note that by default, results are returned as an Array of Ojects which 

### transpose
The `transpose` command inverts the result set. This can be useful for transforming the data structure for further analysis.

#### Options
This command does not accept any options.

#### Example Usage
```bash
# Transpose the result set
transpose
```

#### Notes
The `transpose` command iterates over the events and inverts the result set. It converts rows into columns and columns into rows, allowing for a different perspective on the data.

### value_list
The `value_list` command reduces the result set to include only the values from a specified field. This can be useful for extracting a list of values from a particular field in the events.

#### Options
* `field`: The field to extract the values from.

#### Example Usage
```bash
# Extract values from a specific field
value_list field_name
```

#### Notes
The `value_list` command iterates over the events and extracts the values from the specified field. The extracted values are returned as a list, allowing for further processing and analysis.

### qs_aggregate
The `qs_aggregate` command performs aggregation operations on the queryset. It allows you to compute summary values such as counts, averages, sums, etc.

#### Options
* `field_expressions`: One or more field expressions to aggregate.

#### Example Usage
```bash
# Perform aggregation on specific fields
qs_aggregate field1=Sum field2=Avg
```

#### Notes
The `qs_aggregate` command uses Django's `aggregate` method to perform the specified aggregation operations on the queryset. The field expressions should be in the format `field=AggregationFunction`.

### qs_alias
The `qs_alias` command creates an alias for a field in the queryset. This can be useful for renaming fields or creating new fields based on expressions.

#### Options
* `field_expressions`: One or more field expressions to alias.

#### Example Usage
```bash
# Create aliases for specific fields
qs_alias new_field1=old_field1 new_field2=old_field2
```

#### Notes
The `qs_alias` command uses Django's `alias` method to create the specified aliases in the queryset. The field expressions should be in the format `new_field=old_field`.

### qs_annotate
The `qs_annotate` command annotates the queryset with additional fields. This can be useful for adding computed fields or related data to the queryset.

#### Options
* `field_expressions`: One or more field expressions to annotate.

#### Example Usage
```bash
# Annotate the queryset with additional fields
qs_annotate new_field1=Expression1 new_field2=Expression2
```

#### Notes
The `qs_annotate` command uses Django's `annotate` method to add the specified annotations to the queryset. The field expressions should be in the format `new_field=Expression`.

### qs_count
The `qs_count` command counts the number of entries in the queryset. It returns the total number of records.

#### Options
This command does not accept any options.

#### Example Usage
```bash
# Count the number of entries in the queryset
qs_count
```

#### Notes
The `qs_count` command uses Django's `count` method to return the total number of records in the queryset.

### qs_dates
The `qs_dates` command retrieves dates from the queryset based on the specified field and kind. It returns a list of date objects.

#### Options
* `field`: The field to retrieve dates from.
* `kind`: The kind of dates to retrieve (choices: `year`, `month`, `week`, `day`).
* `order`: The order in which to retrieve the dates (choices: `ASC`, `DESC`).

#### Example Usage
```bash
# Retrieve dates from the queryset
qs_dates field=date_field kind=month order=ASC
```

#### Notes
The `qs_dates` command uses Django's `dates` method to retrieve the specified dates from the queryset. The `field` should be a date or datetime field, and the `kind` should be one of `year`, `month`, `week`, or `day`.

### qs_datetimes
Retrieve datetimes from the queryset.

### qs_defer
Defer loading of specified fields in the queryset.

### qs_delete
Delete entries from the queryset.

### qs_distinct
Retrieve distinct values from the queryset.

### qs_earliest
Retrieve the earliest entry in the queryset.

### qs_exclude
Exclude entries from the queryset based on specified criteria.

### qs_exists
Check if entries exist in the queryset.

### qs_explain
Explain the queryset execution plan.

### qs_filter
Filter the queryset based on specified criteria.

### qs_first
Retrieve the first entry in the queryset.

### qs_last
Retrieve the last entry in the queryset.

### qs_only
Retrieve only specified fields from the queryset.

### qs_order_by
Order the queryset based on specified criteria.

### qs_reverse
Reverse the order of the queryset.

### qs_select_related
Select related fields in the queryset.

### qs_update
Update entries in the queryset.

### qs_using
Specify the database to use for the queryset.

### qs_values
Retrieve values from the queryset.

