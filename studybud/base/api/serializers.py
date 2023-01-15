from rest_framework.serializers import ModelSerializer
from base.models import Room
# serializers are classes that take a certain model or object and turn it into json data

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'