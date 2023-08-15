from rest_framework import serializers
from Accounts.models import PersonalityComponent

class PersonalityComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityComponent
        fields = ('user', 'gender', 'age', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8')
        