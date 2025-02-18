from django.urls import path, include

from rest_framework import routers

from .views import (
    docs,
    index,
    explore,
    edit_global_context,
    ingress,
    # search,
)
from .api import (
    ResolveQueryView,
    SearchCommandViewSet,
    EventViewSet,
    QueryView,
    GlobalContextViewSet,
    LocalContextViewSet,
    FileUploadViewSet,
)    


router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'search_commands', SearchCommandViewSet, basename="SearchCommands")
router.register(r'queries', QueryView)
router.register(r'globals', GlobalContextViewSet)
router.register(r'locals', LocalContextViewSet)
router.register(r'files', FileUploadViewSet)


urlpatterns = [
    path('explore/', explore, name='explore'),
    path('api/query/', ResolveQueryView.as_view(), name='api_query'),
    path('api/', include(router.urls)),
    path('globals/', edit_global_context, name='globals'),
    path('docs/<str:filename>', docs, name='docs'),
    path('ingress/<str:index>/<str:source>/<str:sourcetype>/', ingress, name='ingress'),
    path('', index, name='index'),
]
