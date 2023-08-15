from rest_framework.response import Response
from Charity.models import UserCharity, Charity
from Charity.serializers import CharitySerializer
from rest_framework.views import APIView
from rest_framework import status
from Accounts.models import PersonalityComponent, User
from Accounts.serializers import PersonalityComponentsSerializer


# Create your views here.
class MyCharityView(APIView):
    def get(self, request):
        allObjects = UserCharity.objects.filter(user = request.user)
        charity_qs = Charity.objects.filter(id__in=[obj.charity.id for obj in allObjects])
        serializer = CharitySerializer(instance=charity_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserPersonalityComponentsView(APIView):
    def post(self, request):
        user = request.user
        print(user)
        isPermitted = PersonalityComponent.objects.all().filter(user = user).count()
        print(isPermitted)
        if not isPermitted:
            request.data["user"] = user.pk
            serializer = PersonalityComponentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def get(self, request):
        user = request.user
        user_pc = PersonalityComponent.objects.filter(user=user)
        serializer = PersonalityComponentsSerializer(instance=user_pc, many= True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)
        
        