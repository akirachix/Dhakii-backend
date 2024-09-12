from rest_framework import serializers
from community_health_promoter.models import CHP
from hospital.models import Hospital

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