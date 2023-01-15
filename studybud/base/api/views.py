from rest_framework.decorators import api_view
from rest_framework.response import Response
# using django rest framework for APIs
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # many just means if its going to serialize more than one object
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    # many just means if its going to serialize more than one object
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)