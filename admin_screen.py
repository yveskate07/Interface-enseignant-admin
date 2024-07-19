import os

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen


class CustomLabel(Label):
    pass

class DeleteBtn(MDRaisedButton):
    def __init__(self, **kwargs):
        super(DeleteBtn, self).__init__(**kwargs)

    def on_release(self):
        self.parent.parent.delete()
        self.text = 'Supprimé'
        self.disabled = True

class PersonneLine(GridLayout):
    def __init__(self, personne, **kwargs):
        super(PersonneLine, self).__init__(**kwargs)
        self.personne = personne
        Clock.schedule_once(self.setup, 0)

    def setup(self, dt):
        self.add_widget(CustomLabel(text=self.personne['Nom']))
        self.add_widget(CustomLabel(text=self.personne['Prenoms']))
        self.add_widget(CustomLabel(text=self.personne['Email']))
        self.add_widget(CustomLabel(text=self.personne['Statut']))
        self.add_widget(CustomLabel(text=self.personne['Matricule']))
        lyt = RelativeLayout()
        if self.personne['Matricule'] == App.get_running_app().screen_manager.get_screen('Admin').admin['Matricule']:
            pass
        else:
            lyt.add_widget(DeleteBtn())
        self.add_widget(lyt)

    def delete(self):
        App.get_running_app().delete_personne(self.personne['Matricule'])

class StudentLine(GridLayout):

    def __init__(self, student, **kwargs):
        super(StudentLine,self).__init__(**kwargs)
        self.student = student
        Clock.schedule_once(self.setup, 0)

    def setup(self, dt):
        for i in self.student:
            self.add_widget(CustomLabel(text=i))
        lyt = RelativeLayout()
        lyt.add_widget(DeleteBtn())
        self.add_widget(lyt)

    def delete(self):
        App.get_running_app().delete_student(self.student[0])


class AddingStudentFrame(RelativeLayout):
    no_carte_etudiant = ObjectProperty()
    nom = ObjectProperty()
    prenoms = ObjectProperty()
    email = ObjectProperty()
    classe = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddingStudentFrame, self).__init__(**kwargs)

class AddingPersonneFrame(RelativeLayout):
    nom_personne = ObjectProperty()
    prenoms_personne = ObjectProperty()
    email_personne = ObjectProperty()
    matricule_personne = ObjectProperty()
    statut_personne = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddingPersonneFrame, self).__init__(**kwargs)
class AdminScreen(MDScreen):
    add_student = ObjectProperty()
    add_teacher = ObjectProperty()
    remove_teacher = ObjectProperty()
    remove_student = ObjectProperty()
    nom_admin = ObjectProperty()
    prenoms_admin = ObjectProperty()
    email_admin = ObjectProperty()
    right_layout = ObjectProperty()
    lower_frame = ObjectProperty()
    upper_frame = ObjectProperty()

    def __init__(self, admin, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        self.admin = admin

        self.nom_admin.text = "  " + self.admin['Nom']

        self.prenoms_admin.text = "  " + self.admin['Prenoms']

        self.email_admin.text = "  " + self.admin['Email']

    def display_students(self, instance):
        self.lower_frame.size_hint_y = None
        self.lower_frame.clear_widgets()
        self.students = App.get_running_app().get_all_students()
        if self.lower_frame.size_hint_y == .8:
            self.lower_frame.size_hint_y = None
            self.lower_frame.height = self.lower_frame.minimum_height
        for i in self.students:
            self.lower_frame.add_widget(StudentLine(i))

    def display_personnes(self, instance):
        self.lower_frame.size_hint_y = None
        self.lower_frame.clear_widgets()
        self.personnes = App.get_running_app().get_all_personne()
        if self.lower_frame.size_hint_y == .8:
            self.lower_frame.size_hint_y = None
            self.lower_frame.height = self.lower_frame.minimum_height
        for i in self.personnes:
            self.lower_frame.add_widget(PersonneLine(personne=i))

    def display_add_students_fields(self, instance):
        self.lower_frame.size_hint_y = .8
        self.lower_frame.clear_widgets()
        self.lower_frame.add_widget(AddingStudentFrame())

    def display_add_personnes_fields(self, instance):
        self.lower_frame.size_hint_y = .8
        self.lower_frame.clear_widgets()
        self.lower_frame.add_widget(AddingPersonneFrame())







Builder.load_file(os.path.join(os.path.dirname(__file__), "admin_screen.kv"))