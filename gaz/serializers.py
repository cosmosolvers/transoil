from rest_framework import serializers

from .models import (
    Depot,
    Gaz,
    Location,
    Qte,
    Recharge,
    Transaction,
    User
)



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'



class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def to_representation(self, instance):
        return {
            'user_id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': [
                instance.phone_number1,
                instance.phone_number2
            ],
            'role': instance.role,
            'img': instance.img.url, # 'http://
            'location': LocationSerializer(instance.location).data,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }



class SignInSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(max_length=32, required=True)
    password = serializers.CharField(max_length=128, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def to_representation(self, instance):
        return {
            'user_id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': [
                instance.phone_number1,
                instance.phone_number2
            ],
            'role': instance.role,
            'img': instance.img.url,
            'location': LocationSerializer(instance.location).data,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'location')
    
    def to_representation(self, instance):
        return {
            'user_id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': [
                instance.phone_number1,
                instance.phone_number2
            ],
            'role': instance.role,
            'img': instance.img.url,
            'location': LocationSerializer(instance.location).data,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        exclude = ('saleman',)
    
    def to_representation(self, instance):
        return {
            'depot_id': instance.id,
            'saleman': UserSerializer(instance.saleman).data['username'],
            'state': instance.state,
            'stock': instance.stock,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class GazSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gaz
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'gaz_id': instance.id,
            'type': instance.type,
            'weight': instance.weight,
            'size': instance.size,
            'price': instance.price,
            'img': instance.img.url,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class QteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qte
        exclude = ('depot', 'gaz')
    
    def to_representation(self, instance):
        return {
            'qte_id': instance.id,
            'depot': instance.depot.id,
            'gaz': instance.gaz.id,
            'quantity': instance.quantity,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        exclude = ('user', 'gaz')
    
    def to_representation(self, instance):
        return {
            'recharge_id': instance.id,
            'user': UserSerializer(instance.user).data['username'],
            'gaz': instance.gaz.id,
            'count': instance.count,
            'state': instance.state,
            'amount': instance.amount,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('recharge', 'status')
    
    def to_representation(self, instance):
        return {
            'pay_id': instance.id,
            'user': UserSerializer(instance.user).data['username'],
            'recharge': instance.recharge.id,
            'phone': instance.phone,
            'fees': instance.fees,
            'commission': instance.commission,
            'total_amount': instance.total_amount,
            'distance': instance.distance,
            'status': instance.status,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }



class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
