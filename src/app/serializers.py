from rest_framework.serializers import ModelSerializer
from app.models import Resource


class ResourceSerializer(ModelSerializer):

    ignore_fields = ('modified_by', 'hidden', 'deleted', )

    class Meta:
        model = Resource
        fields = (
            'id',
        )
