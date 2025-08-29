from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email','phone','first_name','last_name','password','address')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            address=validated_data['address']
        )    
        return user
    
class UserListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','address')
    
class deviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = device_detail
        fields = ('id','report_by','model', 'imei1', 'imei2','missing_date') 
        read_only_fields = ['report_by']

    def validate(self,data):
        request = self.context.get('request')
        if self.instance and self.instance.report_by != request.user:
            raise serializers.ValidationError("You can only edit your own missing report.")
        return data    
    
    def create(self, validated_data):
        validated_data['report_by']=self.context['request'].user
        return super().create(validated_data)
    
class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = device_detail
        fields = ('model',) 
    
class SearchSerializer(serializers.ModelSerializer):
    search_user = UserListSerilizer()
    search_device = DeviceListSerializer()
    class Meta:
        model = search_record
        fields = ('id','search_device','search_date','search_user')

