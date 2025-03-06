# Using the Web UI

The Flashlight web UI provides an intuitive interface for interacting with your data. This guide covers the key components of the web UI and how to use them effectively.

## Browsable REST API
The Browsable REST API provides access to almost all of the data that Flashlight has. It allows you to interact with the API endpoints directly from your browser.

### Accessing the Browsable REST API
To access the Browsable REST API, navigate to `/api/` in your browser. You will see a list of available endpoints, including:
- `/api/events/`: Manage events.
- `/api/search_commands/`: Manage search commands.
- `/api/queries/`: Manage queries.
- `/api/globals/`: Manage global contexts.
- `/api/locals/`: Manage local contexts.
- `/api/files/`: Manage file uploads.

### Example Usage
To create a new event, send a POST request to `/api/events/` with the following JSON payload:
```json
{
    "text": "Example event text",
    "index": "default",
    "host": "localhost",
    "source": "example_source",
    "sourcetype": "example_sourcetype"
}
```

## Documentation
The Documentation section provides comprehensive information on using and configuring Flashlight. It includes user guides, administration manuals, and API references.

### Accessing the Documentation
To access the documentation, navigate to `/docs/` in your browser. You will find various sections, including:
- User Guide
- Administration Manual
- API Reference

## Explore UI
The Explore UI is a dynamic, universal search interface that allows you to perform interactive searches and visualize the results.

### Accessing the Explore UI
To access the Explore UI, navigate to `/explore/` in your browser. You will see a search bar where you can enter your search queries.

### Example Usage
To search for events containing the word "error", enter the following query in the search bar:
```
search text__icontains="error"
```

## Admin UI
The Admin UI is an administrative dashboard for managing users, data sources, and system settings.

### Accessing the Admin UI
To access the Admin UI, navigate to `/admin/` in your browser. You will need to log in with your admin credentials.

### Example Usage
To create a new user, follow these steps:
1. Log in to the Admin UI.
2. In the "Users" section, click "Add user".
3. Fill in the required fields, such as username, password, and email address.
4. Click "Save" to create the user.

---

[Previous: Getting Started](Getting_Started.md) | [Next: Ingesting Data](Ingesting_Data.md)
