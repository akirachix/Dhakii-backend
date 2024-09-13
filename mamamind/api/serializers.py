
from rest_framework import serializers
from mother.models import Mother
from next_of_kin.models import NextOfKin
from community_health_promoter.models import CHP
from hospital.models import Hospital
from questions.models import EPDSQuestion
from answers.models import Answer
from screeningtestscore.models import ScreeningTestScore
from users.models import User


class MotherSerializer(serializers.ModelSerializer):
    """This serializer for the Mother model, including all fields."""

    class Meta:
        """This Meta class is to define mother model and fields for the serializer."""
        model = Mother
        fields = '__all__'


class MinimalMotherSerializer(serializers.ModelSerializer):
    """
    This serializer for the Mother model with minimal fields, including full name.
    """
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_full_name(self, object):
        """
        This function the full names of the mother.
        """
        return f"{object.first_name} {object.last_name}"




class NextOfKinSerializer(serializers.ModelSerializer):
    """This serializer for the Nextofkin model, including all fields."""

    class Meta:
        """This Meta class is to define nextofkin model and fields for the serializer."""
        model = NextOfKin
        fields = '__all__'


class MinimalNextOfKinSerializer(serializers.ModelSerializer):
    """
    This serializer for the nextofkin model with minimal fields, including full name.
    """
    full_name = serializers.SerializerMethodField()  

    def get_full_name(self, object):
        """
        This retrieves the full name of the nextofkin.
        """
        return f"{object.first_name} {object.last_name}"

    class Meta:
        model = NextOfKin
        fields = ['id', 'first_name', 'last_name', 'full_name']  



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

