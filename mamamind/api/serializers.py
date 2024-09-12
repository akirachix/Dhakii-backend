from rest_framework import serializers
from questions.models import EPDSQuestion
from answers.models import Answer
from screeningtestscore.models import ScreeningTestScore
from users.models import User

class EPDSQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPDSQuestion
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    question = EPDSQuestionSerializer()  # Nested serializer

    class Meta:
        model = Answer
        fields = ['id', 'question', 'test', 'score']

class ScreeningTestScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningTestScore
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password','phone_number','user_role']


