from rest_framework import status, permissions, viewsets
from rest_framework.response import Response

from gaz.models import Gaz, Recharge
from gaz.serializers import RechargeSerializer



class RechargeViewSet(viewsets.ModelViewSet):
    queryset = Recharge.objects.all()
    serializer_class = RechargeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            gaz = Gaz.objects.get(id=self.request.data.get('gaz'))
            serializer.save(
                user=self.request.user,
                gaz=gaz,
                amount=gaz.price * self.request.data.get('count')
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': str(e),
                    'data': {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_update(self, serializer):
        try:
            serializer.save(
                amount=serializer.instance.gaz.price * self.request.data.get('count')
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': str(e),
                    'data': {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            'count': request.data.get('count'),
            'state': request.data.get('state'),
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': 'Recharge created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user:
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
        self.perform_update(serializer)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Recharge updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user and not request.user.is_superuser:
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
                'message': 'Recharge deleted successfully',
                'data': {}
            },
            status=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        queryset = Recharge.objects.filter(user=request.user)
        if not request.user.is_superuser:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'You do not have permission to perform this action',
                    'data': {}
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = RechargeSerializer(queryset, many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Recharge list',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RechargeSerializer(instance)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Recharge detail',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    