# Author: Ian Docherty
# Date: 2/1/2022
# Description: This module defines the VaultConnection class, which allows the
#              master user to connect to the database and perform CRUD operations
#              on the database

import mysql.connector
from mysql.connector import errorcode
from mysql.connector import connection

class VaultConnection:
    """
    Allows the user to connect to and perform CRUD operations on
    the database
    """

    def __init__(self):
        """
        Creates a VaultConnection object with a master username,
        a given password, and an initially-NULL connection
        """
        self.master_username = "masterUser"
        self.master_password = None
        self.db_connection = None

    def connect_to_db(self, password):
        """
        Connects to the database and sets the class member to
        point to that connection. Returns True if successful, and
        False otherwise
        :return: True on success, False otherwise
        """

        # Connect to database with given password
        try:
            cnx = mysql.connector.connect(user=self.master_username,
                                          password=password,
                                          database='passwordvault')
        except mysql.connector.Error:
            return False  # Incorrect password
        else:

            # Set data member to successful connection
            self.db_connection = cnx
            return True

    def close_connection(self):
        """
        Closes the database connection
        """

    def test_db_connection(self, password):
        """
        Tests then closes a connection to the database with the given
        password. Returns True if test was successful. A return value
        of False indicates the given password is incorrect.
        :param password: password to connect to database
        :return: True on success, False otherwise
        """
        try:
            cnx = mysql.connector.connect(user=self.master_username,
                                          password=password,
                                          database='passwordvault')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return False  # Given password doesn't work
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            return True  # Given password works

    def test_default_password(self):
        """
        Returns True if the database user account still has the
        default password set. Returns False if not.
        :return: True if database user has default password
        """
        return self.test_db_connection("default")

    def create_user(self, username, password):
        """
        Creates a master user with a given name, and a given password
        :param username: name of user
        :param password: master password
        :return:
        """

        # Connect to database with default password
        try:
            cnx = mysql.connector.connect(user=self.master_username,
                                          password='default',
                                          database='passwordvault')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:

            # Insert name of user into master account table
            cursor = cnx.cursor()
            set_user_query = f"INSERT INTO PasswordVault.MasterAccount (masterUser) VALUE ('{username}');"
            cursor.execute(set_user_query)

            # Reset user password to the given password
            set_pwd_query = f"SET PASSWORD = '{password}';"
            cursor.execute(set_pwd_query)

            # Close connection
            cursor.close()
            cnx.close()

    def get_master_username(self):
        """
        Returns the name of the master account username
        :return: Master account username
        """
        cursor = self.db_connection.cursor()
        username_query = "SELECT masterUser FROM PasswordVault.MasterAccount;"
        cursor.execute(username_query)

        return cursor.fetchone()[0]


if __name__ == "__main__":
    pw = VaultConnection()
    print(pw.get_master_username())
