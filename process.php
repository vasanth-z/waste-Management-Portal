<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $teacher = [
        'roll_no' => $_POST['roll_no'],
        'name' => $_POST['name'],
        'qualification' => $_POST['qualification'],
        'experience' => $_POST['experience'],
        'subject' => $_POST['subject']
    ];

    $_SESSION['teachers'][] = $teacher;
}

header("Location: index.php");
exit();
