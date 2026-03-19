# VG2-Information_Dashboard



Database sql:

-- Lag Databsen
CREATE DATABASE IF NOT EXISTS information_dashboard;
USE information_dashboard;

-- Lag "User" table for databasen, sånn at vi kan logge inn
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Index på email, bare en test for sjekke hvordan index fungerer
CREATE INDEX idx_email ON user(email);
