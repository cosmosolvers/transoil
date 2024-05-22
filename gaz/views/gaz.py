from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gaz.models import Gaz
from gaz.serializers import GazSerializer
from rest_framework import status


@api_view(['GET'])
def gaz_list(request):
    query = Gaz.objects.all()
    data = {}
    if query:
        data = GazSerializer(query, many=True)
    return Response(data)


@api_view(['POST'])
def api_view(request):
    serializer = GazSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    return Response({'details':'invalid data'})
 

@api_view(['PUT', 'PATCH'])
def update_gaz(request, pk):
    try:
        gaz_instance = Gaz.objects.get(pk=pk)
    except Gaz.DoesNotExist:
        return Response({'error': 'Gaz not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = GazSerializer(gaz_instance, data=request.data)
    else:
        serializer = GazSerializer(gaz_instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_gaz(request, pk):
    try:
        gaz_instance = Gaz.objects.get(pk=pk)
    except Gaz.DoesNotExist:
        return Response({'error': 'Gaz not found'}, status=status.HTTP_404_NOT_FOUND)

    gaz_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 
