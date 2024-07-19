import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from kivymd.uix.screen import MDScreen

class CustomPopupError(Popup):
    pass

class CustomPopupSuccess(Popup):

    def __init__(self, **kwargs):
        super(CustomPopupSuccess, self).__init__(**kwargs)
        self.title_align = 'center'

    def dismiss(self, *_args, **kwargs):
        super().dismiss()
        App.get_running_app().switch_to_screen()


class LoginScreen(MDScreen):
    no_matricule_field = ObjectProperty()
    signin_button = ObjectProperty()

    def check_user(self, instance):
        matricule = self.no_matricule_field.text
        if App.get_running_app().get_user_infos(matricule) not in ['Connection failed', 'notexist']:
            CustomPopupSuccess().open()

        elif App.get_running_app().get_user_infos(matricule) == 'Connection failed':
            CustomPopupError(title='Verifiez votre connexion').open()

        elif App.get_running_app().get_user_infos(matricule) == 'notexist':
            CustomPopupError(title="Cet utilisateur n'existe pas").open()

Builder.load_file(os.path.join(os.path.dirname(__file__), "login_screen.kv"))
