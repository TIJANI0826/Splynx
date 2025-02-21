import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import geocoder
import requests
import json
from plyer import gps
import platform


# Django API endpoints
API_URL_CHECK_USER = "http://127.0.0.1:8000/check_user/"  # Endpoint to verify user
API_URL_UPDATE_IP = "http://127.0.0.1:8000/update_ip/"  # Endpoint to update IP

# class LoginScreen(BoxLayout):
#     def __init__(self, **kwargs):
#         super().__init__(orientation="vertical", **kwargs)

#         self.add_widget(Label(text="Enter Username:"))
#         self.username_input = TextInput(multiline=False)
#         self.add_widget(self.username_input)

#         self.add_widget(Label(text="Enter User ID:"))
#         self.user_id_input = TextInput(multiline=False)
#         self.add_widget(self.user_id_input)

#         self.login_button = Button(text="Login", on_press=self.check_user)
#         self.add_widget(self.login_button)

#         self.status_label = Label(text="")
#         self.add_widget(self.status_label)

#     def check_user(self, instance):
#         """Verify if the user exists in the database before allowing login."""
#         self.username = self.username_input.text.strip()
#         self.user_id = self.user_id_input.text.strip()

#         if not self.username or not self.user_id:
#             self.status_label.text = "Please enter both Username and User ID."
#             return

#         # Send request to Django API to check if user exists
#         data = {"username": self.username, "user_id": self.user_id}
#         try:
#             response = requests.post(API_URL_CHECK_USER, json=data)
#             response_data = response.json()
            
#             if response.status_code == 200 and response_data.get("exists"):
#                 self.status_label.text = "Login successful! Tracking IP..."
#                 self.start_ip_tracking()
#             else:
#                 self.status_label.text = "User not found. Check credentials!"
#         except requests.exceptions.RequestException:
#             self.status_label.text = "Network error! Check connection."

#     def start_ip_tracking(self):
#         """Start continuously checking IP changes."""
#         self.current_ip = None  # Store last known IP
#         Clock.schedule_interval(self.check_ip, 10)  # Check IP every 10 seconds

#     def check_ip(self, dt):
#         """Fetch the user's IP and update if changed."""
#         ip_data = geocoder.ip("me")
#         new_ip = ip_data.ip if ip_data.ok else None

#         if new_ip and new_ip != self.current_ip:
#             self.current_ip = new_ip
#             self.send_ip_update(new_ip)

#     def send_ip_update(self, ip):
#         """Send the new IP to the API."""
#         data = {
#             "username": self.username,
#             "user_id": self.user_id,
#             "ip_address": ip
#         }
#         try:
#             response = requests.post(API_URL_UPDATE_IP, json=data)
#             if response.status_code == 200:
#                 self.status_label.text = f"IP updated: {ip}"
#             else:
#                 self.status_label.text = "Failed to update IP"
#         except requests.exceptions.RequestException:
#             self.status_label.text = "Network error"

# class IPTrackerApp(App):
#     def build(self):
#         return LoginScreen()

