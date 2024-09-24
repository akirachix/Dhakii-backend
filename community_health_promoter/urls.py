from django.urls import path
from api.views import InviteCHPDetailView

urlpatterns = [
    path('invite_chp_test/', InviteCHPDetailView.as_view(), name='invite_chp_test'),
]

