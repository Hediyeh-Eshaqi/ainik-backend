from rest_framework.response import Response
from Charity.models import UserCharity, Charity
from Charity.serializers import CharitySerializer
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class MyCharityView(APIView):
    def get(self, request):
        allObjects = UserCharity.objects.filter(user = request.user)
        charity_qs = Charity.objects.filter(id__in=[obj.charity.id for obj in allObjects])
        serializer = CharitySerializer(instance=charity_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
