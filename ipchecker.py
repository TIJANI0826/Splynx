from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import requests
import geocoder
import platform
from plyer import gps

SERVER_URL = "https://127.0.0.1:8000/update_ip/"

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.user_id_input = TextInput(hint_text="User ID", multiline=False)
        self.login_button = Button(text="Login", on_press=self.login)
        self.status_label = Label(text="Enter details to log in")

        self.add_widget(self.username_input)
        self.add_widget(self.user_id_input)
        self.add_widget(self.login_button)
        self.add_widget(self.status_label)

        self.current_ip = None
        self.latitude = None
        self.longitude = None

    def login(self, instance):
        self.username = self.username_input.text
        self.user_id = self.user_id_input.text

        if not self.username or not self.user_id:
            self.status_label.text = "Enter valid details"
            return

        self.status_label.text = "Logging in..."
        self.get_ip_and_location()
        Clock.schedule_interval(self.check_ip, 30)

    def get_ip_and_location(self):
        """Get IP and GPS location"""
        try:
            ip_info = geocoder.ip("me")
            self.current_ip = ip_info.ip
            self.latitude, self.longitude = ip_info.latlng
        except:
            self.status_label.text = "Failed to get IP location"

        if platform.system() in ["Android", "Linux"]:
            try:
                gps.configure(on_location=self.on_gps_location)
                gps.start()
            except:
                self.status_label.text = "GPS not available"

        self.send_update()

    def on_gps_location(self, **kwargs):
        """Update location from GPS"""
        self.latitude = kwargs.get("lat", self.latitude)
        self.longitude = kwargs.get("lon", self.longitude)
        self.send_update()

    def check_ip(self, dt):
        """Check if IP changes and update"""
        try:
            ip_info = geocoder.ip("me")
            new_ip = ip_info.ip
            if new_ip != self.current_ip:
                self.current_ip = new_ip
                self.latitude, self.longitude = ip_info.latlng
                self.send_update()
        except:
            self.status_label.text = "Failed to check IP"

    def send_update(self):
        """Send the IP and location data to the server"""
        data = {
            "username": self.username,
            "user_id": self.user_id,
            "ip_address": self.current_ip,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

        try:
            response = requests.post(SERVER_URL, json=data)
            if response.status_code == 200:
                self.status_label.text = f"Updated IP: {self.current_ip}"
            else:
                self.status_label.text = "Failed to update server"
        except:
            self.status_label.text = "Could not connect to server"

class UserTrackingApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    UserTrackingApp().run()
