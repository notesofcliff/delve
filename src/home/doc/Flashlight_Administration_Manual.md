# Flashlight Administration Manual

## Introduction
This section provides an overview of Flashlight administration and outlines the key responsibilities of an administrator. As an administrator, you will be responsible for installing, configuring, and maintaining the Flashlight platform to ensure it runs smoothly and efficiently.

### Overview of Flashlight Administration
Flashlight is a versatile and powerful platform for ingesting, transforming, and searching through structured, unstructured, and semi-structured data. It allows for interactive searches, dashboards, alerts, and more. As an administrator, you will manage the system's configuration, user access, data ingestion, and overall system health.

### Key Responsibilities of an Administrator
- **Installation and Setup**: Installing Flashlight and configuring it for initial use.
- **User Management**: Creating and managing user accounts, roles, and permissions.
- **Data Management**: Managing data ingress, retention, field extractions, and real-time alert processing.
- **System Configuration**: Configuring system settings, environment variables, and performance tuning.
- **Monitoring and Maintenance**: Monitoring system health, managing logs, and performing backups and restores.
- **Security**: Implementing security best practices, configuring TLS/SSL, and ensuring compliance.
- **Troubleshooting**: Diagnosing and resolving common issues, using diagnostic tools, and accessing support resources.

## Installation and Setup
This section covers the system requirements, installation steps, and initial configuration of Flashlight. Proper installation and setup are crucial for ensuring the platform operates efficiently and securely.

### System Requirements
Before installing Flashlight, ensure your system meets the following requirements:
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Database**: SQLite (default), PostgreSQL, or MySQL
- **Disk Space**: Minimum 10 GB of free disk space
- **Memory**: Minimum 4 GB of RAM

