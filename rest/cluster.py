from rest.login import Login
from rest.user_settings import UserSettings


class Cluster:

    def __init__(self):
        self.login = Login()
        self.user_settings = UserSettings()
