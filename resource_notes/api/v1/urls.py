from django.urls import path, include
from rest_framework.routers import DefaultRouter

from resource_notes.api.v1.views import ResourceNotesViewSet

app_name = "resource_notes"

router = DefaultRouter()
router.register("resource_notes", ResourceNotesViewSet, basename="resource_notes")

urlpatterns = [
    path("", include(router.urls)),
]