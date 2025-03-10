# Installation and Setup

This section covers the system requirements, installation steps, and initial configuration of Flashlight. Proper installation and setup are crucial for ensuring the platform operates efficiently and securely.

## System Requirements
Before installing Flashlight, ensure your system meets the following requirements:

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Database**: SQLite (default), PostgreSQL, or MySQL
- **Disk Space**: Minimum 10 GB of free disk space
- **Memory**: Minimum 4 GB of RAM

## Installation Steps
Follow these steps to install Flashlight:

1. **Download Flashlight**: Download the latest release from the [releases page](#).
2. **Extract Files**: Unzip the downloaded file to your desired location.
3. **Configure Settings**: Copy the example settings and URL files.

   ```
   cp ./flashlight/example-settings.py ./flashlight/settings.py
   cp ./flashlight/example-urls.py ./flashlight/urls.py
   ```

**Important**: It is very important to change your `SECRET_KEY` setting. The default setting will invalidate all sessions and more on every restart of the server. `SECRET_KEY` should be set to a randomly generated string that is kept secret and safe. The `./fl gen-secret-key` will print such a string that can be copied and pasted into your `settings.py`.

**Note**: The `SECRET_KEY_FALLBACKS` can be set to a list of fallback secret keys for a particular Django installation. These are used to allow rotation of the `SECRET_KEY`.

4. **Run Migrations**: Create the database and run migrations.

   ```
   ./fl migrate
   ```

**Note**: The `./fl showmigrations` can be used to check the status of all migrations.

5. **Create Admin User**: Create an admin user for accessing the admin interface.

   ```
   ./fl createsuperuser
   ```

**Note**: The createsuperuser can accept all parameters as Command Line arguments which can be used to facilitate automation.

6. **Start the Server**: Start the Flashlight web server, task scheduler, syslog server and/or file-tail utility.

   ```
   ./fl serve

   ./fl qcluster
   
   ./python/$PYTHON_VERSION/bin/python ./utilities/cli/syslog-receiver.py
   
   ./python/$PYTHON_VERSION/bin/python ./utilities/cli/tail-files.py /var/log/*.log
   ```

**NOTE**: Utilities launched with `fl` are generally configured in settings.py, while utilities in `./utilities/cli/` are generally configured via command line arguments.

## Hosting with CherryPy

Flashlight uses CherryPy to host the Django web app. The `serve` management command starts the CherryPy server to serve the Flashlight web UI.

```bash
./fl serve
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

## Initial Configuration
After installation, perform the initial configuration to tailor Flashlight to your needs. Most configuration settings are found in the `settings.py` file.

## Flashlight Supervisor

Flashlight Supervisor is a very simple service (currently only available on Windows) that is configured via the `FLASHLIGHT_SERVICE_COMMANDS` value in `settings.py`. 

`FLASHLIGHT_SERVICE_COMMANDS` should be a list of commands to run when the Flashlight Supervisor service is started. These commands are supposed to run forever (like `./fl serve` and `./fl qcluster`). Each command will be run and if any of the processes die, that process will be restarted.

### Installing Flashlight Supervisor Service on Windows
If you are on Windows, you can use the following command from the Flashlight directory to install the Flashlight supervisor service. Run the command from an Administrator Command Prompt:

```bash
./python/$PYTHON_VERSION/python ./service.py install
```

After the service is installed, use the Windows Services app to configure and start the service. Alternatively, you can use the `service.py` command to see the available options:

```bash
./python/$PYTHON_VERSION/python ./service.py /?
```

### Installing Flashlight Supervisor Service on Other Platforms
This feature is coming soon. Until then, please consult your operating system's documentation for information on hosting services (Systemd, etc.) to have Flashlight automatically started and monitored.

---

[Previous: Introduction](Introduction.md) | [Next: Configuration](Configuration.md)
