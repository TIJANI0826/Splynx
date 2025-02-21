from django.urls import path
from .views import update_ip, check_user, login_user, logout_user, dashboard, admin_dashboard, get_online_users

urlpatterns = [
    path("update_ip/", update_ip, name="update_ip"),
    path("check_user/", check_user, name="check_user"),  # New endpoint
    path("", login_user, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("update_ip/", update_ip, name="update_ip"),
    path("logout/", logout_user, name="logout"),
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),
    path("get_online_users/", get_online_users, name="get_online_users"),
]
