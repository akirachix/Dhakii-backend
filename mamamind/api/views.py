from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from nurse.models import Nurse
from nurse_admin.models import NurseAdmin
from .serializers import NurseSerializer, NurseAdminSerializer
import logging


class NurseListView(APIView):
    """API View for getting a list of nurses"""
    def get(self, request):
        nurses = self.get_queryset()
        serializer = NurseSerializer(nurses, many=True)
        return Response(serializer.data) 

    """You can get a nurse by filtering their sub_location"""
    def get_queryset(self):
        queryset = Nurse.objects.all()
        sub_location = self.request.query_params.get('sub_location',None)
        if sub_location:
            queryset= queryset.filter(sub_location=sub_location)
        return queryset
    
    def post(self, request):
        """This is for adding a nurse to the list of nurses"""
        my_user= Nurse.objects.get_or_create(user_id=request.user_id)[0]
        serializer = NurseSerializer(data=request.data, instance=my_user)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class NurseDetailView(APIView):
    """This APIView is to show the detailed information about the nurse"""
    def get(self, request, pk):
        """This is for getting a specific nurse by using their unique id"""
        nurses = Nurse.objects.get(pk=pk)
        serializer = NurseSerializer(nurses)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        """This is for updating a specific nurse by using their unique id"""
        nurse = Nurse.objects.get(pk=pk)
        serializer = NurseSerializer(nurse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#nurse admin

logger = logging.getLogger(__name__)

class NurseAdminListView(APIView):
    """
    View to list all nurse admins or retrieve by ID, or search nurse admins by name.
    """
    def get(self, request):
        nurse_admins = self.get_queryset()
        serializer = NurseAdminSerializer(nurse_admins, many=True)
        return Response(serializer.data) 

    def get_queryset(self):
        queryset = NurseAdmin.objects.all()
        location = self.request.query_params.get('location',None)
        if location:
            queryset= queryset.filter(location=location)
        return queryset
    

    def post(self, request):
        """This is for adding a nurse admin to the list of nurses"""
        serializer = NurseAdminSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

class NurseAdminDetailView(APIView):
    """
    View to update a specific nurse admin by ID.
    """
    def put(self, request, pk):
        logger.info(f"NurseAdminDetailView PUT request for nurse admin ID: {pk}")
        try:
            nurse_admin = NurseAdmin.objects.get(pk=pk)
        except NurseAdmin.DoesNotExist:
            logger.error(f"Nurse admin with ID {pk} not found for update")
            return Response({"error": "Nurse admin not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NurseAdminSerializer(nurse_admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Nurse admin with ID {pk} updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(f"Failed to update nurse admin with ID {pk}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
