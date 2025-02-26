from django.contrib import admin

from .models import (
    Query,
    Event,
    GlobalContext,
    LocalContext,
    FileUpload,
)

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "user",
        "content",
        "title",
    )
    search_fields = (
        "id",
        "created",
        "modified",
        "user",
        "title",
    )

@admin.register(GlobalContext)
class GlobalContextAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "user",
        "context",
    )
    search_fields = (
        "id",
        "created",
        "modified",
        "user",
        "context",
    )

@admin.register(LocalContext)
class LocalContextAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "user",
        "name",
        "context",
    )
    search_fields = (
        "id",
        "created",
        "modified",
        "user",
        "name",
        "context",
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        # "modified",
        "host",
        "index",
        "source",
        "sourcetype",
        "text",
        "extracted_fields",
    )
    search_fields = (
        "id",
        "created",
        # "modified",
        "host",
        "index",
        "source",
        "sourcetype",
        "text",
        "extracted_fields",
    )

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "created",
        "modified",
        "text",
    )
    search_fields = (
        "id",
        "created",
        "modified",
        "text",
    )
