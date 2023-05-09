from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat_app.serializers import Reg_Serializer , Msg_Serializer
from rest_framework.permissions import IsAuthenticated 
from chat_app.models import Message
import json

class RegisterAPIView(APIView):
    permission_classes = []
    def get(self,request):
        return Response({'Message':'This is Register API'},status=status.HTTP_200_OK)

    def post(self,request):
        try:
            obj = Reg_Serializer(data = request.data)
            if obj.is_valid():
                obj.save()
                return Response({'Message':'User Registered'},status = status.HTTP_200_OK)

            return Response(obj.errors,status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)



class MessageAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data = Message.objects.all()
        
        id = request.query_params.get('id')
        if id is not None:
    
            data = Message.objects.filter(id=id).first()
            serializer = Msg_Serializer(data)
            
            return Response(serializer.data)
        else:
            serializer = Msg_Serializer(data=data, many=True)
            
            serializer.is_valid(raise_exception=False)
            modified_response = {}
            for msg in serializer.data:
                modified_response[msg['id']] = msg
            return Response(modified_response)


    def post(self, request):
        serializer = Msg_Serializer(data={**request.data,"sender":request.user.username})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'Sent'} ,status=status.HTTP_201_CREATED)

    def delete(self,request):
        id = request.query_params.get('id')
        if id is not None:
            message = Message.objects.filter(id=id).first()
            if message.sender != request.user:
                return Response({'message':'users can only delete thier own messeges'},status=status.HTTP_401_UNAUTHORIZED)
            Message.objects.filter(id=id).delete()
            return Response({'message':'Message Deleted'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'messege id not provided'})


