import os

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty, DictProperty, BooleanProperty
from kivymd.uix.selectioncontrol import MDCheckbox



class CheckBoxContainer(GridLayout): # cette classe contiendra tous les checkbox qui appartiennent à la même ligne
    pass

class DropDownItem(Button): # chaque matiere deans la liste deroulante est sous forme de bouton
    pass

class CustomDropDown(DropDown): # liste deroulante
    pass

class SeanceLabel(Label): # Label pour afficher les seances dans l'en-tete
    pass

class StudentNameLabel(Label): # label pour afficher les noms des etudiants
    pass

class CustomCheckBox(MDCheckbox): # classe pour les cases à cocher ou Checkbox

    edit_mode = BooleanProperty(False)
    first_time = True

    def __init__(self,pos, state_,**kwargs):
        super(CustomCheckBox, self).__init__(**kwargs)
        self.position = pos
        self.active = state_ # l'etat du checkbox au demarrage est celui de state_
        self.color_active = '#b290df'
        self.disabled_color = '#c4cbcf'
        Clock.schedule_once(self.update_parent_dictionnary, 0)

    def on_active(self, checkbox, value, *args): # fonction qui s'execute automatiquement lorsque l'etat du Checkbox change
        super().on_active(checkbox, value)
        if not self.first_time:
            if self.position > App.get_running_app().user_infos['Matieres'][App.get_running_app().matiere_selected][1]:
                self.active = False
                MessagePopup(title=f"Vous êtes à la séance {App.get_running_app().user_infos['Matieres'][App.get_running_app().matiere_selected][1]} et ne pouvez modifier les seances ulterieures pour l'instant").open()
            else:
                self.parent.parent.check_list['Séance ' + str(self.position)][1] = 1 if value else 0  # transmet au parent son etat: activé/desactivé
                self.parent.parent.parent.students[self.parent.parent.student_name] = self.parent.parent.check_list


    def on_edit_mode(self, *args):
        if self.position >= App.get_running_app().user_infos['Matieres'][App.get_running_app().matiere_selected][1]: # seules les seances egales ou ulterieures à la seance actuelle sont activées ou desactivés
            self.disabled = not self.edit_mode

    def update_parent_dictionnary(self, dt): # s'execute une seule fois au demarrage pour que l'etat au demarrage de chaque Checkbox se reflete dans le dictionnaire des etudiants
        self.parent.parent.check_list['Séance ' + str(self.position)][1] = 1 if self.active else 0  # transmet au parent son etat: activé/desactivé
        self.parent.parent.parent.students[self.parent.parent.student_name] = self.parent.parent.check_list
        self.first_time = False

class StudentLineCheckout(GridLayout): # cette classe contient à la fois un label pour le nom de l'etudiant mais aussi le CheckBoxContainer correspondant
    checkbox_container = ObjectProperty()
    seance_layout = ObjectProperty()
    student_name = StringProperty("")
    check_list = DictProperty()

    edit_mode = BooleanProperty(False)

    def __init__(self, stu_name, seance: tuple,  **kwargs): # seance = (0,1,0,1,...)
        super(StudentLineCheckout,self).__init__(**kwargs)
        self.student_name = stu_name
        tup1 = ("Séance "+str(i+1) for i in range(len(seance)))
        self.check_list = dict(zip(tup1, seance))  # dictionnaire des presences/absences
        self.resume = {self.student_name:self.check_list} # self.resume = {"student_name":{"Seance 1": [id_seance,present/absent], "Seance 2":[id_seance,present/absent],...
        Clock.schedule_once(self.place_checkboxs, 0)


    def place_checkboxs(self, dt): # fonction pour placer les checkbox
        for i in range(len(list(self.check_list.items()))):
            self.checkbox_container.add_widget(CustomCheckBox(pos=i+1, state_=bool(list(self.check_list.items())[i][1][1])))


    def on_edit_mode(self, *args):
        if self.checkbox_container.children:
            for i in self.checkbox_container.children:
                i.edit_mode = self.edit_mode

class MessagePopup(Popup): # cette classe permet d'afficher des popup

    def __init__(self, **kwargs):
        super(MessagePopup,self).__init__(**kwargs)
        self.title_align = 'center'

class StudentsCkeckoutBody(GridLayout): # cette classe contiendra toutes les lignes labels-checkbox

    edit_mode = BooleanProperty(False)
    students = DictProperty()

    def on_edit_mode(self, *args):
        if self.children:
            for i in self.children:
                i.edit_mode = self.edit_mode

    def save_datas(self): # fonction qui sauvegarde toutes les modifications dans la base de données
        msg = App.get_running_app().updating_database(self.students,
                                                      App.get_running_app().user_infos['Matieres'][App.get_running_app().matiere_selected][0])
        if msg == "Connection failed":
            MessagePopup(title='Verifiez votre connection').open()


