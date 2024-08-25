<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST["name"];
  $email = $_POST["email"];
  $message = $_POST["message"];
  $to = "musanje222@gmail.com";
  $subject = "Contact Form Submission";
  $body = "Name: $name\nEmail: $email\nMessage: $message";
  mail($to, $subject, $body);
  echo "Message sent successfully!";
}
?>