
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserCharity, CharityWork, Charity
from .serializers import CharitySerializer, ChairtyWorkSerialezer



class CharityView(APIView):
    def post(self, request):
        user_id = request.user.id
        serializer = CharitySerializer(data=request.data)
        if serializer.is_valid():
            charity = serializer.save()
            user_charity = UserCharity(user_id=user_id, charity=charity)
            user_charity.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, charity_id):
        user = request.user
        havePermission = UserCharity.objects.filter(charity = charity_id, user = user).exists()
        if havePermission:
            Charity.objects.filter(id=charity_id).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

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
    def delete(self, request, charity_id, work_id):
        havePermission = UserCharity.objects.filter(charity = charity_id, user=request.user).exists()
        if havePermission:
            CharityWork.objects.filter(id=work_id).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
            
            
        
            