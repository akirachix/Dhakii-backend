from rest_framework import serializers
from community_health_promoter.models import CHP
from hospital.models import Hospital
from questions.models import EPDSQuestion
from answers.models import Answer
from screeningtestscore.models import ScreeningTestScore
from users.models import User

class CHPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CHP
        fields = '__all__'

class MinimalCHPSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)  
    sub_location = serializers.SerializerMethodField()

    def get_sub_location(self, obj):
        return obj.sub_location

    class Meta:
        model = CHP
        fields = ['user_id', 'reg_no','sub_location']  
    
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields =  '__all__'

class MinimalHospitalSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, object):
        return f"{object.name} "
    
    class Meta:
        model = Hospital
        fields = ['id', 'name',]



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


