# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserIP
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def login_user(request):
    """Authenticate user using UserIP model."""
    if request.method == "POST":
        username = request.POST.get("username")
        user_id = request.POST.get("user_id")

        try:
            user = UserIP.objects.get(username=username, user_id=user_id)
            request.session["username"] = user.username  # Store session
            request.session["user_id"] = user.user_id
            return redirect("dashboard")
        except UserIP.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")

def dashboard(request):
    """User dashboard where the IP is tracked."""
    if "username" not in request.session:
        return redirect("login")
    return render(request, "dashboard.html", {"username": request.session["username"]})


@csrf_exempt
def update_ip(request):
    """Update the user's IP address, latitude, and longitude if logged in."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ip_address = data.get("ip_address")
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            # Find user and update their IP and location
            user = UserIP.objects.get(username=data.get("username"))
            user.ip_address = ip_address
            user.latitude = latitude
            user.longitude = longitude
            print(user.latitude)
            print(user.longitude)
            print(user.ip_address)
            print(user.username)
            user.save()

            return JsonResponse({"message": "IP and location updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Unauthorized"}, status=403)

def logout_user(request):
    """Logout the user."""
    request.session.flush()
    return redirect("login")



def get_online_users(request):
    """Return a list of online users with their locations."""
    five_minutes_ago = now() - timedelta(minutes=5)
    online_users = UserIP.objects.filter(last_updated__gte=five_minutes_ago)

    user_data = [
        {
            "username": user.username,
            "ip": user.ip_address,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "last_updated": user.last_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for user in online_users
    ]

    return JsonResponse({"users": user_data})


def is_admin(user):
    return user.is_staff  # Allow only admin users

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@csrf_exempt
def check_user(request):
    """Check if the user exists in the database before allowing login."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            user_id = data.get("user_id")

            user_exists = UserIP.objects.filter(user_id=user_id, username=username).exists()
            
            return JsonResponse({"exists": user_exists}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
