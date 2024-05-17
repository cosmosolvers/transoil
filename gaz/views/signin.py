from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from gaz.models import User
from gaz.serializers import SignInSerializer

from django.utils import timezone





class SignInViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignInSerializer
    permission_classes = [permissions.AllowAny]
    
    def authenticated(self, request, user: User):
        
        if not user.check_password(request.data.get('password')):
            return Response(
                {
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Invalid password',
                    'data': {}
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user.last_login = timezone.now()
        user.is_active = True
        user.save()
        
        user = User.objects.get(pk=user.id)
        
        serializer = SignInSerializer(user).data
        token = RefreshToken.for_user(user)
        serializer['token'] = {
            'access': str(token.access_token),
            'refresh': str(token)
        }
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'User authenticated successfully',
                'data': serializer
            },
            status=status.HTTP_200_OK
        )
    
    def create(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(username=request.data.get('username'))
            
            return self.authenticated(request, user)
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': str(e),
                    'data': {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['POST'])
    def forgot_password(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
            # envoie d'sms au user avec l'url de reset password
            
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Password reset successfully',
                    'data': {}
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': str(e),
                    'data': {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        try:
            user = ''
            # recuperation du user dans l'url
            user.set_password(request.data.get('password'))
            user.save()
            
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Password reset successfully',
                    'data': {}
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': str(e),
                    'data': {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
