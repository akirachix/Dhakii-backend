
from rest_framework import serializers
from mother.models import Mother
from next_of_kin.models import NextOfKin


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