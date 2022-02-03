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
        Connects to the database. Returns True if successful, and
        False otherwise
        :return: True on success, False otherwise
        """

    def close_connection(self):
        """
        Closes the database connection
        """

    def test_db_connection(self, password):
        """
        Tests then closes a connection to the database with the given
        password. Returns True if test was successful. A return value
        of False indicates the given password is incorrect. Used to
        check if user has created an account with a new password.
        :param password: password to connect to database
        :return: True on success, False otherwise
        """

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
                                          password='defaultpassword',
                                          database='passwordvault')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or passowrd")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:

            # Reset user password to the given password

            # Insert name of user into master account table

            # Close connection
            cnx.close()


if __name__ == "__main__":
    pw = VaultConnection()
