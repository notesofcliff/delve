# Configuration

Flashlight uses the Django configuration system, which involves setting various options in the `settings.py` file. This file contains all the configuration settings for your Flashlight instance.

## Overview of Django Configuration
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

## Configuring Email Settings
Django provides a flexible email backend system that allows you to configure various email settings. Here are the steps to configure email settings in `settings.py`:

### SMTP Email Backend
To use an SMTP server for sending emails, configure the following settings in `settings.py`:

```python
# filepath: /flashlight/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587  # Common ports are 587 (TLS) or 465 (SSL)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = 'Flashlight Alerts <alerts@your-domain.com>'
```

### File-Based Email Backend
For development purposes, you can use the file-based email backend, which writes emails to a file instead of sending them. Configure the following settings in `settings.py`:

```python
# filepath: /flashlight/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'  # Change this to your preferred location
```

## Flashlight-Specific Configuration Options
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

## Example Configuration
Here is an example `settings.py` file with some common configurations:

```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flashlight',
    'rest_framework',
    'django_q',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flashlight.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flashlight.wsgi.application'

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = 'Flashlight Alerts <alerts@your-domain.com>'

# Flashlight-specific settings
FLASHLIGHT_AUTORELOAD = True
FLASHLIGHT_SERVER_HOST = 'localhost'
FLASHLIGHT_SERVER_PORT = 8000
FLASHLIGHT_SERVER_LOG_STDOUT = True
FLASHLIGHT_MAX_REQUEST_BODY_SIZE = 10485760  # 10 MB
FLASHLIGHT_MAX_REQUEST_HEADER_SIZE = 8192  # 8 KB
FLASHLIGHT_SSL_PRIVATE_KEY = '/path/to/private_key.pem'
FLASHLIGHT_SSL_CERTIFICATE = '/path/to/certificate.pem'
FLASHLIGHT_SSL_MODULE = 'builtin'
FLASHLIGHT_SOCKET_TIMEOUT = 30
FLASHLIGHT_SOCKET_QUEUE_SIZE = 100
FLASHLIGHT_ACCEPTED_QUEUE_TIMEOUT = 30
FLASHLIGHT_SERVER_MAX_THREADS = 10
FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE = True
FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE = True
FLASHLIGHT_ENABLE_EXTRACTIONS_ON_UPDATE = True
FLASHLIGHT_ENABLE_PROCESSORSS_ON_UPDATE = True
FLASHLIGHT_STRICT_VALIDATION = False
FLASHLIGHT_DOCUMENTATION_DIRECTORY = os.path.join(BASE_DIR, 'doc')
FLASHLIGHT_EXTRACTION_MAP = {
    'default': 'flashlight.extractions.default_extraction',
}
FLASHLIGHT_PROCESSOR_MAP = {
    'default': 'flashlight.processors.default_processor',
}
FLASHLIGHT_NAV_MENU = {
    'Home': 'home',
    'Explore': 'explore',
    'Admin': 'admin:index',
}
FLASHLIGHT_SEARCH_COMMANDS = {
    'search': 'flashlight.search.commands.search',
    'request': 'flashlight.search.commands.request',
    'read_file': 'flashlight.search.commands.read_file',
}
Q_CLUSTER = {
    'name': 'flashlight',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
}
FLASHLIGHT_SERVICE_COMMANDS = [
    'fl serve',
    'fl qcluster',
]
FLASHLIGHT_SERVICE_INTERVAL = 60
```

---

[Previous: Installation and Setup](Installation_and_Setup.md) | [Next: User and Group Management](User_and_Group_Management.md)
