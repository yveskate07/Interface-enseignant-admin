import Controller
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SwapTransition
from login_screen import LoginScreen
from main_screen import MainScreen
from admin_screen import AdminScreen



class Application(MDApp):

    edit_mode = BooleanProperty(False) # au demarrage l'application n'est pas en mode edition, donc certaines fonctionnalitées sont verrouillées
    matiere_selected = ''

    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        self.login_screen = LoginScreen(name='Login')
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(self.login_screen)

    def build(self):

        return self.screen_manager

    def get_user_infos(self, matricule):
        self.user_infos = Controller.get_infos_from_matricule(matricule) # les infos de la personne connectée
        return self.user_infos

    def get_students_and_matieres_from_id(self, id):
        return Controller.get_student_from_matiere_id(id)

    def switch_to_screen(self):
        if self.user_infos['Statut'] == 'enseignant': # si l'utilisateur connecté a le statut d'enseignant on lui affiche l'interface dedié aux enseignants
            self.main_screen = MainScreen(name='Main', enseignant=self.user_infos)
            self.screen_manager.transition = SwapTransition()
            self.screen_manager.add_widget(self.main_screen)
            self.screen_manager.current = 'Main'

        elif self.user_infos['Statut'] == 'admin': # si l'utilisateur connecté a le statut d'admin on lui affiche l'interface dedié à l'admin
            self.admin_screen = AdminScreen(name='Admin', admin=self.user_infos)
            self.screen_manager.transition = SwapTransition()
            self.screen_manager.add_widget(self.admin_screen)
            self.screen_manager.current = 'Admin'

    def add_new_student(self, instance):
        no_carte_etudiant = instance.parent.No_carte_etudiant.text
        nom = instance.parent.Nom.text
        prenoms = instance.parent.Prenoms.text
        email = instance.parent.Email.text
        classe = instance.parent.Classe.text
        Controller.add_new_students({'no_carte': no_carte_etudiant, 'nom': nom, 'prenoms': prenoms, 'email': email, 'classe': classe})

    def add_new_person(self, instance):
        Matricule_personne = instance.parent.Matricule_personne.text
        Nom_personne = instance.parent.Nom_personne.text
        Prenoms_personne = instance.parent.Prenoms_personne.text
        Email_personne = instance.parent.Email_personne.text
        Statut_personne = instance.parent.Statut_personne.text
        Controller.add_new_personne({'Matricule_personne':Matricule_personne, 'Nom_personne':Nom_personne,'Prenoms_personne':Prenoms_personne,'Email_personne':Email_personne, 'Statut_personne':Statut_personne})

    def delete_student(self, no_carte):
        Controller.delete_student(no_carte)

    def delete_personne(self, matricule):
        Controller.delete_personne(matricule)

    def get_all_students(self):

        return Controller.get_all_students()

    def get_all_personne(self):

        return Controller.get_all_personne()


    def updating_database(self, datas, mat):
        Controller.update_datas_to_db(datas, mat)

Application().run()
