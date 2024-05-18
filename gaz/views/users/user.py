from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from gaz.models import User
from gaz.serializers import UserSerializer

from gaz.utilities.permissions import IsLogin



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsLogin]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance and not request.user.is_superuser:
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
                'message': 'User updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance and not request.user.is_superuser:
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
                'message': 'User deleted successfully',
                'data': {}
            },
            status=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = UserSerializer(queryset, many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'User list',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'User detail',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
