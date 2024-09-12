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




















# from django.http import HttpResponse, JsonResponse
# import pandas as pd
# from django.views.decorators.csrf import csrf_exempt
# from questions.models import EPDSQuestion
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from screeningtestscore.models import ScreeningTestScore
# from .serializers import ScreeningTestScoreSerializer
# from django.utils.dateparse import parse_date
# from answers.models import Answer
# from .serializers import AnswerSerializer, EPDSQuestionSerializer

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import HttpResponse, JsonResponse
# import pandas as pd
# from .models import EPDSQuestion, ScreeningTestScore, Answer
# from .serializers import EPDSQuestionSerializer, ScreeningTestScoreSerializer, AnswerSerializer
# from django.utils.dateparse import parse_date
# from django.views.decorators.csrf import csrf_exempt












# @csrf_exempt
# def questions(request, question_id=None):
#     if request.method == 'POST':
#         if 'file' not in request.FILES:
#             return HttpResponse("File not found.", status=400)
        
#         file = request.FILES['file']
#         try:
          
#             data_df = pd.read_csv(file)
            
            
#             required_columns = ['question', 'option_1', 'first_score', 'option_2', 'second_score', 'option_3', 'third_score', 'option_4', 'forth_score']
#             for column in required_columns:
#                 if column not in data_df.columns:
#                     return HttpResponse(f"Missing column: {column}", status=400)
            
            
#             data_df = data_df.head(11)
            
          
#             for _, row in data_df.iterrows():
#                 EPDSQuestion.objects.create(
#                     question=row.get('question'),
#                     option_1=row.get('option_1'),
#                     first_score=row.get('first_score'),
#                     option_2=row.get('option_2'),
#                     second_score=row.get('second_score'),
#                     option_3=row.get('option_3'),
#                     third_score=row.get('third_score'),
#                     option_4=row.get('option_4'),
#                     forth_score=row.get('forth_score'),
#                 )
            
#             return HttpResponse("File uploaded successfully")
        
#         except Exception as e:
#             print(f"Error: {e}")
#             return HttpResponse(f"Can't process the file: {e}", status=500)
    
#     elif request.method == 'GET':
#         try:
#             if question_id:
#                 try:
#                     question = EPDSQuestion.objects.get(id=question_id)
#                     return JsonResponse(question.to_dict(), safe=False)
#                 except EPDSQuestion.DoesNotExist:
#                     return HttpResponse(f"Question {question_id} not found", status=404)
#             else:
               
#                 questions = EPDSQuestion.objects.all()[:10].values()
#                 return JsonResponse(list(questions), safe=False)
        
#         except Exception as e:
#             print(f"Error: {e}")
#             return HttpResponse(f"Can't retrieve data: {e}", status=500)
    
#     return HttpResponse("Invalid request method", status=405)



# class ScreeningTestScoreListView(APIView):
#     def get(self, request):
#         test_date = request.query_params.get('test_date', None)
#         if test_date:
#             test_date_obj = parse_date(test_date)
#             if test_date_obj:
#                 screening_tests = ScreeningTestScore.objects.filter(test_date=test_date_obj)
#             else:
#                 return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             screening_tests = ScreeningTestScore.objects.all()
#         serializer = ScreeningTestScoreSerializer(screening_tests, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ScreeningTestScoreSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ScreeningTestScoreDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             screening_test = ScreeningTestScore.objects.get(pk=pk)
#             serializer = ScreeningTestScoreSerializer(screening_test)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except ScreeningTestScore.DoesNotExist:
#             return Response({"error": "Screening test score not found"}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         try:
#             screening_test = ScreeningTestScore.objects.get(pk=pk)
#         except ScreeningTestScore.DoesNotExist:
#             return Response({"error": "Screening test not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ScreeningTestScoreSerializer(screening_test, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class AnswerListCreateView(APIView):
#    def get(self, request):
#        name = request.query_params.get('name', None)
#        if name:
#            answers = Answer.objects.filter(question__icontains=name)
#        else:
#            answers = Answer.objects.all()
#        serializer = AnswerSerializer(answers, many=True)
#        return Response(serializer.data)
#    def post(self, request):
#        serializer = AnswerSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class AnswerDetailView(APIView):
#    def get(self, request, pk):
#        try:
#            answer = Answer.objects.get(pk=pk)
#        except Answer.DoesNotExist:
#            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
#        serializer = AnswerSerializer(answer)
#        return Response(serializer.data)

