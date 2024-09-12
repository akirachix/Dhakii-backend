

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from mother.models import Mother
from next_of_kin.models import NextOfKin
from .serializers import MotherSerializer, MinimalMotherSerializer
from .serializers import NextOfKinSerializer,MinimalNextOfKinSerializer




class MotherListView(APIView):
    """API View for getting a list of mothers"""
    def get(self, request):
        """You can get a mothers by filtering their first_name"""
        mothers = self.get_queryset()
        serializer = MotherSerializer(mothers, many=True)
        return Response(serializer.data)
    def get_queryset(self):
        queryset = Mother.objects.all()
        first_name = self.request.query_params.get('first_name',None)
        if first_name:
            queryset= queryset.filter(first_name=first_name)
        return queryset

    def post(self, request):
        """This is for adding a mother to the list of mothers"""
        serializer = MotherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotherDetailView(APIView):
    """This APIView is to show the detailed information about the mother"""

    def get(self, request, id):
        """This is for getting a specific mother by using their unique id"""
        mother = Mother.objects.get(id=id)
        serializer = MotherSerializer(mother)
        return Response(serializer.data)

    def patch(self, request, id):
        """This is for updating a specific mother by using their unique id"""
        mother = Mother.objects.get(id=id)
        serializer = MotherSerializer(mother, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class NextOfKinListView(APIView):
    """API View for getting a list of nextofkins"""
    def get(self, request):
        """You can get a nextofkin by filtering their first_name"""
        nextofkins = self.get_queryset()
        serializer = NextOfKinSerializer(nextofkins, many=True)
        return Response(serializer.data)
    def get_queryset(self):
        queryset = NextOfKin.objects.all()
        first_name = self.request.query_params.get('first_name',None)
        if first_name:
            queryset= queryset.filter(first_name=first_name)
        return queryset


    def post(self, request):
        """This is for adding a mother to the list of nextofkins"""
        serializer = NextOfKinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class NextOfKinDetailView(APIView):
    """This APIView is to show the detailed information about the nextofkin"""

    def get(self, request, id):
        """This is for getting a specific nextofkin by using their unique id"""
        nextofkins = NextOfKin.objects.get(id=id)
        serializer = NextOfKinSerializer(nextofkins)
        return Response(serializer.data)

    def patch(self, request, id):
        """This is for updating a specific nextofkin by using their unique id"""
        nextofkins = NextOfKin.objects.get(id=id)
        serializer = NextOfKinSerializer(nextofkins, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



