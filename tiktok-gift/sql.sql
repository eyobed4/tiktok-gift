CREATE DATABASE tiktok_clone;
CREATE USER 'tiktok_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON tiktok_clone.* TO 'tiktok_user'@'localhost';
FLUSH PRIVILEGES;
