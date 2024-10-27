from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from nurse.models import Nurse
from django.db import IntegrityError
from nurse_admin.models import NurseAdmin
from .serializers import NurseSerializer, NurseAdminSerializer, MotherSerializer, NextOfKinSerializer, CHPSerializer, HospitalSerializer, EPDSQuestionSerializer,ScreeningTestScoreSerializer,AnswerSerializer, EPDSQuestionSerializer,  UserSerializer,AnswerSerializer,InviteCHPSerializer, LocationSerializer
import logging
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model 
from django.contrib.auth import logout
from mother.models import Mother
from next_of_kin.models import NextOfKin
from django.shortcuts import get_object_or_404
from hospital.models import Hospital
from community_health_promoter.models import CHP
from django.core.mail import send_mail
from django.conf import settings 
from django.contrib.auth.models import User
from questions.models import EPDSQuestion
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from screeningtestscore.models import ScreeningTestScore
from django.utils.dateparse import parse_date
from users.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from answers.models import Answer
from community_health_promoter.utils import send_invitation_email
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from careguide.models import Careguide  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ScreeningTestScoreSerializer 
from django.http import Http404
from careguide.models import Careguide
from .serializers import CareguideSerializer
from community_health_promoter.utils import send_invitation_email
from rest_framework.views import APIView
from locations.models import Location
from django.utils import timezone


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
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class NurseDetailView(APIView):
    """This APIView is to show the detailed information about the nurse"""
    def get(self, request, pk):
        """This iRan existing unit tests to verify that no new bugs were introduced.s for getting a specific nurse by using their unique id"""
        nurses = Nurse.objects.get(pk=pk)
        serializer = NurseSerializer(nurses)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        """This is for updating a specific nurse by using their unique id"""
        try:
            nurse = Nurse.objects.get(pk=pk)
        except Nurse.DoesNotExist:
            logger.error('Nurse with pk %d not found for update.', pk)
            return Response({"detail": "Nurse not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = NurseSerializer(nurse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('Nurse with pk %d updated successfully.', pk)
            return Response(serializer.data)
        else:
            logger.error('Nurse update failed for pk %d: %s', pk, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MotherListView(APIView):
    """API View for getting a list of mothers"""
    def get(self, request):
        mothers = self.get_queryset()
        serializer = MotherSerializer(mothers, many=True)
        return Response(serializer.data)

        """You can get a mothers by filtering their first_name"""

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
        """This is for adding a CHP to the list of CHPs"""
        serializer = CHPSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ChpDetailView(APIView):
    """This APIView is to show the detailed information about the CHP"""

    def get(self, request, id):
        try:
            chp = CHP.objects.get(id=id)
            serializer = CHPSerializer(chp)
            return Response(serializer.data)
        except CHP.DoesNotExist:
            return Response({"error": "CHP not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """This is for updating a specific CHP by using their unique id"""
        try:
            chp = CHP.objects.get(id=id)
            serializer = CHPSerializer(chp, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CHP.DoesNotExist:
            return Response({"error": "CHP not found."}, status=status.HTTP_404_NOT_FOUND)

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

    def get(self, request, id):
        """This is for getting a specific nurse admin by using their unique id"""
        nurseAdmin = NurseAdmin.objects.get(id=id)
        serializer = NurseAdminSerializer(nurseAdmin)
        return Response(serializer.data)

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





logger = logging.getLogger(__name__)

class InviteCHPDetailView(APIView):
    """
    View to send an email invitation to a CHP based on their user ID and email.
    """
    def post(self, request):
        logger.info("Received request to send invitation email.")
        
        serializer = InviteCHPSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        email = serializer.validated_data['email']
        
        logger.info("Looking up user with ID: %s", user_id)
        User = get_user_model()
        user = User.objects.filter(id=user_id).first()

        if not user:
            logger.error("User with ID %s does not exist.", user_id)
            return Response({"detail": "User with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if user.email != email:
            logger.error("Email %s does not match the user with ID %s.", email, user_id)
            return Response({"detail": "Email does not match the user."}, status=status.HTTP_400_BAD_REQUEST)

        chp_instance = CHP.objects.filter(user=user).first()
        if not chp_instance:
            logger.error("CHP instance for user %s does not exist.", email)
            return Response({"detail": "CHP with this user does not exist."}, status=status.HTTP_404_NOT_FOUND)

        logger.info("Sending invitation email to: %s", email)

        try:
            send_invitation_email(email)
            logger.info("Invitation email sent to %s.", email)
            return Response({
                "message": "Invitation sent successfully.",
                "CHP_details": CHPSerializer(chp_instance).data  
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Failed to send invitation email to %s. Error: %s", email, str(e))
            return Response({
                "detail": "Failed to send invitation email. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])

def questions(request, question_id=None):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({"error": "File not found."}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['file']
        try:
            data_df = pd.read_csv(file)
            required_columns = ['question', 'option_1', 'first_score', 'option_2', 'second_score', 'option_3', 'third_score', 'option_4', 'forth_score']
            for column in required_columns:
                if column not in data_df.columns:
                    return Response({"error": f"Missing column: {column}"}, status=status.HTTP_400_BAD_REQUEST)
            for _, row in data_df.iterrows():
                EPDSQuestion.objects.create(
                    question=row.get('question'),
                    option_1=row.get('option_1'),
                    first_score=row.get('first_score'),
                    option_2=row.get('option_2'),
                    second_score=row.get('second_score'),
                    option_3=row.get('option_3'),
                    third_score=row.get('third_score'),
                    option_4=row.get('option_4'),
                    forth_score=row.get('forth_score'),
                )
            return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Can't process the file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            if question_id:
                try:
                    question = EPDSQuestion.objects.get(id=question_id)
                    serializer = EPDSQuestionSerializer(question)
                    return Response(serializer.data)
                except EPDSQuestion.DoesNotExist:
                    return Response({"error": f"Question {question_id} not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                questions = EPDSQuestion.objects.all()[:10]
                serializer = EPDSQuestionSerializer(questions, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Can't retrieve data: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class ScreeningTestScoreListView(APIView):
    def get(self, request):
        test_date = request.query_params.get('test_date', None)
        if test_date:
            test_date_obj = parse_date(test_date)
            if test_date_obj:
                screening_tests = ScreeningTestScore.objects.filter(test_date=test_date_obj)
            else:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            screening_tests = ScreeningTestScore.objects.all()
        
        serializer = ScreeningTestScoreSerializer(screening_tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """This is for adding a screening test"""
        serializer = ScreeningTestScoreSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new screening test score
            serializer.save()

            # Return the saved data with a success message
            return Response({
                "message": "Screening test score added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ScreeningTestScoreDetailView(APIView):


    def get(self, request, id):
        """This is for getting a specific nurse admin by using their unique id"""
        screening_test = ScreeningTestScore.objects.get(id=id)
        serializer = ScreeningTestScoreSerializer(screening_test)        
        return Response(serializer.data)

        
    def put(self, request, pk):
        try:
            screening_test = ScreeningTestScore.objects.get(pk=pk)
        except ScreeningTestScore.DoesNotExist:
            return Response({"error": "Screening test score not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScreeningTestScoreSerializer(screening_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Screening test score updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnswerListCreateView(APIView):
   def get(self, request):           

       name = request.query_params.get('name', None)
       if name:
           answers = Answer.objects.filter(question__icontains=name)
       else:
           answers = Answer.objects.all()
       serializer = AnswerSerializer(answers, many=True)
       return Response(serializer.data)
   def post(self, request):
       serializer = AnswerSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class AnswerDetailView(APIView):

    def get(self, request, pk):
        
        """
        Retrieve an answer by ID.
        """
        try:
            answer = Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            logger.error('Answer with ID %d not found.', pk)
            return Response({"detail": "Answer not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AnswerSerializer(answer)
        logger.info('Answer with ID %d retrieved successfully.', pk)
        return Response(serializer.data)

class UserListView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error('User creation failed: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        Retrieve a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved user list.")
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    Handle User detail retrieval, update, and deletion.
    """
    def get(self, request, id):
        
        """
        Retrieve a user by ID.
        """
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            logger.error('User with ID %d not found.', id)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        logger.info('User with ID %d retrieved successfully.', id)
        return Response(serializer.data)
    
    def patch(self, request, id):
        """
        Update a user by ID.
        """
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            logger.error('User with ID %d not found for update.', id)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('User with ID %d updated successfully.', id)
            return Response(serializer.data)
        else:
            logger.error('User update failed for ID %d: %s', id, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            return Response({
                'message': 'Registration successful',
                'user': serializer.data, 
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YourProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response({"message": "You have access to this view!"})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user using email instead of username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # User is authenticated, return user info
            return Response({
                'message': 'Login successful',
                'userId': user.id,
                'role': user.user_role 
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)



class CreateAdminUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            return Response({"detail": "Superuser created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Superuser already exists"}, status=status.HTTP_400_BAD_REQUEST)



    
    
class UserSearchView(APIView):
    def get(self, request):
        first_name = request.query_params.get('first_name', None)
        if first_name:
            users = User.objects.filter(first_name__icontains=first_name)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "first_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  
            return Response({'success': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        




    
    
roles = ["Admin", "Nurse", "CHP"]

class UserRoleListCreateView(APIView):
    
    def get(self, request):
        return Response({"roles": roles}, status=status.HTTP_200_OK)

    def post(self, request):
        new_role = request.data.get('role')
        if new_role:
            if new_role not in roles:
                roles.append(new_role)
                return Response({"message": f"Role '{new_role}' added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Role already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "No role provided"}, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user 
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


#careguide

class CareguideListView(APIView):

    def post(self, request):
        """
        Create a new careguide entry.
        """
        serializer = CareguideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    API View for getting a list of careguides and creating a new careguide.
    """
    
    def get(self, request):
        """
        Get a list of careguides.
        """
        careguides = self.get_queryset()
        serializer = CareguideSerializer(careguides, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        """
        Retrieve a queryset of careguides. Optionally filter by category.
        """
        queryset = Careguide.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class CareguideDetailView(APIView):
    """
    API View for retrieving, updating, and soft-deleting a specific careguide.
    """
    def get(self, request, id):
        
        """
        Retrieve a careguide resource by ID.
        """
        try:
            careguide = Careguide.objects.get(id=id)
        except Careguide.DoesNotExist:
            logger.error('resource with ID %d not found.', id)
            return Response({"detail": "resource not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CareguideSerializer(careguide)
        logger.info('User with ID %d retrieved successfully.', id)
        return Response(serializer.data)

    

    def patch(self, request, id):
        """
        Update a resource by ID.
        """
        try:
            resource = Careguide.objects.get(id=id)
        except Careguide.DoesNotExist:
            logger.error('Resource with ID %d not found for update.', id)
            return Response({"detail": "resource not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CareguideSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('Resource with ID %d updated successfully.', id)
            return Response(serializer.data)
        else:
            logger.error('Resource update failed for ID %d: %s', id, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    def delete(self, request, id):
        """
        Soft-delete a specific careguide by marking it inactive instead of deleting it from the database.
        """
        careguide = Careguide.objects.get(id=id)
        careguide.is_active = False
        careguide.save()
        return Response({"message": "Article deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



#locations
   
logger = logging.getLogger(__name__)

class LocationListView(APIView):
    """Add a new location."""
    def post(self, request):
        logger.info("Received data for adding a new location: %s", request.data)
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Data is valid, saving new location.")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Validation errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    View to list all locations, search by location name, or add a new location.
    """

    def get(self, request):
        """Get a list of all locations or filter by location name."""
        locations = self.get_queryset()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """Get all locations or filter by location name."""
        queryset = Location.objects.all()
        location_name = self.request.query_params.get('location', None)
        if location_name:
            queryset = queryset.filter(location__icontains=location_name)
        return queryset


class LocationDetailView(APIView):
    """
    View to retrieve, update, or delete a specific location by ID.
    """

    def get(self, request, pk):
        """Get a specific location by ID."""
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        """Update a specific location by ID."""
        try:
            location = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Soft delete a location by setting a 'deleted' timestamp.
        """
        try:
            location = Location.objects.get(pk=pk)
            location.deleted_at = timezone.now()
            location.save()
            return Response({"message": "Location soft-deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

        