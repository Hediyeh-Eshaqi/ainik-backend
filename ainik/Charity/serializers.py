
from rest_framework import serializers
from .models import Charity, CharityWork

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('id', 'name', 'address', 'description')

class ChairtyWorkSerialezer(serializers.ModelSerializer):
    charityName = CharitySerializer()
    class Meta:
        model = CharityWork
        fields = ('id', 'title', 'type', 'charityName')
        