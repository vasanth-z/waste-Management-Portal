<?php
// Start session to store teacher data
session_start();
if (!isset($_SESSION['teachers'])) {
    $_SESSION['teachers'] = [];
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teacher Management</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav class="navbar">
        <div class="logo">
            <img src="logo.png" alt="Logo" width="40">
            <span>தமிழும் கலையும்</span>
        </div>
        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#">Logout</a>
        </div>
    </nav>

    <div class="container">
        <div class="form-container">
            <h2>Add Teacher Details</h2>
            <form action="process.php" method="post">
                <input type="text" name="roll_no" placeholder="Roll No" required>
                <input type="text" name="name" placeholder="Name" required>
                <input type="text" name="qualification" placeholder="Qualification" required>
                <input type="number" name="experience" placeholder="Experience" required>
                <input type="text" name="subject" placeholder="Subject" required>
                <button type="submit">Add</button>
            </form>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Roll No</th>
                        <th>Name</th>
                        <th>Qualification</th>
                        <th>Experience</th>
                        <th>Subject</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    if (!empty($_SESSION['teachers'])) {
                        foreach ($_SESSION['teachers'] as $teacher) {
                            echo "<tr>
                                <td>{$teacher['roll_no']}</td>
                                <td>{$teacher['name']}</td>
                                <td>{$teacher['qualification']}</td>
                                <td>{$teacher['experience']}</td>
                                <td>{$teacher['subject']}</td>
                            </tr>";
                        }
                    }
                    ?>
                </tbody>
            </table>
        </div>
    </div>

    <footer>
        <p>© 2025 Tamiliyum Kalaiyum</p>
    </footer>

</body>
</html>
