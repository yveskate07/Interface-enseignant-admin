<?php

session_start();
if(!isset($_POST['logout-btn'])){
    header('Location: ../Accueil/index.php?semestre=1');
    exit();
}else{
    session_unset();
    session_destroy();
    header('Location: ../Connexion/index.php');
    exit();
}

?>