### Installation Steps
Follow these steps to install Flashlight:
1. **Download Flashlight**: Download the latest release from the [releases page](#).
2. **Extract Files**: Unzip the downloaded file to your desired location.
3. **Configure Settings**: Copy the example settings and URL files.
   ```bash
   cp ./flashlight/example-settings.py ./flashlight/settings.py
   cp ./flashlight/example-urls.py ./flashlight/urls.py
   ```
4. **Run Migrations**: Create the database and run migrations.
   ```bash
   ./fl migrate
   ```
5. **Create Admin User**: Create an admin user for accessing the admin interface.
   ```bash
   ./fl createsuperuser
   ```
6. **Start the Server**: Start the Flashlight web server, task scheduler, syslog server and/or file-tail utility.
   ```bash
   ./fl serve
   ./fl qcluster
   ./python/$PYTHON_VERSION/bin/python ./utilities/cli/syslog-receiver.py
   ./python/$PYTHON_VERSION/bin/python ./utilities/cli/tail-files.py /var/log/*.log
   ```

**NOTE**: Utilities launched with `fl` are generally configured in settings.py, while utilities in `./utilities/cli/` are generally configured via command line arguments.

### Initial Configuration
After installation, perform the initial configuration to tailor Flashlight to your needs. Most configuration settings are found in the `settings.py` file.

### Installing Flashlight Supervisor Service on Windows
If you are on Windows, you can use the following command from the Flashlight directory to install the Flashlight supervisor service. This service handles the server, qcluster, and other Flashlight services. Run the command from an Administrator Command Prompt:

```bash
./python/$PYTHON_VERSION/python ./service.py install
```

After the service is installed, use the Windows Services app to configure and start the service. Alternatively, you can use the `service.py` command to see the available options:

```bash
./python/$PYTHON_VERSION/python ./service.py /?
```

### Installing Flashlight Supervisor Service on Other Platforms
This feature is coming soon. Until then, please consult your operating system's documentation for information on hosting services (Systemd, etc.) to have Flashlight automatically started and monitored.

## Configuration
Flashlight uses the Django configuration system, which involves setting various options in the `settings.py` file. This file contains all the configuration settings for your Flashlight instance.

### Overview of Django Configuration
Django configuration is typically done in the `settings.py` file, which includes settings for the database, installed apps, middleware, and more. You can also use environment variables to override settings, which is useful for different environments (e.g., development, testing, production).

### Using Environment Variables
To use environment variables in Django, you can use the `os` module to read environment variables and set them in `settings.py`. For example:

```python
import os

DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'flashlight'),
        'USER': os.getenv('DB_USER', 'flashlight_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Flashlight-Specific Configuration Options
Flashlight has several specific configuration options that you can set in `settings.py`:

- **FLASHLIGHT_AUTORELOAD**: If `True`, Python source code changes will result in a reload of the server to apply the new code.
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
- **FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE**: If `True`, Flashlight will run field extraction functions on events based on sourcetype when the events are created.
- **FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE**: If `True`, Flashlight will run processor functions on events based on sourcetype when the events are created.
- **FLASHLIGHT_ENABLE_EXTRACTIONS_ON_UPDATE**: If `True`, Flashlight will run field extraction functions on events based on sourcetype when the events are updated.
- **FLASHLIGHT_ENABLE_PROCESSORSS_ON_UPDATE**: If `True`, Flashlight will run processor functions on events based on sourcetype when the events are updated.
- **FLASHLIGHT_STRICT_VALIDATION**: (Experimental) If enabled, type checks will be performed on the values passed between search commands, which can cause crashes.
- **FLASHLIGHT_DOCUMENTATION_DIRECTORY**: The directory where the Flashlight documentation will be served from.
- **FLASHLIGHT_EXTRACTION_MAP**: A mapping of sourcetype to field extraction function to be called on each event with the specified sourcetype.
- **FLASHLIGHT_PROCESSOR_MAP**: A mapping of sourcetype and processor function to be called on each event with the specified sourcetype.
- **FLASHLIGHT_NAV_MENU**: A mapping of title and view to add to the side nav of the Flashlight web UI.
- **FLASHLIGHT_SEARCH_COMMANDS**: A mapping of search commands to their implementations.
- **Q_CLUSTER**: Not specific to Flashlight, but is the task scheduler used by Flashlight.
- **FLASHLIGHT_SERVICE_COMMANDS**: The commands specifying the processes for the Flashlight Supervisor Service to spawn and keep alive.
- **FLASHLIGHT_SERVICE_INTERVAL**: The number of seconds to sleep before the next check on the processes for the Flashlight Supervisor Service.

## User and Group Management
Creating users and groups, as well as assigning permissions, is an essential part of managing your Flashlight instance. This section covers how to perform these tasks through the Django Admin Interface.

### Creating Users
To create a new user, follow these steps:

1. Log in to the Django Admin Interface using your admin credentials.
2. In the "Users" section, click "Add user".
3. Fill in the required fields, such as username, password, and email address.
4. Click "Save" to create the user.

### Creating Groups
To create a new group, follow these steps:

1. Log in to the Django Admin Interface using your admin credentials.
2. In the "Groups" section, click "Add group".
3. Enter a name for the group.
4. Select the permissions you want to assign to the group.
5. Click "Save" to create the group.

### Assigning Permissions
To assign permissions to a user or group, follow these steps:

1. Log in to the Django Admin Interface using your admin credentials.
2. Navigate to the "Users" or "Groups" section, depending on whether you want to assign permissions to a user or a group.
3. Click on the user or group you want to modify.
4. In the "Permissions" section, select the permissions you want to assign.
5. Click "Save" to apply the changes.

### Adding a User to a Group
To add a user to a group, follow these steps:

1. Log in to the Django Admin Interface using your admin credentials.
2. Navigate to the "Users" section and click on the user you want to add to a group.
3. In the "Groups" section, select the group(s) you want to add the user to.
4. Click "Save" to apply the changes.

By following these steps, you can effectively manage users, groups, and permissions in your Flashlight instance.

## Monitoring and Maintenance
Monitoring and maintaining Flashlight is crucial for ensuring its smooth operation and performance. This section covers various aspects of monitoring and maintenance, including using Django management commands and performing backups.

### Monitoring System Health
Monitoring the health of your Flashlight instance involves keeping an eye on system resources, application logs, and performance metrics. Here are some key areas to monitor:

- **System Resources**: Monitor CPU, memory, and disk usage to ensure the system has enough resources to handle the workload.
- **Application Logs**: Regularly check application logs for errors, warnings, and other important messages. Logs can be found in the `log` directory.
- **Performance Metrics**: Monitor response times, request rates, and other performance metrics to identify potential bottlenecks and optimize performance. The logging system can be fine-tuned to gain insights into these metrics without allowing the logs to become overly verbose.

### Using Django Management Commands
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

#### Django Extension Commands
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

### Hosting with CherryPy
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

### Performing Backups
Performing regular backups is essential to prevent data loss and ensure data integrity. Django provides the `dumpdata` and `loaddata` management commands to facilitate backups and restores.

#### Backing Up Data
Use the `dumpdata` command to export data from the database to a JSON file. This command can be used to back up specific apps or the entire database.

```bash
# Back up the entire database
fl dumpdata > backup.json

# Back up specific apps (e.g., users, auth)
fl dumpdata users auth > backup_users_auth.json
```

#### Restoring Data
Use the `loaddata` command to import data from a JSON file into the database. This command can be used to restore data from a backup.

```bash
# Restore data from a backup file
fl loaddata backup.json

# Restore specific apps (e.g., users, auth)
fl loaddata backup_users_auth.json
```

### Custom User Model
Flashlight includes a custom user model in the `users` app. However, the default Django `Group` and `Permission` models are used for managing user roles and permissions. When performing backups and restores, ensure that data from the `users` app and the `auth` app is included to maintain user accounts and permissions.

## Security
Implementing security best practices is crucial for protecting your Flashlight instance and the data it processes. This section covers key security aspects, including the `SECRET_KEY` setting, configuring TLS, and other relevant security practices.

### SECRET_KEY Setting
The `SECRET_KEY` setting in `settings.py` is a critical component of your Django project's security. It is used for cryptographic signing and should be kept secret. Here are some best practices for managing the `SECRET_KEY`:

- **Keep It Secret**: Never share your `SECRET_KEY` or commit it to version control.
- **Use a Strong Key**: Generate a strong, random key. You can use tools like `django-admin startproject` to generate a new key.
- **Environment Variables**: Store the `SECRET_KEY` in an environment variable and read it in `settings.py`. For example:
  ```python
  import os

  SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')
  ```

### Configuring TLS
Transport Layer Security (TLS) is essential for securing data in transit between clients and the Flashlight server. Flashlight provides several configuration options for enabling and configuring TLS:

- **FLASHLIGHT_SSL_PRIVATE_KEY**: The path to the TLS private key file (in PEM format).
- **FLASHLIGHT_SSL_CERTIFICATE**: The path to the TLS certificate file (in PEM format).
- **FLASHLIGHT_SSL_MODULE**: The SSL module to use with the web server.

To configure TLS, set these options in `settings.py`:

```python
FLASHLIGHT_SSL_PRIVATE_KEY = '/path/to/private_key.pem'
FLASHLIGHT_SSL_CERTIFICATE = '/path/to/certificate.pem'
FLASHLIGHT_SSL_MODULE = 'builtin'
```

### Additional Security Practices
- **Use HTTPS**: Ensure that your Flashlight instance is accessible only over HTTPS to protect data in transit.
- **Update Regularly**: Keep your Flashlight instance and its dependencies up to date with the latest security patches.
- **Restrict Access**: Use firewalls and access controls to restrict access to your Flashlight instance.
- **Monitor Logs**: Regularly monitor application and server logs for suspicious activity.
- **Database Security**: Secure your database by using strong passwords, enabling encryption, and restricting access.

## Troubleshooting
Troubleshooting is an essential part of maintaining a Flashlight instance. This section covers common troubleshooting techniques for Flashlight, Django, DjangoRestFramework, and django_extensions.

### Common Issues and Solutions
Here are some common issues you might encounter and their solutions:

- **Server Not Starting**: Check the logs for error messages. Ensure that all required services (e.g., database) are running.
- **Database Connection Issues**: Verify the database settings in `settings.py`. Ensure that the database server is running and accessible.
- **Permission Errors**: Ensure that the user running the Flashlight server has the necessary permissions to access files and directories.
- **Missing Migrations**: Run `fl showmigrations` and `fl migrate` to ensure that all database migrations are applied.

### Using Django Debug Toolbar
The Django Debug Toolbar, which comes pre-installed but disabled, is a helpful tool for debugging and profiling Django applications. To enable it, follow these steps:

1. Add it to the `INSTALLED_APPS` and `MIDDLEWARE` settings in `settings.py`:
   ```python
   INSTALLED_APPS = [
       // ...existing code...
       'debug_toolbar',
   ]

   MIDDLEWARE = [
       // ...existing code...
       'debug_toolbar.middleware.DebugToolbarMiddleware',
   ]
   ```

2. Configure the internal IPs in `settings.py`:
   ```python
   INTERNAL_IPS = ['127.0.0.1']
   ```

3. Include the debug toolbar URLs in your `urls.py`:
   ```python
   from django.urls import include, path

   urlpatterns = [
       // ...existing code...
       path('__debug__/', include('debug_toolbar.urls')),
   ]
   ```

**Note**: The Django Debug Toolbar can be misleading because it only really engages during page loads, so AJAX calls (like submitting a search in the Explore UI) may not show in the results.

### Using Django Extensions
Django Extensions provides additional management commands and utilities for Django projects. To install and enable it, follow these steps:

1. Install Django Extensions:
   ```bash
   pip install django-extensions
   ```

2. Add it to the `INSTALLED_APPS` setting in `settings.py`:
   ```python
   INSTALLED_APPS = [
       // ...existing code...
       'django_extensions',
   ]
   ```

3. Use the additional management commands provided by Django Extensions. Some useful commands include:
   - **`shell_plus`**: An enhanced version of the Django shell with autoloading of models and other conveniences.
     ```bash
     fl shell_plus
     ```
   - **`graph_models`**: Creates a GraphViz dot file (or JSON file) for the specified app names.
     ```bash
     fl graph_models events
     ```

### Checking Logs
Regularly check the application logs for errors, warnings, and other important messages. Logs can be found in the `log` directory. You can also configure logging settings in `settings.py` to customize log levels, formats, and handlers.

### Accessing Support Resources
If you encounter issues that you cannot resolve, consider accessing support resources such as:

- **Django Documentation**: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- **DjangoRestFramework Documentation**: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- **Django Extensions Documentation**: [https://django-extensions.readthedocs.io/](https://django-extensions.readthedocs.io/)
- **Flashlight Documentation**: Included with every Flashlight documentation in the `doc` directory, available in the Flashlight Web UI (default http://127.0.0.1:8000/docs/) and in the [Github Repository](https://github.com/DelveCorp/flashlight/blob/main/src/home/doc/index)
- **Flashlight Community**: Refer to the [Community](Community.md) section for information on reporting issues, submitting feature requests, and contacting the project maintainers.

By following these troubleshooting techniques and utilizing available resources, you can effectively diagnose and resolve issues with your Flashlight instance.
