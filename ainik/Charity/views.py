
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserCharity, CharityWork, Charity
from .serializers import CharitySerializer, ChairtyWorkSerialezer
from Accounts.models import User, PersonalityComponent
from Accounts.serializers import publicUserSerializer
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
from sklearn import preprocessing

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
    def get(self, request, charity_id):
        charity = Charity.objects.filter(pk = charity_id)
        if (len(charity)>0):
            creator_user = UserCharity.objects.filter(charity=charity_id)[0]
            chairtyserializer = CharitySerializer(instance=charity, many=True)
            userserializer = publicUserSerializer(creator_user.user)
            charityworks = CharityWork.objects.filter(charityName = charity_id)
            charityworkserializer = ChairtyWorkSerialezer(instance=charityworks, many=True)
            data = {}
            data["creator"] = userserializer.data
            data["info"] = chairtyserializer.data[0]
            data["charity_works"]= charityworkserializer.data
            return Response(data, status=status.HTTP_200_OK)
        return Response([],status=status.HTTP_404_NOT_FOUND)

class CharityWorkView(APIView):
    def post(self, request, charity_id):
        data = request.data
        ch = Charity.objects.filter(pk=charity_id).first()
        data["charityName"] = ch
        print(data,"******")
        havePermission = UserCharity.objects.filter(charity = charity_id, user=request.user).exists()
        if havePermission:
            ChairtyWorkSerialezer.create(self, validated_data=data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, charity_id, work_id):
        havePermission = UserCharity.objects.filter(charity = charity_id, user=request.user).exists()
        if havePermission:
            CharityWork.objects.filter(id=work_id).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

class CharityListView(APIView):
    def get(self, request):
        from_index = request.query_params.get('from')
        to_index = request.query_params.get('to')
        queryset = Charity.objects.all().order_by('-id')[int(from_index):int(to_index)]
        serializer = CharitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class CharityWorkListView(APIView):
    def get(self, request):
        from_index = request.query_params.get('from')
        to_index = request.query_params.get('to')
        queryset = CharityWork.objects.all().order_by('-id')[int(from_index):int(to_index)]
        serializer = ChairtyWorkSerialezer(queryset, many=True)
        return Response(serializer.data)  

# this function will apply the pre processing operations that was applied to the data passed to model to train
def data_pre_process(upc):
    EI = (upc.q1 + (100 - upc.q5))/2
    SN = (upc.q2 + (100 - upc.q6))/2
    TF = (upc.q3 + (100 - upc.q7))/2
    JP = (upc.q4 + (100 - upc.q8))/2
    minmax_scale = joblib.load('minMaxScale.pkl')
    # Apply the scaler object to new data
    new_data = pd.DataFrame({'gender': [upc.gender], 'age': [upc.age], "humanitarianAids":[0],	"education":[0],	"healthCares":[0],	"povertyReduction":[0],	"environmentalProtection":[0],	"animalWelfare":[0], 'EI': [EI], 'SN': [SN], 'TF': [TF], 'JP': [JP],})
    new_data_minmax = minmax_scale.transform(new_data[new_data.columns])
    preprocessed_data = pd.DataFrame({'gender': [new_data_minmax[0][0]], 'age': [new_data_minmax[0][1]], 'EI': [new_data_minmax[0][8]], 'SN': [new_data_minmax[0][9]], 'TF': [new_data_minmax[0][10]], 'JP': [new_data_minmax[0][11]],})
    print(preprocessed_data)
    return preprocessed_data
    
class RecommendedCharityWork(APIView):
    def get(self, request):
        user = request.user
        user_personality_componens = PersonalityComponent.objects.filter(user = user).first()
        data_pre_processd = data_pre_process(user_personality_componens)
        # Load the saved model
        loaded_model = load_model('sequential_model.h5')
        # Use the loaded model to make predictions on new data
        predictions = loaded_model.predict(data_pre_processd)[0]
        print(predictions)
        types = ["1", "2", "3", "4", "5", "6"]
        combined = list(zip(predictions, types))
        combined.sort(reverse=True)
        predictions, types = zip(*combined)
        
        recommendeds = []
        f = CharityWork.objects.all().order_by('-id').filter(type=int(types[0]))[0:3]
        s = CharityWork.objects.all().order_by('-id').filter(type=int(types[1]))[0:2]
        t = CharityWork.objects.all().order_by('-id').filter(type=int(types[2]))[0:1]
        f1 = CharityWork.objects.all().order_by('-id').filter(type=int(types[3]))[0:1]
        s1 = CharityWork.objects.all().order_by('-id').filter(type=int(types[4]))[0:1]
        t1 = CharityWork.objects.all().order_by('-id').filter(type=int(types[5]))[0:1]
        for obj in f:
            recommendeds.append(obj)
        for obj in s:
            recommendeds.append(obj)
        for obj in t:
            recommendeds.append(obj)
        for obj in f1:
            recommendeds.append(obj)
        for obj in s1:
            recommendeds.append(obj)
        for obj in t1:
            recommendeds.append(obj)

        serializer = ChairtyWorkSerialezer(recommendeds, many=True)
        return Response(serializer.data) 
        
         
            
            
        
            