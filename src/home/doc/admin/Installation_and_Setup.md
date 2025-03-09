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

**Important**: It is very important to change your `SECRET_KEY` setting.

4. **Run Migrations**: Create the database and run migrations.

   ```
   ./fl migrate
   ```

5. **Create Admin User**: Create an admin user for accessing the admin interface.

   ```
   ./fl createsuperuser
   ```

6. **Start the Server**: Start the Flashlight web server, task scheduler, syslog server and/or file-tail utility.

   ```
   ./fl serve
   ./fl qcluster
   ./python/$PYTHON_VERSION/bin/python ./utilities/cli/syslog-receiver.py
   ./python/$PYTHON_VERSION/bin/python ./utilities/cli/tail-files.py /var/log/*.log
   ```

**NOTE**: Utilities launched with `fl` are generally configured in settings.py, while utilities in `./utilities/cli/` are generally configured via command line arguments.

## Initial Configuration
After installation, perform the initial configuration to tailor Flashlight to your needs. Most configuration settings are found in the `settings.py` file.

## Installing Flashlight Supervisor Service on Windows
If you are on Windows, you can use the following command from the Flashlight directory to install the Flashlight supervisor service. This service handles the server, qcluster, and other Flashlight services. Run the command from an Administrator Command Prompt:

```bash
./python/$PYTHON_VERSION/python ./service.py install
```

After the service is installed, use the Windows Services app to configure and start the service. Alternatively, you can use the `service.py` command to see the available options:

```bash
./python/$PYTHON_VERSION/python ./service.py /?
```

## Installing Flashlight Supervisor Service on Other Platforms
This feature is coming soon. Until then, please consult your operating system's documentation for information on hosting services (Systemd, etc.) to have Flashlight automatically started and monitored.

---

[Previous: Introduction](Introduction.md) | [Next: Configuration](Configuration.md)
