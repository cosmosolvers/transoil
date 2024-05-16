from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from gaz.models import User

from gaz.utilities.permissions import IsLogin


class SignOutViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsLogin]
    
    
    def create(self, request, *args, **kwargs):
        
        user = request.user
        user.is_active = False
        user.save()
        
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'User signed out successfully',
                'data': {}
            },
            status=status.HTTP_200_OK
        )
