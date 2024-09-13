from django.urls import path
from .views import NurseListView, NurseDetailView, NurseAdminListView, NurseAdminDetailView

urlpatterns = [
    path('nurses/', NurseListView.as_view(), name='nurse_list_view'),
    path('nurses/search/', NurseListView.as_view(), name='nurse_search'),
    path('nurses/<int:pk>/', NurseDetailView.as_view(), name='nurse_detail'),

    path('nurse_admins/', NurseAdminListView.as_view(), name='nurse_admin_list_view'),
    path('nurse_admins/search/', NurseAdminListView.as_view(), name='nurse_admin_search'),
    path('nurse_admins/<int:pk>/', NurseAdminDetailView.as_view(), name='nurse_admin_detail'),

  ]







