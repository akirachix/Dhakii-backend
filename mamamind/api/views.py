from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hospital.models import Hospital
from community_health_promoter.models import CHP
from django.core.mail import send_mail
from .serializers import CHPSerializer
from .serializers import HospitalSerializer
from .utilis import send_invitation_email
from django.contrib.auth.models import User



class HospitalListView(APIView):
    """API View for getting a list of hospitals"""
    
    def get(self, request):
       nurses = self.get_queryset()
       serializer = HospitalSerializer(nurses, many=True)
       return Response(serializer.data)
    

    """You can get a hospitals by filtering their sub_location"""

    def get_queryset(self):
       queryset = Hospital.objects.all()

       sub_location = self.request.query_params.get('sub_location',None)

       if sub_location:
           queryset= queryset.filter(sub_location=sub_location)
       return queryset


    def post(self, request):
        """This is for adding a hospital to the list of hospitals"""
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class HospitalDetailView(APIView):
    """This APIView is to show the detailed information about the hospital"""

    def get(self, request, id):
        """This is for getting a specific hospital by using their unique id"""
        hospitals = Hospital.objects.get(id=id)
        serializer = HospitalSerializer(hospitals)
        return Response(serializer.data)

    def patch(self, request, id):
        """This is for updating a specific hospital by using their unique id"""
        hospital = Hospital.objects.get(id=id)
        serializer = HospitalSerializer(hospital, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CHPListView(APIView):
       """API View for getting a list of CHPs"""
       def get(self, request):
        chps = self.get_queryset()
        serializer = CHPSerializer(chps, many=True)
        return Response(serializer.data)
        
       """You can get a CHP by filtering their sub_location"""
       def get_queryset(self):
        queryset = CHP.objects.all()
        sub_location = self.request.query_params.get('sublocation', None)
        if sub_location:
            queryset = queryset.filter(sub_location__icontains=sub_location)
        return queryset



       def post(self, request):
        """This is for adding a chp to the list of chp"""
        serializer = CHPSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ChpDetailView(APIView):
    """This APIView is to show the detailed information about the chp"""

    def get(self, request, id):
        chps = CHP.objects.get(id=id)
        serializer = CHPSerializer(chps)
        return Response(serializer.data)


    def patch(self, request, id):
        """This is for updating a specific CHP by using their unique id"""
        chps = CHP.objects.get(id=id)
        serializer = CHPSerializer(chps, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class InviteCHPTestView(APIView):
    """
    View to send an email invitation to a CHP based on their email.
    """
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"detail": "Email not provided."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


        chp_instance = CHP.objects.filter(user_id=user.id).first()
        if not chp_instance:
            return Response({"detail": "CHP with this user does not exist."}, status=status.HTTP_404_NOT_FOUND)

        send_invitation_email(email)

        serializer = CHPSerializer(chp_instance)
        return Response({
            "message": "Invitation sent successfully.",
            "CHP_details": serializer.data
        }, status=status.HTTP_200_OK)