class SeanceFrame(BoxLayout): # c'est cette class qui met tout les checkbox en place

    students_checkouts_header = ObjectProperty()
    students_checkouts_body = ObjectProperty()
    nbr_seances = NumericProperty()
    students = DictProperty()

    seances = ListProperty()
    seances_to_display = ListProperty()
    previous_index = NumericProperty(0)
    next_index = NumericProperty(1)

    max_index = NumericProperty() # l'index de la derniere page

    edit_mode = BooleanProperty(False)

    def __init__(self,**kwargs): # students = {'student1':{'Séance 1':0,'Séance 2':1,....}
        super(SeanceFrame, self).__init__(**kwargs)
        self.students = dict()

        Clock.schedule_once(self.start, 0)


    def clean_out_header_and_body(self): # cete fonction enleve tous les widgets de students_checkouts_header et students_checkouts_body # 👍
        if self.students_checkouts_header.children or self.students_checkouts_body.children:
            self.students_checkouts_header.clear_widgets()
            self.students_checkouts_body.clear_widgets()

    def start(self, dt): # fonction qui s'execute une seule fois lorsqu'on choisit une matiere pour la premiere fois
        self.setup()

    def setup(self): # 👍

        if self.students: # si self.students est un ensemble non vide
            self.seances = ["Séance " + str(i+1) for i in range(len(list(self.students.items())[0][1]))]
            self.nbr_seances = len(self.seances)
            self.max_index = self.nbr_seances / 10

            if self.nbr_seances <= 10:
                self.seances_to_display = self.seances # s'il y a moins de 10 seances alors les deux boutons sont desactivés

            else:
                if self.next_index == 1:
                    self.parent.prev_btn.disabled = True # si on est à la premiere page le bouton precedent est desactivé
                self.seances_to_display = self.seances[self.previous_index*10:self.next_index*10]


            # students_checkouts_header
            for i in self.seances_to_display:
                self.students_checkouts_header.add_widget(SeanceLabel(text=i))

            # students_checkouts_body
            for i in list(self.students.keys()):
                self.students_checkouts_body.add_widget(StudentLineCheckout(stu_name=i, seance=tuple(j for j in list(self.students[i].values()))))


    def on_edit_mode(self, *args): # fonction qui s'execute automatiquement lorsque l'on change le mode edition
        self.students_checkouts_body.edit_mode = self.edit_mode

    def check_out_done(self):
        #students = dict()
        if self.students_checkouts_body.children:
            for i in self.students_checkouts_body.children:
                self.students_checkouts_body.students[list(i.resume.items())[0][0]] = list(i.resume.items())[0][1] # à ce niveau toutes les modifications ont été faites et prêtes à être exportées.
            self.students_checkouts_body.save_datas()


    def on_students(self, *args): # fonction qui s'execute automatiquement lorsque le dictionnaire des etudiants est modifié
        self.setup()

class LowerFrame(FloatLayout): # contient tous les widgets en dessous des labels Seances 1, Seance 2 ....
    welcome_label = ObjectProperty()

    edit_mode = BooleanProperty(False)
    seance_frame = ObjectProperty()
    # les boutons du bas
    edit_checkouts_btn = ObjectProperty()
    next_btn = ObjectProperty()
    prev_btn = ObjectProperty()

    def __init__(self, **kwargs):
        super(LowerFrame, self).__init__(**kwargs)
        Clock.schedule_once(self.start,0)

    def start(self, dt):
        self.edit_checkouts_btn.bind(on_press=self.toggle_edit_mode)

    def on_edit_mode(self, *args):
        self.seance_frame.edit_mode = self.edit_mode

    def toggle_edit_mode(self, instance): # changer le text du bouton "Modifier"
        if self.edit_checkouts_btn.text == "Modifier":
            self.edit_mode = True
            self.edit_checkouts_btn.text = "Terminer"
        else:
            self.edit_mode = False
            self.edit_checkouts_btn.text = "Modifier"
            # ensuite faire la mise à jour des données vers la base de données
            self.checkout_done()

    def checkout_done(self): # quand toutes les modifications ont finies d'etre faites
        self.seance_frame.check_out_done()

        MessagePopup(title='Modification terminées').open()


    def on_children(self, *args):
        if self.edit_checkouts_btn:
            if self.welcome_label not in self.children:
                self.edit_checkouts_btn.disabled = False


class MainScreen(MDScreen): # Screen principal pour l'enseignant
    nom_enseignant = ObjectProperty()
    prenoms_enseignant = ObjectProperty()
    email = ObjectProperty()
    right_layout = ObjectProperty()
    lower_frame = ObjectProperty()
    upper_frame = ObjectProperty()

    first_time = True

    dropdownbtn=ObjectProperty() # bouton "Selectionnez une matiere"

    def __init__(self, enseignant, **kwargs): # enseignant = {'matricule':matricule du prof,'matieres':[liste des matricules]}
        super(MainScreen, self).__init__(**kwargs)

        self.dropdown = CustomDropDown()
        self.dropdownbtn.bind(on_release=self.dropdown.open) # ce bouton aura pour action d'ouvrir la liste deroulante

        self.enseignant = enseignant

        self.nom_enseignant.text = "  " + self.enseignant['Nom']

        self.prenoms_enseignant.text = "  " +self.enseignant['Prenoms']

        self.email.text = "  " + self.enseignant['Email']

        self.set_menu()
        self.dropdown.bind(on_select=self.get_text_selected)


    def set_menu(self): # fonction pour disposer les items dans le dropdown
        for i in list(self.enseignant['Matieres'].keys()):
            self.dropdown.add_widget(DropDownItem(text=i))

    def get_text_selected(self, instance, x):
        self.dropdownbtn.text = x
        if self.first_time:
            self.lower_frame.remove_widget(self.lower_frame.welcome_label) # une fois une matiere choisie, le message "Bienvenu" disparait
            self.first_time = False
        matiere_id = self.enseignant['Matieres'][x][0]

        App.get_running_app().matiere_selected = x

        self.lower_frame.seance_frame.clean_out_header_and_body() # on enleve tous les widgets (labels et checkbox) deja presents dans la fenetre

        students = App.get_running_app().get_students_and_matieres_from_id(matiere_id)

        if students != 'Connection failed':

            self.lower_frame.seance_frame.students = students

        else:
            MessagePopup(title='Verifiez votre connection').open()


Builder.load_file(os.path.join(os.path.dirname(__file__), "main_screen.kv"))