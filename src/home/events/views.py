import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import markdown

from .forms import (
    QueryForm,
    GlobalContextForm,
    LocalContextForm,
    FileUploadForm,
)
from .models import Event

def http_405():
    return HttpResponse(
        "<p>Method Not Allowed</p>",
        content_type="text/html",
        status=405,
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required()
def docs(request, filename):
    path = settings.FLASHLIGHT_DOCUMENTATION_DIRECTORY.joinpath(filename)
    if path.exists():
        content = path.read_text()
    else:
        content = "Sorry, couldn't find that for you."
    # formatter = markdown.HtmlFormatter(noclasses=True)
    html = markdown.markdown(
        content,
        extensions=[
            'codehilite',
            'fenced_code',
            'tables',
        ],
    )
    return render(
        request,
        'events/markdown_template.html',
        {
            'content': html,
        },
    )

@login_required()
def edit_global_context(request):
    if request.method == "POST":
        global_context_form = GlobalContextForm(request.POST, instance=request.user.global_context)
        if global_context_form.is_valid():
            global_context_form.save()
            messages.add_message(
                request=request,
                level=messages.SUCCESS,
                message="Globals successfully updated."
            )
    elif request.method == "GET":
        global_context_form = GlobalContextForm(instance=request.user.global_context)
    else:
        return http_405()
    return render(
        request,
        "events/edit-global-context.html",
        {
            "global_context_form": global_context_form,
        }
    )

@login_required()
def explore(request):
    log = logging.getLogger(__name__)
    if request.method == "GET":
        if request.GET:
            log.debug(f"Found request.GET: {request.GET}")
        query_form = QueryForm()
        current_context_form = LocalContextForm()
        file_upload_form = FileUploadForm()
    else:
        return http_405()
    return render(
        request,
        'events/explore.html',
        {
            'query_form': query_form,
            'current_context_form': current_context_form,
            'file_upload_form': file_upload_form,
        }
    )

@login_required()
@csrf_exempt
def ingress(request, index, source, sourcetype):
    log = logging.getLogger(__name__)
    if request.method != "POST":
        return http_405()
    host = get_client_ip(request=request)
    event = Event.objects.create(
        index=index,
        host=host,
        source=source,
        sourcetype=sourcetype,
        text=request.body.decode(),
    )
    if settings.FLASHLIGHT_ENABLE_EXTRACTIONS_ON_CREATE:
        event.extract_fields()
    if settings.FLASHLIGHT_ENABLE_PROCESSORSS_ON_CREATE:
        event.process()
    event.save()
    return HttpResponse(
        "<h1>Created!</h1>",
        content_type="text/html",
        status=201,
    )

def index(request):
    if request.method == "GET":
        return render(
            request,
            'project/base.html',
            {},
        )
    else:
        return http_405()
