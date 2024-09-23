from django.urls import path
from api.views import InviteCHPTestView

urlpatterns = [
    path('invite_chp_test/', InviteCHPTestView.as_view(), name='invite_chp_test'),
]

