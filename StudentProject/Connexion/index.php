<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="container">
        <form action="../extern/login.ext.php" method="POST">
            <img src="logo_dit.png" alt="">
            <label for="no_carte">Entrez votre identifiant</label>
                <input type="text" name="no_carte" id="no_carte_entry">
                <button type="submit" name='login-submit'>Se connecter</button>
                <p id="alert-msg" style="color:red">
                    <?php 
                        if(isset($_GET['message'])){
                            if($_GET['message'] == 'usernotfound'){
                                echo "Utilisateur inexistant";
                                }
                            }
                        ?>
                </p>
        </form>
    </div>
</body>
</html>