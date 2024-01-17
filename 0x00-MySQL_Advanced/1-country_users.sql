-- Script that creates a table users following these requirements:
-- id, email, name, country(enumeration of US, CO and TN)
ALTER TABLE users
ADD COLUMN country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL;

