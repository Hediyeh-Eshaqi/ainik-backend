
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserCharity
from .serializers import CharitySerializer, ChairtyWorkSerialezer

from .models import UserCharity


class CharityCreateView(APIView):
    def post(self, request, user_id):
        serializer = CharitySerializer(data=request.data)
        if serializer.is_valid():
            charity = serializer.save()
            user_charity = UserCharity(user_id=user_id, charity=charity)
            user_charity.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharityWorkView(APIView):
    def post(self, request, charity_id):
        data = request.data
        data["charityName"] = charity_id 
        serializer = ChairtyWorkSerialezer(data=data)
        havePermission = UserCharity.objects.filter(charity = charity_id, user=request.user).exists()
        if havePermission:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)    
        return Response(status=status.HTTP_403_FORBIDDEN)
            