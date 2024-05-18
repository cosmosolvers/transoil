from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from gaz.models import Location
from gaz.serializers import LocationSerializer

from gaz.utilities.permissions import IsLogin




class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsLogin]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.user.location = serializer.instance
        request.user.save()
        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': 'Location created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.location != instance and not request.user.is_superuser:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'You do not have permission to perform this action',
                    'data': {}
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Location updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.location != instance and not request.user.is_superuser:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'You do not have permission to perform this action',
                    'data': {}
                },
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Location deleted successfully',
                'data': {}
            },
            status=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'You do not have permission to perform this action',
                    'data': {}
                },
                status=status.HTTP_403_FORBIDDEN
            )
        queryset = self.filter_queryset(self.get_queryset())
        serializer = LocationSerializer(queryset, many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Location list',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
