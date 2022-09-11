from rest_framework.viewsets import ModelViewSet

from module.pagination import CustomPagination
from resource_notes.api.v1.serializers import ResourceNotesSerializer
from resource_notes.models import ResourceNotes


class ResourceNotesViewSet(ModelViewSet):
    queryset = ResourceNotes.objects.filter(is_deleted=False)
    serializer_class = ResourceNotesSerializer
    pagination_class = CustomPagination

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
