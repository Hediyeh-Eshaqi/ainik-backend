
from rest_framework import serializers
from .models import Charity, CharityWork

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('id', 'name', 'address', 'description')

class ChairtyWorkSerialezer(serializers.ModelSerializer):
    charityName = CharitySerializer(many=False, read_only=True)
    class Meta:
        model = CharityWork
        fields = ('id', 'title', 'type', 'charityName')
        
    def create(self, validated_data):
        print(validated_data,"&&&&&&&&&")
        charity_data = validated_data.pop('charityName')
        
        charity_work = CharityWork.objects.create(charityName=charity_data, **validated_data)
        return charity_work

        