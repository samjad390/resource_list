from rest_framework.serializers import ModelSerializer

from resource_notes.models import ResourceNotes


class ResourceNotesSerializer(ModelSerializer):

    class Meta:
        model = ResourceNotes
        fields = ('id', 'name', 'notes', 'email')
