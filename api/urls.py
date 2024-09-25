from django.urls import path
from .views import MotherListView,MotherDetailView
from .views import NextOfKinListView,NextOfKinDetailView
from .views import HospitalDetailView,HospitalListView,ChpDetailView,CHPListView,InviteCHPDetailView
from .views import questions, ScreeningTestScoreListView, ScreeningTestScoreDetailView, AnswerListCreateView, AnswerDetailView
from .views import UserListView, UserDetailView
from . import views
from .views import UserSearchView
from .views import LoginView
from .views import LogoutView
from .views import UserRoleListCreateView
from .views import UserProfileView
from .views import NurseListView, NurseDetailView, NurseAdminListView, NurseAdminDetailView
from api.views import InviteCHPDetailView
from .views import CareguideListView, CareguideDetailView

urlpatterns = [
    path('nurses/', NurseListView.as_view(), name='nurse_list_view'),
    path('nurses/search/', NurseListView.as_view(), name='nurse_search'),
    path('nurses/<int:pk>/', NurseDetailView.as_view(), name='nurse_detail'),

    path('nurse_admins/', NurseAdminListView.as_view(), name='nurse_admin_list_view'),
    path('nurse_admins/search/', NurseAdminListView.as_view(), name='nurse_admin_search'),
    path('nurse_admins/<int:id>/', NurseAdminDetailView.as_view(), name='nurse_admin_detail'),

    path('questions/', questions, name='questions'), 
    path('questions/<int:question_id>/', questions, name='question_detail'),

    path('screeningtestscore/', ScreeningTestScoreListView.as_view(), name='screeningtestscore'),
    path('screeningtestscore/<int:id>/', ScreeningTestScoreDetailView.as_view(), name='screeningtestscore_detail'),
    path('screeningtestscore/date/<int:year>/<int:month>/<int:day>/', ScreeningTestScoreListView.as_view(), name='screeningtestscore_date'),

    path('users/', UserListView.as_view(), name='user_view'), 
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail_view'),  
    path('users/search/', UserSearchView.as_view(), name='user_search_view'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/roles/', UserRoleListCreateView.as_view(), name='user_roles'),
    path('users/profile/', UserProfileView.as_view(), name='user_profile'),

    path('hospitals/', HospitalListView.as_view(), name='hospital_list_view'),
    path('hospitals/<int:id>/', HospitalDetailView.as_view(), name='hospital_detail_view'),

    path('chps/', CHPListView.as_view(), name='chp_list_view'),
    path('chps/<int:id>/', ChpDetailView.as_view(), name='chp_detail_view'),
    path('invite_chp_test/', InviteCHPDetailView.as_view(), name='invite_chp_test'),

    path('mothers/search/', MotherListView.as_view(), name='mother-search'),  
    path('mothers/', MotherListView.as_view(), name='mothers_list_view'),  
    path('mothers/<int:id>/', MotherDetailView.as_view(), name='mother_detail_view'), 

    path('nextofkins/', NextOfKinListView.as_view(), name='nextofkins_list'),  
    path('nextofkins/<int:id>/', NextOfKinDetailView.as_view(),name='nextofkin_detail_view'),
    path('nextofkins/search/', NextOfKinListView.as_view(), name='nextofkin-search'),

    path('answers/', AnswerListCreateView.as_view(), name='answer_list_create'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer_detail'),
    
    path('careguides/', CareguideListView.as_view(), name='careguide-list'),
    path('careguides/<int:id>/', CareguideDetailView.as_view(), name='careguide-detail'),

    

]
