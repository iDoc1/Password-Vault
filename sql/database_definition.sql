/* Database and table definition queries used to build the
 * PasswordVault database and master user account
 */

CREATE SCHEMA IF NOT EXISTS PasswordVault;

DROP TABLE IF EXISTS PasswordVault.Passwords, PasswordVault.MasterAccount;

/* Stores all of the user's accounts and passwords */
CREATE TABLE PasswordVault.Passwords (
	id INT AUTO_INCREMENT NOT NULL,
    accountName VARCHAR(255) NOT NULL,
    accountPassword VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

/* Stores the master account username and password */
CREATE TABLE PasswordVault.MasterAccount (
	id INT AUTO_INCREMENT NOT NULL,
    masterUser VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

/* Create a new user account with default password "password" */
DROP USER IF EXISTS 'masterUser'@'localhost';
CREATE USER IF NOT EXISTS 'masterUser'@'localhost' IDENTIFIED BY 'default';

/* Grant privileges to user to create, read, update, and delete records */
GRANT SELECT, INSERT, UPDATE, DELETE ON PasswordVault.* to 'masterUser'@'localhost';
