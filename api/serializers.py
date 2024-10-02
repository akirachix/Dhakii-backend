from nurse.models import Nurse
from nurse_admin.models import NurseAdmin
from rest_framework import serializers
from mother.models import Mother
from next_of_kin.models import NextOfKin
from community_health_promoter.models import CHP
from hospital.models import Hospital
from questions.models import EPDSQuestion
from screeningtestscore.models import ScreeningTestScore
from users.models import User
from careguide.models import Careguide  
from answers.models import Answer
from rest_framework import serializers
from careguide.models import Careguide

#nurse
class NurseSerializer(serializers.ModelSerializer):
    """
    NurseSerializer: Serializes the Nurse model for API interactions.
    Converts Nurse objects to and from JSON.
    """
    class Meta:
        model = Nurse
        fields = '__all__'


#nurse_admin

class NurseAdminSerializer(serializers.ModelSerializer):
    """
    NurseAdminSerializer: Serializes the NurseAdmin model for API interactions.
    Converts NurseAdmin objects to and from JSON.
    """
    class Meta:
        model = NurseAdmin
        fields = '__all__'




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
        fields = '__all__'  


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
        fields = '__all__'


class InviteCHPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user_id = serializers.IntegerField()


    def validate_email(self, value):
        return value


    
    
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
        fields = '__all__'



class EPDSQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPDSQuestion
        fields = '__all__'
               

class ScreeningTestScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningTestScore
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            user_role=validated_data.get('user_role', '')
        )
        # Hash the password
        user.set_password(validated_data['password'])
        user.save()
        return user




class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=EPDSQuestion.objects.all())
    class Meta:
        model = Answer
        fields = '__all__'


#caregude

class CareguideSerializer(serializers.ModelSerializer):
    """
    CareguideSerializer: Serializes the Careguide model for API interactions.
    Converts Careguide objects to and from JSON.
    """
    class Meta:
        model = Careguide
        fields = '__all__'




        