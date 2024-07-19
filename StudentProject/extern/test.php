<?php

session_start();

foreach($_SESSION['datas'] as $row){
    print_r($row);
    echo '<br><br>';
}
echo '<br><br>';


foreach($_SESSION['cols_names'] as $row1){
    print_r($row1);
    echo '<br><br>';
}


?>