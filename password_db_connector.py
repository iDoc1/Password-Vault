# Author: Ian Docherty
# Date: 2/1/2022
# Description: This module defines the VaultConnection class, which allows the
#              master user to connect to the database and perform CRUD operations
#              on the database


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

    def create_user(self, username, password):
        """
        Creates a master user with a given name, and a given password
        :param username: name of user
        :param password: master password
        :return:
        """