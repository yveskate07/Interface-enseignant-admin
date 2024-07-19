<?php

session_start();


if(!isset($_GET['semestre'])){
    if(isset($_GET['selectd-semestre'])){ // dans le cas où l'on accède à cette page depuis la page Accueil/index.php en appuyant sur afficher
        require 'dbh.ext.php';
        $_SESSION['semestre'] = $_GET['selectd-semestre'];
        $sql = "SELECT `participe_à`.`Present`, seances.Numero_seance, seances.Effectuee, matieres.Nom_Matiere FROM `participe_à` INNER JOIN seances 
        ON `participe_à`.`Id_seance` = seances.Id INNER JOIN `est_enseignée_dans` ON seances.Matiere = `est_enseignée_dans`.`Id` INNER JOIN 
        matieres ON `est_enseignée_dans`.`Matiere` = matieres.Id_matiere WHERE No_carte_etudiant = '".$_SESSION['No_carte']."' AND `participe_à`.`Id_seance` 
        IN (SELECT Id FROM seances WHERE Matiere IN (SELECT Id FROM est_enseignée_dans WHERE Matiere IN (SELECT Id_matiere FROM matieres WHERE matieres.Semestre = ".$_SESSION['semestre']."))) 
        ORDER BY seances.Numero_seance ASC;
        ";

        $res = mysqli_query($conn, $sql);

        $data = mysqli_fetch_all($res, MYSQLI_ASSOC);

        $_SESSION['cols_names'] = array_unique(array_column($data, 'Nom_Matiere'));
        
        $_SESSION['datas'] = $data;

        header('Location: ../Accueil/index.php?semestre='.$_SESSION['semestre']);
        exit();
    }else{
        header('Location: ../Connexion/index.php?message=semestrenotdefined');
        exit();
    }
    
}else{
    if(!isset($_SESSION['No_carte'])){
        header('Location:../Connexion/index.php?message=No_cartenotdefined');
        exit();
    }else{
        require 'dbh.ext.php';
        if(isset($_GET['selectd-semestre'])){ // dans le cas où l'on accède à cette page depuis la page Accueil/index.php
            $_SESSION['semestre'] = $_GET['selectd-semestre'];
            $sql = "SELECT `participe_à`.`Present`, seances.Numero_seance, seances.Effectuee, matieres.Nom_Matiere FROM `participe_à` INNER JOIN seances 
            ON `participe_à`.`Id_seance` = seances.Id INNER JOIN `est_enseignée_dans` ON seances.Matiere = `est_enseignée_dans`.`Id` INNER JOIN 
            matieres ON `est_enseignée_dans`.`Matiere` = matieres.Id_matiere WHERE No_carte_etudiant = '".$_SESSION['No_carte']."' AND `participe_à`.`Id_seance` 
            IN (SELECT Id FROM seances WHERE Matiere IN (SELECT Id FROM est_enseignée_dans WHERE Matiere IN (SELECT Id_matiere FROM matieres WHERE matieres.Semestre = ".$_SESSION['semestre']."))) 
            ORDER BY seances.Numero_seance ASC;
            ";

            $res = mysqli_query($conn, $sql);

            $data = mysqli_fetch_all($res, MYSQLI_ASSOC);

            $_SESSION['cols_names'] = array_unique(array_column($data, 'Nom_Matiere'));
            
            $_SESSION['datas'] = $data;

            //header('Location: test.php');

            header('Location: ../Accueil/index.php?semestre='.$_SESSION['semestre']);
            exit();
        }else{
            $_SESSION['semestre'] = $_GET['semestre']; // dans le cas où l'on accède à cette page depuis la page Connexion/index.php
            $sql = "SELECT `participe_à`.`Present`, seances.Numero_seance, seances.Effectuee, matieres.Nom_Matiere FROM `participe_à` INNER JOIN seances 
            ON `participe_à`.`Id_seance` = seances.Id INNER JOIN `est_enseignée_dans` ON seances.Matiere = `est_enseignée_dans`.`Id` INNER JOIN 
            matieres ON `est_enseignée_dans`.`Matiere` = matieres.Id_matiere WHERE No_carte_etudiant = '".$_SESSION['No_carte']."' AND `participe_à`.`Id_seance` 
            IN (SELECT Id FROM seances WHERE Matiere IN (SELECT Id FROM est_enseignée_dans WHERE Matiere IN (SELECT Id_matiere FROM matieres WHERE matieres.Semestre = ".$_SESSION['semestre']."))) 
            ORDER BY seances.Numero_seance ASC;
            ";

            $res = mysqli_query($conn, $sql);

            $data = mysqli_fetch_all($res, MYSQLI_ASSOC);

            $_SESSION['cols_names'] = array_unique(array_column($data, 'Nom_Matiere'));
            
            $_SESSION['datas'] = $data;

            header('Location: ../Accueil/index.php?semestre='.$_SESSION['semestre']);
            exit();
        }
    }
    mysqli_close($conn);
}
?>