# Monitoring and Maintenance

Monitoring and maintaining Flashlight is crucial for ensuring its smooth operation and performance. This section covers various aspects of monitoring and maintenance, including using Django management commands and performing backups.

## Monitoring System Health
Monitoring the health of your Flashlight instance involves keeping an eye on system resources, application logs, and performance metrics. Here are some key areas to monitor:

- **System Resources**: Monitor CPU, memory, and disk usage to ensure the system has enough resources to handle the workload.
- **Application Logs**: Regularly check application logs for errors, warnings, and other important messages. Logs can be found in the `log` directory.
- **Performance Metrics**: Monitor response times, request rates, and other performance metrics to identify potential bottlenecks and optimize performance. The logging system can be fine-tuned to gain insights into these metrics without allowing the logs to become overly verbose.

## Using Django Management Commands
Django provides several management commands that are useful for monitoring and maintaining your Flashlight instance. Some key commands include (see the output of `./fl --help` for a complete list):

- **`./fl check`**: Checks the entire Django project for potential problems.
    ```bash
    fl check
    ```
- **`./fl showmigrations`**: Lists all migrations and their status.
    ```bash
    fl showmigrations
    ```
- **`./fl migrate`**: Applies database migrations.
    ```bash
    fl migrate
    ```
- **`./fl createsuperuser`**: Creates a new superuser account.
    ```bash
    fl createsuperuser
    ```

### Django Extension Commands
The Django Extensions module provides a number of helpful commands. Here are some of the more useful ones in the context of Flashlight:

- **`./fl shell_plus`**: An enhanced version of the Django shell with autoloading of models and other conveniences.
    ```bash
    fl shell_plus
    ```
- **`./fl graph_models`**: Generates a visual representation of your Django models.
    ```bash
    fl graph_models -a -o models.png
    ```
- **`./fl show_urls`**: Displays all the URL patterns in your project.
    ```bash
    fl show_urls
    ```
- **`./fl sqldiff`**: Compares the database schema with your models and displays differences.
    ```bash
    fl sqldiff
    ```

## Hosting with CherryPy
Flashlight uses CherryPy to host the Django web app. The `serve` management command starts the CherryPy server to serve the Flashlight web UI.

```bash
fl serve
```

The following settings in `settings.py` control the behavior of the CherryPy web server:

- **FLASHLIGHT_SERVER_HOST**: The host on which to serve the Flashlight web UI (must also be in `ALLOWED_HOSTS` setting).
- **FLASHLIGHT_SERVER_PORT**: The TCP port on which to serve the Flashlight web UI.
- **FLASHLIGHT_SERVER_LOG_STDOUT**: If `True`, send HTTP server logging to stdout.
- **FLASHLIGHT_MAX_REQUEST_BODY_SIZE**: The size in bytes for request body size.
- **FLASHLIGHT_MAX_REQUEST_HEADER_SIZE**: The max size in bytes for request headers.
- **FLASHLIGHT_SSL_PRIVATE_KEY**: The TLS Private Key (in PEM format) to use for TLS.
- **FLASHLIGHT_SSL_CERTIFICATE**: The TLS Certificate (in PEM format) to use for TLS.
- **FLASHLIGHT_SSL_MODULE**: The SSL module to use with the web server.
- **FLASHLIGHT_SOCKET_TIMEOUT**: The number of seconds to wait for sockets to be established.
- **FLASHLIGHT_SOCKET_QUEUE_SIZE**: The number of connections to allow to queue before being rejected.
- **FLASHLIGHT_ACCEPTED_QUEUE_TIMEOUT**: How long to wait for an HTTP request to be accepted before timing out.
- **FLASHLIGHT_SERVER_MAX_THREADS**: The max number of threads to spawn to handle web requests.

## Performing Backups
Performing regular backups is essential to prevent data loss and ensure data integrity. Django provides the `dumpdata` and `loaddata` management commands to facilitate backups and restores.

### Backing Up Data
Use the `dumpdata` command to export data from the database to a JSON file. This command can be used to back up specific apps or the entire database.

```bash
# Back up the entire database
fl dumpdata > backup.json

# Back up specific apps (e.g., users, auth)
fl dumpdata users auth > backup_users_auth.json
```

### Restoring Data
Use the `loaddata` command to import data from a JSON file into the database. This command can be used to restore data from a backup.

```bash
# Restore data from a backup file
fl loaddata backup.json

# Restore specific apps (e.g., users, auth)
fl loaddata backup_users_auth.json
```

### Custom User Model
Flashlight includes a custom user model in the `users` app. However, the default Django `Group` and `Permission` models are used for managing user roles and permissions. When performing backups and restores, ensure that data from the `users` app and the `auth` app is included to maintain user accounts and permissions.

---

[Previous: User and Group Management](User_and_Group_Management.md) | [Next: Security](Security.md)