# if __name__ == "__main__":
#     IPTrackerApp().run()


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.user_id_input = TextInput(hint_text="User ID", multiline=False)
        self.login_button = Button(text="Login", on_press=self.check_user)
        self.status_label = Label(text="Enter details to log in")

        self.add_widget(self.username_input)
        self.add_widget(self.user_id_input)
        self.add_widget(self.login_button)
        self.add_widget(self.status_label)

        self.current_ip = None
        self.latitude = None
        self.longitude = None

    def check_user(self, instance):
        """Verify if the user exists in the database before allowing login."""
        self.username = self.username_input.text.strip()
        self.user_id = self.user_id_input.text.strip()

        if not self.username or not self.user_id:
            self.status_label.text = "Please enter both Username and User ID."
            return

        # Send request to Django API to check if user exists
        data = {"username": self.username, "user_id": self.user_id}
        try:
            response = requests.post(API_URL_CHECK_USER, json=data)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("exists"):
                self.status_label.text = "Login successful! Tracking IP..."
                self.start_ip_tracking()
            else:
                self.status_label.text = "User not found. Check credentials!"
        except requests.exceptions.RequestException:
            self.status_label.text = "Network error! Check connection."

    def start_ip_tracking(self):
        """Start continuously checking IP changes."""
        self.current_ip = None  # Store last known IP
        Clock.schedule_interval(self.check_ip, 10)  # Check IP every 10 seconds

    def check_ip(self, dt):
        """Fetch the user's IP and update if changed."""
        ip_data = geocoder.ip("me")
        print(ip_data)
        new_ip = ip_data.ip if ip_data.ok else None

        if new_ip and new_ip != self.current_ip:
            self.current_ip = new_ip
            location = ip_data.latlng
            print(location)
            self.latitude, self.longitude = ip_data.latlng
            print(self.latitude, self.longitude)
            print(type(self.latitude))
            print(type(self.longitude))
            self.send_ip_update(new_ip)

    def send_ip_update(self, ip):
        """Send the new IP to the API."""
        data = {
            "username": self.username,
            "user_id": self.user_id,
            "ip_address": ip,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
        }
        headers = {
                    "Content-Type": "application/json",
        }
        try:
            response = requests.post(API_URL_UPDATE_IP, headers=headers,json=data)
            if response.status_code == 200:
                self.status_label.text = f"IP updated: {ip}"
            else:
                self.status_label.text = "Failed to update IP"
        except requests.exceptions.RequestException:
            self.status_label.text = "Network error"
        
    # def get_ip_and_location(self,dt):
    #     """Gets the current IP and location (lat/lon)"""

    #     # 1️⃣ Get IP-based location (Works everywhere)
    #     try:
    #         ip_info = geocoder.ip("me")
    #         self.current_ip = ip_info.ip
    #         self.latitude, self.longitude = ip_info.latlng
    #     except:
    #         self.status_label.text = "Failed to get IP location"

    #     # 2️⃣ Try getting GPS location (Only for Android/iOS)
    #     if platform.system() in ["Android", "Linux"]:  # Plyer GPS works on Android
    #         try:
    #             gps.configure(on_location=self.on_gps_location)
    #             gps.start()
    #         except:
    #             self.status_label.text = "GPS not available"

    #     self.send_update()

    # def on_gps_location(self, **kwargs):
    #     """Gets location from GPS"""
    #     self.latitude = kwargs.get("lat", self.latitude)
    #     self.longitude = kwargs.get("lon", self.longitude)
    #     self.send_update()

    # def check_ip(self):
    #     """Check if IP changes and update"""
    #     try:
    #         ip_info = geocoder.ip("me")
    #         new_ip = ip_info.ip
    #         if new_ip != self.current_ip:
    #             self.current_ip = new_ip
    #             self.latitude, self.longitude = ip_info.latlng
    #             print(f"New IP: {self.current_ip}")
    #             print(f"New Location: {self.latitude}, {self.longitude}")
    #             self.send_update()
    #     except:
    #         self.status_label.text = "Failed to check IP"

    # def start_ip_tracking(self):
    #     """Start continuously checking IP changes."""
    #     self.current_ip = None  # Store last known IP
    #     Clock.schedule_interval(self.get_ip_and_location, 30)  # Check IP every 10 seconds

    # def send_update(self):
    #     """Send the IP and location data to the server"""
    #     data = {
    #         "username": self.username,
    #         "user_id": self.user_id,
    #         "ip_address": self.current_ip,
    #         "latitude": self.latitude,
    #         "longitude": self.longitude,
    #     }

    #     try:
    #         response = requests.post(API_URL_UPDATE_IP, json=data)
    #         if response.status_code == 200:
    #             self.status_label.text = f"Updated IP: {self.current_ip}"
    #         else:
    #             self.status_label.text = "Failed to update server"
    #     except:
    #         self.status_label.text = "Could not connect to server"

class UserTrackingApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    UserTrackingApp().run()
