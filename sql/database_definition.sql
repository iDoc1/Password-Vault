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
    masterPassword VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);