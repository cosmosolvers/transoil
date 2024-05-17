from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from gaz.models import User

from gaz.utilities.permissions import IsLogin


class SignOutViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsLogin]
    
    @staticmethod
    def sign_out(request):
        request.user.is_active = False
        request.user.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'User signed out',
                'data': {}
            },
            status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        return SignOutViewSet.sign_out(request)
