<?php

if(isset($_POST['login-submit'])){

    require 'dbh.ext.php'; // cette ligne nous permettra d'interagir avec la base de données

    $no_carte = $_POST['no_carte'];

    $sql = "SELECT * FROM etudiant INNER JOIN classes ON etudiant.Classe = classes.Id_Classe WHERE No_carte_etudiant='".$no_carte."';";
    $res = mysqli_query($conn, $sql);
    if(!$res){
        header("Location: ../Connexion/index.php?message=sqlerror");
        exit();
    }else{
        $resultCheck = mysqli_num_rows($res); // le nombre de lignes correspondantes
        if($resultCheck==0){
            header("Location: ../Connexion/index.php?message=usernotfound");
            exit();
        }else{
            session_start(); // demarrage d'une session
            $row = mysqli_fetch_assoc($res);
            $_SESSION['No_carte'] = $row['No_carte_etudiant'];
            $_SESSION['Nom'] = $row['Nom'];
            $_SESSION['Prenoms'] = $row['Prenom'];          
            $_SESSION['Email'] = $row['Email_etudiant'];            
            $_SESSION['Classe'] = $row['Nom_Classe'];
            header("Location: ../extern/matieres.ext.php?semestre=1");
            exit();
        }
    }

    mysqli_close($conn);

}else{
    header('Location:../Connexion/index.php ');
}

?>