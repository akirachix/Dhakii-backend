
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from questions.models import EPDSQuestion
from .serializers import EPDSQuestionSerializer
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from screeningtestscore.models import ScreeningTestScore
from .serializers import ScreeningTestScoreSerializer
from django.utils.dateparse import parse_date
from answers.models import Answer
from .serializers import AnswerSerializer, EPDSQuestionSerializer

import logging
from users.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import logout




@csrf_exempt
@api_view(['GET', 'POST'])
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
        serializer = ScreeningTestScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScreeningTestScoreDetailView(APIView):
    def get(self, request, pk):
        try:
            screening_test = ScreeningTestScore.objects.get(pk=pk)
            serializer = ScreeningTestScoreSerializer(screening_test)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ScreeningTestScore.DoesNotExist:
            return Response({"error": "Screening test score not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            screening_test = ScreeningTestScore.objects.get(pk=pk)
        except ScreeningTestScore.DoesNotExist:
            return Response({"error": "Screening test not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScreeningTestScoreSerializer(screening_test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
       try:
           answer = Answer.objects.get(pk=pk)
       except Answer.DoesNotExist:
           return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
       serializer = AnswerSerializer(answer)
       return Response(serializer.data)

logger = logging.getLogger(__name__)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  

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
    # Method to handle POST requests for user registration
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class YourProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Your view logic here
        return Response({"message": "You have access to this view!"})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': 'Successfully logged in.',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
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


@csrf_exempt
def generate_token(request):
    user,created =User.objects.get_or_create(username='dummyuser')
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'access':str(refresh.access_token),
        'refresh':str(refresh)
    })
    
    
    
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
                token.blacklist()  # Blacklist the token to prevent reuse
            return Response({'success': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Create a token but do not include it in the response
        token = super().get_token(user)
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Call the super method to get the default response
        response = super().post(request, *args, **kwargs)
        
        # Customize the response to only include the success message
        if response.status_code == status.HTTP_200_OK:
            return Response({"message": "Successfully logged in"}, status=status.HTTP_200_OK)
        
        return response
    
    
roles = ["Admin", "Nurse", "CHP"]

class UserRoleListCreateView(APIView):
    
    # GET request to retrieve the list of roles
    def get(self, request):
        return Response({"roles": roles}, status=status.HTTP_200_OK)

    # POST request to add a new role
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
        # Assuming you have a User model and a UserSerializer to handle user data
        user = request.user  # Get the logged-in user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user  # Get the logged-in user
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
        

