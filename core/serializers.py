from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Batch
from .models import Session
from .models import Attendance

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name']       
    
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'   

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'              