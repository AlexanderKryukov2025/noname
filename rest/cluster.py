from rest.user import User
from rest.login import Login
from rest.events import Events
from rest.devices import Devices
from rest.user_settings import UserSettings


class Cluster:

    def __init__(self):
        self.user = User()
        self.login = Login()
        self.events = Events()
        self.devices = Devices()
        self.user_settings = UserSettings()
