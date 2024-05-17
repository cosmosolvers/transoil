from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from gaz.models import User
from gaz.serializers import SignUpSerializer

from .signin import SignInViewSet




class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        serializer.save()
        serializer.instance.set_password(serializer.instance.password)
        serializer.instance.save()
    
    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return SignInViewSet().authenticated(request, serializer.instance)
