import json
from django import template
from uuid import uuid4

from events.models import Query
from events.util import resolve

register = template.Library()

@register.inclusion_tag('events/query-table.html', takes_context=True)
def query_table(context, query_string, form=None, kwargs=None):
    ctx = {}
    if form and form.is_valid():
        ctx = form.cleaned_data
    else:
        ctx = {}
    if kwargs:
        ctx.update(kwargs)
    query_obj = Query(text=query_string)
    results = query_obj.resolve(request=context["request"], context=ctx)
    results = resolve(results)
    if results:
        fields = [key for key in results[0].keys()]
    else:
        fields = []
    return {
        "fields": fields,
        "results": results,
    }

@register.inclusion_tag('events/query-chart.html', takes_context=True)
def query_chart(context, query_string, form=None, kwargs=None):
    if form and form.is_valid():
        ctx = form.cleaned_data
    else:
        ctx = {}
    if kwargs:
        ctx.update(kwargs)
    query_obj = Query(text=query_string)
    results = query_obj.resolve(request=context["request"], context=ctx)
    try:
        results = resolve(results)[0]
    except KeyError:
        pass

    return {
        "results": results,
        "id": uuid4(),
    }

@register.simple_tag()
def query_table_js():
    return '/static/js/fl-table.js'

@register.simple_tag()
def query_chart_js():
    return '/static/js/fl-chart.js'

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]