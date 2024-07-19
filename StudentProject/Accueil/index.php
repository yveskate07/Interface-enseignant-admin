<?php

session_start();

if(!isset($_SESSION['No_carte'])){ 
    // si un utilisateur n'est pas connecté et essaie d'afficher cette page, on le renvoie à la page de connexion 
    header('Location:../Connexion/index.php?message=retouraconnexion');
    exit();
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="main-container">
        <div id="left-container">
            <div id="img-frame"><img src="student_pic.png" style="width: 50%;" alt="photo_profil"></div>
            <div id="infos_persos">
                <h2 id="name"><?php echo $_SESSION['Nom']?></h2>
                <h2 id="second-name"><?php echo $_SESSION['Prenoms']?></h2>
                <h2 id="classe"><?php echo $_SESSION['Classe']?></h2>
                <h3 id="email-address"><?php echo $_SESSION['Email']?></h3>

                <form action="../extern/logout.ext.php", method="POST">
                    <button type='submit' name='logout-btn' id = 'logoutbtn'>Se deconnecter</button>
                </form>
                
            </div>
        </div>

        <div id="right-container">
            <div id="upper-frame">
                <?php 
                if($_GET['semestre'] == 1){
                echo "<form action='../extern/matieres.ext.php' method='GET'>
                    <select name='selectd-semestre' id='matieres-select'>
                        <option value='1' selected>Semestre 1</option>
                        <option value='2' >Semestre 2</option>
                    </select>
                    <button type='submit' name='display-matieres'>Afficher</button>
                </form>";}else{
                    echo "<form action='../extern/matieres.ext.php' method='GET'>
                    <select name='selectd-semestre' id='matieres-select'>
                        <option value='1'>Semestre 1</option>
                        <option value='2' selected >Semestre 2</option>
                    </select>
                    <button type='submit' name='display-matieres'>Afficher</button>
                </form>";
                }
                ?>
            </div>
            <div id="lower-frame">
                <h1 id="welcome-msg">Bienvenu(e)</h1>
                <?php 
                function get_matiere($arr, $chr){
                    for($a=0; $a<count($arr); $a++){
                        if($arr[$a]['Nom_Matiere'] == $chr){
                            return $arr[$a];
                        }
                    }
                }
                $count = 1;

                $temp = array();
                $first=1;
                echo '<table>'.'';
                echo '<tr><th></th>';
                for($i=0; $i<count($_SESSION['cols_names']); $i++){
                    echo '<th>'.$_SESSION['cols_names'][$i].'</th>';
                }
                echo '</tr>'; // à ce niveau tous les en tetes de la table ont ete places

                foreach($_SESSION['datas'] as $row){
                    if($row['Numero_seance']==$count){
                        array_push($temp, $row);
                        if(count($temp) == count($_SESSION['cols_names'])){
                            echo '<tr><td>Séance '.$count.'</td>';
                            for($j=0; $j<count($temp); $j++){
                                $matiere = get_matiere($temp, $_SESSION['cols_names'][$j]);
                                if($matiere['Present']==1){
                                    echo '<td>Présent</td>';
                                }else{
                                    if($matiere['Present']== null && $matiere['Effectuee'] == 0){
                                        echo '<td></td>';
                                    }else{
                                        if($matiere['Present']== null && $matiere['Effectuee'] == 1){
                                        echo '<td>Absent</td>';
                                        }
                                    }
                                }
                            }
                            echo '<tr>';
                            $count++;
                            $temp = array();
                            }
                        }
                    }
                echo '</table>';
                ?>
            </div>
        </div>
    </div>
</body>
</html>