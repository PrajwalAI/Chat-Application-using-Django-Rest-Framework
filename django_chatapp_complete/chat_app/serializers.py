from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message 

# A serializer for user registeration
class Reg_Serializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    username = serializers.CharField()
    password =  serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ('email','username','password','password2')

    def create(self,validated_data):
        del validated_data['password2']
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self,value):

        if value.get('password') != value.get('password2'):
            raise serializers.ValidationError('Both the passwords does not match')
        return value

# A serializer for user messages
class Msg_Serializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    #message = serializers.JSONField()

    class Meta:
        model = Message
        #fields = '__all__'
        fields = ['id', 'sender', 'message' ,'timestamp']



     