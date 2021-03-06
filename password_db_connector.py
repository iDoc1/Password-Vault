# Author: Ian Docherty
# Description: This module defines the VaultConnection class, which allows the
#              master user to connect to the database and perform CRUD operations
#              on the database

import mysql.connector
from mysql.connector import errorcode


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
        self.db_connection.close()

    def test_default_password(self):
        """
        Returns True if the database user account still has the
        default password set. Returns False if not.
        :return: True if database user has default password
        """
        return self.test_db_connection("default")

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

    def create_user(self, username, password):
        """
        Creates a master user with a given name, and a given password
        :param username: name of user
        :param password: master password
        :return: True if account creation successful, False otherwise
        """

        cnx = self._try_connect_with_default()
        if cnx:

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
            return True

    def _try_connect_with_default(self):
        """
        Attempts to connect to the database using the default password.
        :return: Connection if successful, None otherwise
        """
        try:
            cnx = mysql.connector.connect(user=self.master_username,
                                          password='default',
                                          database='passwordvault')
            return cnx

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            return None

    def edit_master_username(self, new_username):
        """
        Inserts a new username into master account table
        :return: True if successful, False otherwise
        """
        try:
            cursor = self.db_connection.cursor()
            edit_username_query = "UPDATE PasswordVault.MasterAccount " \
                                  "SET masterUser = %s WHERE id >= 1;"

            cursor.execute(edit_username_query, (new_username, ))

            # Commit changes
            self.db_connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True

    def edit_master_password(self, new_password):
        """
        Updates master account with new password
        :return: True if successful, False otherwise
        """
        try:
            cursor = self.db_connection.cursor()
            edit_password_query = f"SET PASSWORD = '{new_password}';"
            cursor.execute(edit_password_query)

            cursor.close()
        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True

    def get_master_username(self):
        """
        Returns the name of the master account username
        :return: Master account username or None if not exists
        """
        cursor = self.db_connection.cursor()
        username_query = "SELECT masterUser FROM PasswordVault.MasterAccount;"
        cursor.execute(username_query)

        master_username = cursor.fetchone()
        if master_username is None:
            return None
        else:
            return master_username[0]

    def fetch_all_passwords(self):
        """
        Executes a query to get all passwords from the database and
        returns the result set. The dictionaries contain the following
        keys: 'row_id', 'account', 'password'.
        :return: An array of dictionaries of the results
        """
        cursor = self.db_connection.cursor()
        fetch_all_query = "SELECT * FROM PasswordVault.Passwords ORDER BY accountName;"
        cursor.execute(fetch_all_query)

        # Store all results in an array of dictionaries
        result_set = []
        for (row_id, account, password) in cursor:
            row_dict = {"row_id": row_id, "account": account, "password": password}
            result_set.append(row_dict)

        cursor.close()
        return result_set

    def add_new_password(self, account, password):
        """
        Adds a new password with the given account name and password
        to the database
        :param account: account name to add
        :param password: password to add
        :return: True if add successful, False otherwise
        """
        try:
            cursor = self.db_connection.cursor()
            insert_query = "INSERT INTO PasswordVault.Passwords (accountName, accountPassword) " \
                           "VALUES (%s, %s);"
            cursor.execute(insert_query, (account, password))

            # Commit changes
            self.db_connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True

    def delete_password(self, password_id):
        """
        Deletes the password in the database with the given id
        :param password_id: The row id of the password
        :return: True if deletion successful, False otherwise
        """
        try:
            cursor = self.db_connection.cursor()
            delete_query = "DELETE FROM PasswordVault.Passwords WHERE id = %s;"
            cursor.execute(delete_query, (password_id, ))

            # Commit changes
            self.db_connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True

    def edit_password(self, password_id, account, password):
        """
        Updates the password with the given password ID with the given
        account name and password
        :param password_id: ID of password to change
        :param account: new account name
        :param password: new password
        :return: True if edit successful, False otherwise
        """
        try:
            cursor = self.db_connection.cursor()
            delete_query = "UPDATE PasswordVault.Passwords SET accountName = %s, " \
                           "accountPassword = %s WHERE id = %s;"
            cursor.execute(delete_query, (account, password, password_id))

            # Commit changes
            self.db_connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            return True
