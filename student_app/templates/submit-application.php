<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $firstName = htmlspecialchars($_POST['firstName']);
    $lastName = htmlspecialchars($_POST['lastName']);
    $dob = htmlspecialchars($_POST['dob']);
    $gender = htmlspecialchars($_POST['gender']);
    $address = htmlspecialchars($_POST['address']);
    $parentName = htmlspecialchars($_POST['parentName']);
    $relationship = htmlspecialchars($_POST['relationship']);
    $parentContact = htmlspecialchars($_POST['parentContact']);
    $parentEmail = htmlspecialchars($_POST['parentEmail']);
    $previousSchool = htmlspecialchars($_POST['previousSchool']);
    $examYear = htmlspecialchars($_POST['examYear']);
    $examNumber = htmlspecialchars($_POST['examNumber']);
    $course = htmlspecialchars($_POST['course']);
    $additionalInfo = htmlspecialchars($_POST['additionalInfo']);

    // File upload handling
    $resultSlip = $_FILES['resultSlip'];
    $uploadDir = 'UNEB Admission/';
    $uploadFile = $uploadDir . basename($resultSlip['name']);
    move_uploaded_file($resultSlip['tmp_name'], $uploadFile);

    // Prepare the email
    $to = 'musanjerobert222@gmail.com';
    $subject = 'New Student Application';
    $message = "
        First Name: $firstName\n
        Last Name: $lastName\n
        Date of Birth: $dob\n
        Gender: $gender\n
        Address: $address\n
        Parent/Guardian Name: $parentName\n
        Relationship: $relationship\n
        Parent/Guardian Contact: $parentContact\n
        Parent/Guardian Email: $parentEmail\n
        Previous School: $previousSchool\n
        Year of UNEB Exam: $examYear\n
        UNEB Index Number: $examNumber\n
        Level Applied For: $course\n
        Additional Information: $additionalInfo\n
        Result Slip: $uploadFile
    ";
    $headers = "From: no-reply@hanainternational.ac.ug";

    // Send the email
    if (mail($to, $subject, $message, $headers)) {
        echo "Application submitted successfully!";
    } else {
        echo "Failed to submit the application.";
    }
}
?>
