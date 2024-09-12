from django.urls import path
from .views import HospitalDetailView,HospitalListView,ChpDetailView,CHPListView,InviteCHPTestView

urlpatterns = [
    path('hospitals/', HospitalListView.as_view(), name='hospital_list_view'),
    path('hospitals/<int:id>/', HospitalDetailView.as_view(), name='hospital_detail_view'),
    path('chps/', CHPListView.as_view(), name='chp_list_view'),
    path('chps/<int:id>/', ChpDetailView.as_view(), name='chp_detail_view'),
    path('api/invite_chp_test/', InviteCHPTestView.as_view(), name='invite_chp_test'),

]