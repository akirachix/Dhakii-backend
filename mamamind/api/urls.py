from django.urls import path
from .views import MotherListView,MotherDetailView
from .views import NextOfKinListView,NextOfKinDetailView

urlpatterns = [
    path('mothers/search/', MotherListView.as_view(), name='mother-search'),  
    path('mothers/', MotherListView.as_view(), name='mothers_list_view'),  
    path('mothers/<int:id>/', MotherDetailView.as_view(), name='mother_detail_view'), 
    path('nextofkins/', NextOfKinListView.as_view(), name='nextofkins_list'),  
    path('nextofkins/<int:id>/', NextOfKinDetailView.as_view(),name='nextofkin_detail_view'),
    path('nextofkins/search/', NextOfKinListView.as_view(), name='nextofkin-search'),

]
