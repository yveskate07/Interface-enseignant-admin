import mysql.connector
import os
from dotenv import load_dotenv

try:
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Récupération des identifiants de connexion depuis les variables d'environnement
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
except Exception as e:
    print('Error: ',e)
else:
    pass


# Fonction pour se connecter à la base de données
def connect_to_db():
    try:
        return mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,  # on essaie de se connecter à la base de données
            database=db_name,
            ssl_disabled=False  # Assurez-vous d'avoir un certificat SSL configuré si vous utilisez SSL/TLS
        )
    except Exception as e:
        print(f'While tempting to connect, an error occured: {e}')
        return None


# Fonction pour exécuter une requête SELECT
def select_query(query, params=None):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    else:
        return None


# Fonction pour exécuter une requête UPDATE
def update_query(query, params=None):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        return "Connexion failed"


# Fonction pour exécuter une requête DELETE
def delete_query(query, params=None):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        return None


# Fonction pour exécuter une requête INSERT
def insert_query(query, params=None):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        return None


def get_infos_from_matricule(matricule):

    temp_dict = dict()

    req1 = f"""SELECT Nom_personne, Prenoms_personne, Email_personne, Statut_personne FROM personne WHERE Matricule_personne="{matricule}";"""
    infos = select_query(req1)


    if infos:

        req2 = f"""SELECT Matiere FROM enseigné_par WHERE Enseignant='{matricule}';"""
        matieres = select_query(req2)
        matieres = tuple(int(i[0]) for i in matieres)

        names_matieres = get_names_from_id(matieres)

        if names_matieres == 'Connection failed':
            return 'Connection failed'

        temp_dict = {"Nom":infos[0][0], "Prenoms":infos[0][1],"Email":infos[0][2], "Statut":infos[0][3], 'Matieres':names_matieres, 'Matricule': matricule}

        return temp_dict

    elif infos == None:
        return 'Connection failed'

    else:
        return "notexist"


def get_names_from_id(ids):

    temp_dict = dict()
    for i in ids:
        req = f"""SELECT classes.Nom_Classe, matieres.Nom_Matiere FROM classes INNER JOIN est_enseignée_dans ON
        classes.Id_Classe = est_enseignée_dans.Classe INNER JOIN matieres ON matieres.Id_matiere = est_enseignée_dans.Matiere
        WHERE est_enseignée_dans.Id = {i};"""

        names = select_query(req)

        if names == None:
            return 'Connection failed'

        temp_dict[" / ".join(names[0])] = [i,get_current_seance_from_id(i)]

    return temp_dict


def get_student_from_matiere_id(matiere_id):

    req = f"""SELECT Nom, Prenom, participe_à.Id_seance, participe_à.Present, seances.Numero_seance, seances.Effectuee FROM etudiant INNER JOIN 
                    participe_à ON etudiant.No_carte_etudiant = participe_à.No_carte_etudiant INNER JOIN seances ON 
                    participe_à.Id_seance = seances.Id WHERE participe_à.Id_seance IN (SELECT Id
                   FROM seances WHERE Matiere={matiere_id}) ORDER BY Nom ASC, Prenom ASC, Id_seance ASC"""

    res = select_query(req)

    if res == None:
        return 'Connection failed'

    students_names = list(set([i[0] + ' ' + i[1] for i in res]))

    students_names.sort()

    students_seances = []

    nbr_seance = len(res) // len(students_names)

    temp_dict = dict()

    num_seance = 1

    for i in res:
        if (res.index(i) + 1) % nbr_seance == 0 and res.index(
                i) > 0:  # chaque fois que i est à la position un multiple de 10
            temp_dict['Séance ' + str(num_seance)] = [i[2], i[3]]
            students_seances.append(temp_dict)
            temp_dict = dict()
            num_seance = 1
        else:
            temp_dict['Séance ' + str(num_seance)] = [i[2], i[3]]
            num_seance += 1

    students_dict = dict(zip(students_names, students_seances))

    return students_dict


def get_current_seance_from_id(id):
    req = f"""SELECT Numero_seance FROM seances WHERE Matiere= {id} AND Effectuee = 0"""
    return select_query(req)[0][0]


def update_datas_to_db(datas, matiere_selected):

    for i in list(datas.keys()):

        name = i.split(' ', maxsplit=1)
        req = f"""SELECT No_carte_etudiant FROM etudiant WHERE Nom = '{name[0]}' AND Prenom = '{name[1]}'"""

        ids = select_query(req)[0][0]

        if ids == None:
            return 'Connection failed'

        for j in list(datas[i].keys()):
            req = f'''UPDATE participe_à SET Present = %s WHERE No_carte_etudiant = %s AND Id_seance = %s;'''
            res = update_query(req, (datas[i][j][1] if datas[i][j][1] == 1 else None,ids,datas[i][j][0]))
            if res == 'Connection Failed':
                return 'Connection Failed'

    req = f"""UPDATE seances SET Effectuee = {1} WHERE Matiere = {matiere_selected} AND Numero_seance = {get_current_seance_from_id(matiere_selected)}"""
    res = update_query(req)
    if res == 'Connection Failed':
        return 'Connection Failed'


def add_new_students(datas):
    req = """INSERT INTO etudiant(No_carte_etudiant, Nom, Prenom, Email, Classe) VALUES (%s, %s, $s, $s, $s)"""
    insert_query(req, (datas['no_carte'], datas['nom'], datas['prenoms'], datas['email'], datas['classe']))


def add_new_personne(datas):
    req = """INSERT INTO personne(Nom_personne, Prenoms_personne, Email_personne, Matricule_personne, Statut_personne) VALUES (%s, %s, %s, %s, %s)"""
    insert_query(req, (i for i in list(datas.values())))


def delete_student(no_carte):
    delete_query(f"""DELETE FROM etudiant WHERE No_carte_etudiant = '{no_carte}'""")


def delete_personne(matricule):
    delete_query(f"""DELETE FROM personne WHERE Matricule_personne = '{matricule}'""")

def get_all_students():
    req = """SELECT etudiant.No_carte_etudiant, etudiant.Nom, etudiant.Prenom, 
    etudiant.Email_etudiant, classes.Nom_Classe FROM etudiant INNER JOIN classes ON etudiant.Classe = classes.Id_classe"""
    return select_query(req)


def get_all_personne():
    req = """SELECT Matricule_personne FROM personne;"""
    res = select_query(req)
    personnes = []
    for i in res:
        personnes.append(get_infos_from_matricule(i[0]))
    return personnes