from rest_framework import serializers
from nurse.models import Nurse
from nurse_admin.models import NurseAdmin


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