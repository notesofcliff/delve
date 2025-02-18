# Application Developer Guide
This document is for developers looking to build a Flashlight App to integrate one or more data sources into Flashlight in a more tailored way than Flashlight makes possible out-of-the-box.

## Introduction
The most important thing to know about Flashlight Apps is that they are, at their core, Django Apps. This means that the world-class documentation that Django provides, as well as years of questions and answers on sites like Stack Overflow, applies to Flashlight as well.

Be sure to review and refer to the [Django documentation]().

Flashlight is a data platform designed to be lightweight, easy, versatile, and scalable. Flashlight is built on Django and Django Rest Framework.

Flashlight is made up of the following parts:

* **REST API** - A fully-featured and tested REST API providing access to almost all of the data that Flashlight has.
* **Web UI** - A convenient web interface featuring a dynamic, universal search interface, and a simple navigation bar showing available dashboards.
* **Admin UI** - A one-stop-shop administrative dashboard.
* **CLI Utilities** - Utilities that are useful for Flashlight but don't fit neatly into the web-server paradigm, like file-tailing and syslog receivers.
* **An Extensible Query Language** - Designed on the idea of shell pipelines, search commands are provided to access and transform data. Queries are parsed according to shell-style semantics but are also rendered in Jinja 2 context, providing templating capabilities useful for updating a dashboard panel with a form, for instance.

A custom app can tie into every piece of Flashlight.

## Creating a Custom Application

To create a Flashlight application, follow these steps:

1. **Create the Application:**
   Run the following command to create a new Flashlight application:
   ```bash
   ./fl startapp your_app_name
   ```

2. **Register the Application:**
   Add your new application to the `INSTALLED_APPS` list in `./flashlight/settings.py`:
   ```python
   # filepath: ./flashlight/settings.py
   INSTALLED_APPS = [
       // ...existing code...
       'your_app_name',
   ]
   ```

### Creating a Data Model
Creating data models for your app provides a number of benefits. While Flashlight Events are designed to be a flexible, general-purpose data container, custom data models can be tailored to your specific use case:

* Data is stored in a separate database table.
* Allows custom data permissions.
* Allows binding logic to data in Python.
* Almost automatic forms.
* Almost automatic API endpoints.
* Almost automatic data serializers.
* Almost automatic admin interface integration.
* Almost automatic web interface.
* Custom signal handling when data is added, deleted, updated, etc.

The Django project maintains extensive documentation on models, please refer to that documentation for detailed information on everything about models.

Here is an example model, if you named your app `your_app_name`, the file for models would be `./your_app_name/models.py`:
```python
# filepath: ./your_app_name/models.py
from django import models

class MyCustomModel(models.Model):
    str_field = models.CharField(max_length=255)
    text_field = models.TextField()
    int_field = models.IntegerField()
    datetime_field = models.DateTimeField()
    json_field = models.JSONField()
```
