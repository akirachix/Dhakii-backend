import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import HttpResponse
from users.models import User
from django.http import JsonResponse, HttpResponseNotAllowed
from authlib.integrations.django_client import OAuth
from django.contrib.auth import authenticate


oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)



# Assuming you're using a method to get tokens, replace this placeholder
def get_tokens(email, password):
    # Replace this with your actual logic to obtain tokens
    return {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQxNDM3NTE0LCJpYXQiOjE3MjYwNzc1MTQsImp0aSI6IjJmYjU4NTAwN2JhNjQyMjhiMTc1NTg3ZGJhYzg1Zjg0IiwidXNlcl9pZCI6N30.h91Xrag7O8D4DX1fFFjDW8v4J_TyI0ueGbKw-j_HtRg",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MjA0MTQzNzUxNCwiaWF0IjoxNzI2MDc3NTE0LCJqdGkiOiI0MWRjZGFkYWU1ZjY0ZTA3ODQzM2Q3NmU1Y2I2NDUzYSIsInVzZXJfaWQiOjd9.EqRdtiPrXYQlwfwDTpsYTzeWHS9mJGU_lSv_K3GbE2Y"
    }

def login(request):
    if request.method == "POST":
        try:
            credentials = json.loads(request.body)
            email = credentials.get("email")
            password = credentials.get("password")
            
            # Debugging logs (avoid in production)
            print(f"Email: {email}")
            print(f"Password: {password}")
            
            # Authenticate the user (replace this with your actual authentication logic)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Obtain tokens (replace with your actual token retrieval logic)
                tokens = get_tokens(email, password)
                
                # Return both success message and tokens
                return JsonResponse({
                    "message": "Successfully logged in",
                    "tokens": tokens
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return JsonResponse({"error": f"Login failed: {str(e)}"}, status=401)
    
    elif request.method == "GET":
        # Render the login page template
        return render(request, "login/index.html")
    
    else:
        return HttpResponseNotAllowed(["POST", "GET"])



def callback(request):
    try:
        token = oauth.auth0.authorize_access_token(request)
        request.session["user"] = token
        return redirect(request.build_absolute_uri(reverse("index")))
    except Exception as e:
        return HttpResponse(f"Error during authentication: {str(e)}")



def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )
    
def check_existing_email(email):
    return User.objects.filter(email=email).exists()

def index(request):
    user = request.session.get("user")
    if not user:
        return redirect(reverse("login"))
    email = user['userinfo']['email']
    if not email:
        return HttpResponse("email not passed in the")
    if not check_existing_email(email):
        return HttpResponse("user does not exist")
    return render(
        request,
        "login/index.html",
        context={
            "session": user,
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )