<?php
// Enable error reporting for debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Database configuration
$servername = "localhost";
$username = "your_username";
$password = "your_password";
$dbname = "tiktok_clone";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get data from POST request
$username = $_POST['username'];
$country_code = $_POST['country-code'];
$phone = $_POST['phone'];
$password = $_POST['password'];

// Validate input
if (empty($username) || empty($password)) {
    http_response_code(400);
    echo "Username and password are required";
    exit;
}

// Hash the password
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

// Create users table if it doesn't exist
$sql = "CREATE TABLE IF NOT EXISTS users (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)";

if ($conn->query($sql) !== TRUE) {
    echo "Error creating table: " . $conn->error;
}

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO users (username, country_code, phone, password) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ssss", $username, $country_code, $phone, $hashed_password);

// Execute the statement
if ($stmt->execute()) {
    echo "New account created successfully";
} else {
    echo "Error: " . $stmt->error;
}

// Close connections
$stmt->close();
$conn->close();
?>
