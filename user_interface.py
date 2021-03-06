# Author: Ian Docherty
# Description: This module defines all of the classes and methods for the
#              password vault graphical user interface.

import password_entropy
import threading
import time
import pyperclip
import rpyc
from password_db_connector import VaultConnection
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QPushButton, \
    QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QCheckBox, QSpinBox, QMessageBox, QProgressBar, QMenu, QAction

# Constants for allowed characters
LOWERS = "abcdefghijklmnopqrstuvwxyz"
UPPERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '1234567890'
SPECIALS = '@%+!$?~'


class MainWindow(QMainWindow):
    """
    This class defines the main window for the GUI where all
    widgets for this application reside. Screen switching is
    handled by this class.
    """

    def __init__(self):
        """
        Create a MainWindow object and start at the login screen
        """
        super().__init__()

        # Create VaultConnection object
        self.vault_cnx = VaultConnection()

        # Create a menu bar object
        self.account_menu = QMenu("Account Settings")

        # Create stacked widget and set central widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create a LoginScreen object and define button slots
        self.login_screen_widget = LoginScreen()
        self.login_screen_widget.login_button.clicked.connect(self.attempt_to_login)
        self.login_screen_widget.password_input.returnPressed.connect(self.attempt_to_login)
        self.login_screen_widget.create_account_button.clicked.connect(self.go_to_create_account_screen)

        # If default password already changed, disable create account button
        if not self.vault_cnx.test_default_password():
            self.login_screen_widget.create_account_button.setEnabled(False)

        # Create a CreateAccountScreen object and define button slots
        self.create_account_screen_widget = CreateAccountScreen()
        self.create_account_screen_widget.create_account_button.clicked.connect(self.attempt_to_create_account)

        # Define screens that will not be initialized until user successfully logs in
        self.main_screen_widget = None
        self.add_password_screen_widget = None
        self.edit_password_screen_widget = None
        self.edit_master_account_screen_widget = None

        # Add all screen widgets to stacked widget indexes
        self.central_widget.addWidget(self.login_screen_widget)  # Index 0
        self.central_widget.addWidget(self.create_account_screen_widget)  # Index 1

        self.go_to_login_screen()

        # Set window geometry and show window
        self.setGeometry(600, 500, 400, 250)
        self.setWindowTitle('PasswordVault')
        self.setWindowIcon(QIcon("./icons/key_icon.png"))
        self.statusBar().showMessage("Ready")
        self.show()

    def go_to_login_screen(self):
        """
        Clears any password input and shows login screen
        """
        self.menuBar().clear()
        self.reset_login_screen()

        # Clear edit master account fields if necessary
        if self.edit_master_account_screen_widget is not None:
            self.edit_master_account_screen_widget.clear_input_fields()

        self.central_widget.setCurrentIndex(0)

    def attempt_to_login(self):
        """
        Attempts to login to master account. Displays message if attempt fails.
        """

        # Check if user has an account. If not, display message.
        if self.vault_cnx.test_default_password():
            self.show_create_account_message()
        else:

            # If password is correct, create remaining screens and go to main screen
            if self.vault_cnx.connect_to_db(self.login_screen_widget.password_input.text()):

                self.add_account_settings_to_menu_bar()

                if self.screens_already_exist():
                    self.central_widget.setCurrentIndex(2)
                    return

                self.create_remaining_screen_widgets()
                self.display_master_username()

                # Go to main screen and enlarge window
                self.central_widget.setCurrentIndex(2)
                self.setGeometry(600, 500, 550, 400)
            else:
                self.show_failed_login_message()

    def show_create_account_message(self):
        """
        Displays message to user if their login attempt fails
        """
        self.login_screen_widget.password_incorrect_label.setText("You must create a user account to begin.")
        self.login_screen_widget.password_incorrect_label.setStyleSheet("background-color: yellow;")
        self.login_screen_widget.login_button.setEnabled(False)  # Disable login button
        self.login_screen_widget.create_account_button.setEnabled(True)  # Enable create account button

    def create_remaining_screen_widgets(self):
        """
        Initializes objects for the main, add password, edit password, and edit
        master account screens
        """
        self.create_main_screen_widget()
        self.create_add_password_screen_widget()
        self.create_edit_password_screen_widget()
        self.edit_master_account_screen_widget = EditMasterAccountScreen(self)
        self.add_remaining_widgets_to_stack()

    def screens_already_exist(self):
        """
        Returns True if the main, add password, edit password, and edit master
        account screens
        """
        main_exists = self.main_screen_widget is not None
        add_exists = self.add_password_screen_widget is not None
        edit_exists = self.edit_password_screen_widget is not None
        edit_master_exists = self.edit_master_account_screen_widget is not None
        return main_exists and add_exists and edit_exists and edit_master_exists

    def add_remaining_widgets_to_stack(self):
        """
        Adds the main, add password, edit password, and edit master account screen
        widgets to the central stacked widget
        """
        self.central_widget.addWidget(self.main_screen_widget)  # Index 2
        self.central_widget.addWidget(self.add_password_screen_widget)  # Index 3
        self.central_widget.addWidget(self.edit_password_screen_widget)  # Index 4
        self.central_widget.addWidget(self.edit_master_account_screen_widget)  # Index 5

    def create_main_screen_widget(self):
        """
        Creates object for main screen and defines add password button slot
        """
        self.main_screen_widget = MainScreen(self)  # Set MainWindow as parent widget
        self.main_screen_widget.add_password_button.clicked.connect(self.go_to_add_password_screen)

    def create_add_password_screen_widget(self):
        """
        Creates object for add password screen and defines button slots
        """
        self.add_password_screen_widget = AddPasswordScreen(self)
        self.add_password_screen_widget.add_button.clicked.connect(self.attempt_to_add_password)
        self.add_password_screen_widget.cancel_button.clicked.connect(self.go_to_main_screen_from_add)

    def create_edit_password_screen_widget(self):
        """
        Creates object for edit password screen and defines button slots
        """
        self.edit_password_screen_widget = EditPasswordScreen(self)
        self.edit_password_screen_widget.edit_button.clicked.connect(self.attempt_to_edit_password)
        self.edit_password_screen_widget.cancel_button.clicked.connect(self.go_to_main_screen_from_edit)

    def display_master_username(self):
        """
        Displays master username stored in database
        """
        master_user = self.vault_cnx.get_master_username()
        self.main_screen_widget.welcome_label.setText("Welcome, " + master_user)

    def add_account_settings_to_menu_bar(self):
        """
        Adds dropdown menus called 'Account Settings' and 'Log out' to the menu bar
        """
        self.menuBar().clear()
        self.account_menu.clear()
        self.menuBar().addMenu(self.account_menu)
        self.menuBar().setStyleSheet("background-color: lightGray")

        account_action = QAction("Edit Master Account", self)
        account_action.triggered.connect(self.go_to_edit_master_account_screen)
        self.account_menu.addAction(account_action)

        logout_action = QAction("Sign Out", self)
        logout_action.triggered.connect(self.go_to_login_screen)
        self.account_menu.addAction(logout_action)

    def show_failed_login_message(self):
        """
        Shows message when incorrect password is entered
        """
        self.login_screen_widget.password_incorrect_label.setText("Incorrect password")
        self.login_screen_widget.password_incorrect_label.setStyleSheet("background-color: yellow;")

    def go_to_edit_master_account_screen(self):
        """
        Creates an EditMasterAccountScreen widget then routes user to that
        screen
        """

        # Display current username in the username input prior to routing
        master_username = self.vault_cnx.get_master_username()
        self.edit_master_account_screen_widget.name_input.setText(master_username)
        self.central_widget.setCurrentIndex(5)

    def go_to_create_account_screen(self):
        """
        Shows the create account screen
        """
        self.central_widget.setCurrentIndex(1)

    def attempt_to_create_account(self):
        """
        Attempts to create a master account then route the user back to the login screen
        """
        username = self.create_account_screen_widget.name_input.text()
        password_input = self.create_account_screen_widget.password_input.text()
        reenter_input = self.create_account_screen_widget.reenter_input.text()

        # Check if passwords are the same
        if password_input != reenter_input:
            self.create_account_screen_widget.password_match_label.setText("Passwords must match")
            self.create_account_screen_widget.password_match_label.setStyleSheet("background-color: yellow;")
        else:
            self.vault_cnx.create_user(username, password_input)
            self.clear_create_account_screen()
            self.reset_login_screen()
            self.go_to_login_screen()

    def clear_create_account_screen(self):
        """
        Clears all inputs on the create account screen
        """
        self.create_account_screen_widget.name_input.setText("")
        self.create_account_screen_widget.password_input.setText("")
        self.create_account_screen_widget.reenter_input.setText("")

    def reset_login_screen(self):
        """
        Clears all login screen inputs then disables the create account button
        so user only has the choice to log in
        """
        self.login_screen_widget.password_input.setText("")
        self.login_screen_widget.login_button.setEnabled(True)  # Re-enable login button
        self.login_screen_widget.create_account_button.setEnabled(False)  # Disable create account button
        self.login_screen_widget.password_incorrect_label.setStyleSheet("")  # Reset label color
        self.login_screen_widget.password_incorrect_label.setText("")

    def go_to_add_password_screen(self):
        """
        Takes user to a new screen to add a new password to the database
        """
        self.central_widget.setCurrentIndex(3)

    def attempt_to_add_password(self):
        """
        Creates a new account and password in the database then routes
        back to main screen if there are no issues with use inputs
        """

        # Only add password if there are no input errors
        if not self.password_input_errors_exist(self.add_password_screen_widget):

            # Add password and account to the database
            new_account = self.add_password_screen_widget.account_input.text()
            password_input = self.add_password_screen_widget.password_input.text()
            add_password_status = self.vault_cnx.add_new_password(new_account, password_input)

            # Check if there was a database error
            if not add_password_status:
                self.statusBar().showMessage("Database error while adding password.")
            else:
                self.go_to_main_screen_from_add()

    def attempt_to_edit_password(self):
        """
        Attempts to modify the existing password with the inputs that the user
        entered then updates the database
        """

        # Only edit password if no password input errors exist
        if not self.password_input_errors_exist(self.edit_password_screen_widget):
            password_id = self.edit_password_screen_widget.password_id
            new_account = self.edit_password_screen_widget.account_input.text()
            password_input = self.edit_password_screen_widget.password_input.text()

            # Add password to the database
            edit_password_status = self.vault_cnx.edit_password(password_id, new_account, password_input)

            # Check if there was a database error
            if not edit_password_status:
                self.statusBar().showMessage("Database error while adding password.")
            else:
                self.go_to_main_screen_from_edit()

    def password_input_errors_exist(self, add_or_edit_widget):
        """
        Checks for errors in the password entry fields for the add and edit screen widgets
        :param add_or_edit_widget: the add or edit password screen widget
        :return: True if there are no errors, False otherwise
        """
        new_account = add_or_edit_widget.account_input.text()
        password_input = add_or_edit_widget.password_input.text()
        reenter_input = add_or_edit_widget.reenter_input.text()

        # Check if passwords are the same
        if password_input != reenter_input:
            return self.show_password_mismatch_message(add_or_edit_widget)

        # Check if account name was entered
        elif len(new_account) == 0:
            return self.show_missing_account_message(add_or_edit_widget)

        # Check if password input is empty
        elif len(password_input) == 0:
            return self.show_missing_password_message(add_or_edit_widget)

        elif self.contains_unapproved_specials(password_input):
            return self.show_illegal_special_chars_message(add_or_edit_widget)
        else:
            return False

    def show_password_mismatch_message(self, add_or_edit_widget):
        """
        Displays message when password don't match and returns True to
        indicate password don't match
        """
        add_or_edit_widget.password_match_label.setText("Passwords must match")
        add_or_edit_widget.password_match_label.setStyleSheet("background-color: yellow;")
        return True

    def show_missing_account_message(self, add_or_edit_widget):
        """
        Displays message when account name is missing and returns True to
        indicate this
        """
        add_or_edit_widget.password_match_label.setText("Account name is required")
        add_or_edit_widget.password_match_label.setStyleSheet("background-color: yellow;")
        return True

    def show_missing_password_message(self, add_or_edit_widget):
        """
        Displays message when password input is missing and returns True to
        indicate this
        """
        add_or_edit_widget.password_match_label.setText("Password is required")
        add_or_edit_widget.password_match_label.setStyleSheet("background-color: yellow;")
        return True

    def show_illegal_special_chars_message(self, add_or_edit_widget):
        """
        Displays message when password input contains illegal special characters
        and returns True to indicate this
        """
        add_or_edit_widget.password_match_label.setText("Password can only have the "
                                                        "following special characters: " + SPECIALS)
        add_or_edit_widget.password_match_label.setStyleSheet("background-color: yellow;")
        return True

    def contains_unapproved_specials(self, password):
        """
        Returns True if the given password contains special characters not in
        the approved special characters constant SPECIALS
        """
        for char in password:
            if char not in LOWERS and char not in UPPERS and char not in NUMBERS:
                if char not in SPECIALS:
                    return True

        return False

    def go_to_main_screen_from_add(self):
        """
        Takes user back to main screen after clearing all add screen input fields
        """
        self.main_screen_widget.load_password_data()
        self.clear_add_password_fields()
        self.central_widget.setCurrentIndex(2)  # Back to main screen

    def go_to_main_screen_from_edit(self):
        """
        Takes user back to main screen after clearing all edit screen input fields
        """
        self.main_screen_widget.load_password_data()
        self.clear_edit_password_fields()
        self.central_widget.setCurrentIndex(2)

    def clear_add_password_fields(self):
        """
        Clears all input fields for the add password screen
        """
        self.clear_password_input_fields(self.add_password_screen_widget)

    def clear_edit_password_fields(self):
        """
        Clears all input fields for the edit password screen
        """
        self.edit_password_screen_widget.password_id = None
        self.clear_password_input_fields(self.edit_password_screen_widget)

    def clear_password_input_fields(self, add_or_edit_widget):
        """
        Clears password input fields for the given add or edit screen widget
        :param add_or_edit_widget: the add or edit password screen widget
        """
        add_or_edit_widget.account_input.clear()
        add_or_edit_widget.password_input.clear()
        add_or_edit_widget.reenter_input.clear()
        add_or_edit_widget.generate_widget.special_chars_check.setChecked(False)
        add_or_edit_widget.generate_widget.numbers_check.setChecked(False)
        add_or_edit_widget.generate_widget.case_check.setCheckState(False)
        add_or_edit_widget.generate_widget.char_length_box.setValue(12)  # Spinbox set to min value
        add_or_edit_widget.password_match_label.setText("")
        add_or_edit_widget.password_match_label.setStyleSheet("")
        self.statusBar().showMessage("Ready")


class LoginScreen(QWidget):
    """
    This class defines the login screen for the GUI
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a login key icon
        login_icon_layout = QHBoxLayout()
        self.login_label = QLabel(self)
        self.login_pixmap = QPixmap("./icons/login_icon.png")
        self.login_label.setPixmap(self.login_pixmap.scaledToWidth(80))  # Resize image
        self.login_label.resize(self.login_pixmap.width(), self.login_pixmap.height())  # Resize label

        # Center the login key icon
        login_icon_layout.addStretch(-1)
        login_icon_layout.addWidget(self.login_label)
        login_icon_layout.addStretch(-1)
        self.login_icon_widget = QWidget(self)
        self.login_icon_widget.setLayout(login_icon_layout)

        # Create welcome label widget
        welcome_label_layout = QHBoxLayout()
        self.welcome_label = QLabel("   Welcome to your password vault!\nPlease enter your password to log in.")
        self.welcome_label.setFont(QFont("Arial", 12))

        # Center the welcome label
        welcome_label_layout.addStretch(-1)
        welcome_label_layout.addWidget(self.welcome_label)
        welcome_label_layout.addStretch(-1)
        self.welcome_widget = QWidget(self)
        self.welcome_widget.setLayout(welcome_label_layout)

        # Create password input and password label widgets
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask password input when typing password
        self.password_input.setPlaceholderText("Enter password")
        self.password_label = QLabel("Password: ")

        # Create horizontal password layout
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        self.password_widget = QWidget(self)
        self.password_widget.setLayout(password_layout)

        # Create label to tell user if password was incorrect
        self.password_incorrect_label = QLabel("")

        # Create login button layout
        self.login_button = QPushButton("Login")

        # Create a label to explain how to create an account
        self.create_account_label = QLabel("\nNew user? Click below to create a master account and password.")
        self.create_account_label.setFont(QFont("Arial", 10))

        # Create a "Create Account" button
        self.create_account_button = QPushButton("Create Account")

        # Add all widgets to this widget's layout
        layout.addWidget(self.login_icon_widget)
        layout.addWidget(self.welcome_widget)
        layout.addWidget(self.password_widget)
        layout.addWidget(self.login_button)
        layout.addWidget(self.password_incorrect_label)
        layout.addWidget(self.create_account_label)
        layout.addWidget(self.create_account_button)
        self.setLayout(layout)


class CreateAccountScreen(QWidget):
    """
    This class defines the account creation screen for the GUI
    which allows a first-time user to create a password
    """

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Create person account label
        account_icon_layout = QHBoxLayout()
        self.account_label = QLabel(self)
        self.account_pixmap = QPixmap("./icons/create_account_icon.png")
        self.account_label.setPixmap(self.account_pixmap.scaledToWidth(80))  # Resize image
        self.account_label.resize(self.account_pixmap.width(), self.account_pixmap.height())  # Resize label

        # Center account icon label
        account_icon_layout.addStretch(-1)
        account_icon_layout.addWidget(self.account_label)
        account_icon_layout.addStretch(-1)
        self.account_icon_widget = QWidget(self)
        self.account_icon_widget.setLayout(account_icon_layout)

        # Create instruction label
        instruct_label_layout = QHBoxLayout()
        self.instruct_label = QLabel("Enter below information to create a master account.")
        self.instruct_label.setFont(QFont("Arial", 12))

        # Center instruction label
        instruct_label_layout.addStretch(-1)
        instruct_label_layout.addWidget(self.instruct_label)
        instruct_label_layout.addStretch(-1)
        self.instruct_label_widget = QWidget(self)
        self.instruct_label_widget.setLayout(instruct_label_layout)

        # Create name input and name label widgets
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter username here")
        self.name_label = QLabel("Username: ")

        # Create horizontal name input layout
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        self.name_widget = QWidget(self)
        self.name_widget.setLayout(name_layout)

        # Create password input and password label widgets
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password here")
        self.password_label = QLabel("Password: ")

        # Create horizontal password layout
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        self.password_widget = QWidget(self)
        self.password_widget.setLayout(password_layout)

        # Create reenter password input and reenter password label widgets
        self.reenter_input = QLineEdit()
        self.reenter_input.setPlaceholderText("Re-enter password here")
        self.reenter_label = QLabel("Re-enter\nPassword: ")

        # Create horizontal reenter password layout
        reenter_layout = QHBoxLayout()
        reenter_layout.addWidget(self.reenter_label)
        reenter_layout.addWidget(self.reenter_input)
        self.reenter_widget = QWidget(self)
        self.reenter_widget.setLayout(reenter_layout)

        # Create a label to tell user if passwords match or not
        self.password_match_label = QLabel("")

        # Create a button to create account and login
        self.create_account_button = QPushButton("Create Account")

        # Add all widgets to this layout
        self.layout.addWidget(self.account_icon_widget)
        self.layout.addWidget(self.instruct_label_widget)
        self.layout.addWidget(self.name_widget)
        self.layout.addWidget(self.password_widget)
        self.layout.addWidget(self.reenter_widget)
        self.layout.addWidget(self.password_match_label)
        self.layout.addWidget(self.create_account_button)
        self.setLayout(self.layout)


class EditMasterAccountScreen(CreateAccountScreen):
    """
    This class is a modified version of the CreateAccountScreen that
    allows the user to edit the master account
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.vault_cnx = self.parent.vault_cnx  # Database connection

        # Modify text instructions
        self.instruct_label.setText("Edit below information edit master account name and password")
        self.password_label.setText("New\nPassword: ")
        self.password_input.setPlaceholderText("Enter new password here")
        self.reenter_input.setPlaceholderText("Re-enter new password here")
        self.create_account_button.setText("Edit Master Account")

        # Add cancel button
        self.layout.removeWidget(self.create_account_button)  # Remove so layout can be changed
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.go_back_to_main_screen)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_account_button)
        button_layout.addWidget(self.cancel_button)

        # Designate new slot for create account button
        self.create_account_button.clicked.connect(self.update_master_user)

        self.buttons_widget = QWidget(self)
        self.buttons_widget.setLayout(button_layout)
        self.layout.addWidget(self.buttons_widget)

    def update_master_user(self):
        """
        Updates master user with new username and password
        """

        # Check if passwords are the same
        if self.password_input.text() != self.reenter_input.text():
            self.password_match_label.setText("Passwords must match")
            self.password_match_label.setStyleSheet("background-color: yellow;")
        else:
            new_username = self.name_input.text()
            new_password = self.password_input.text()

            self.vault_cnx.edit_master_username(new_username)
            self.vault_cnx.edit_master_password(new_password)

            self.parent.display_master_username()
            self.go_back_to_main_screen()

    def go_back_to_main_screen(self):
        """
        Routes user back to main screen
        """
        self.clear_input_fields()
        self.parent.central_widget.setCurrentIndex(2)

    def clear_input_fields(self):
        """
        Clears username and password text inputs and stylesheet
        """
        self.name_input.setText("")
        self.password_input.setText("")
        self.reenter_input.setText("")
        self.password_match_label.setText("")
        self.password_match_label.setStyleSheet("")


class MainScreen(QWidget):
    """
    This class defines the main screen for the GUI where the
    user can view all accounts and passwords and take action
    as necessary
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()

        # Create welcome label
        welcome_label_layout = QHBoxLayout()
        self.welcome_label = QLabel("")
        self.welcome_label.setFont(QFont("Arial", 12))

        # Center the welcome label
        welcome_label_layout.addStretch(-1)
        welcome_label_layout.addWidget(self.welcome_label)
        welcome_label_layout.addStretch(-1)
        self.welcome_label_widget = QWidget(self)
        self.welcome_label_widget.setLayout(welcome_label_layout)

        # Create table widget to view accounts and passwords
        self.password_table = QTableWidget(self)
        self.password_table.verticalHeader().setVisible(False)
        self.password_table.horizontalHeader().setVisible(False)

        # Refresh/add data to table
        self.load_password_data()

        # Create button to add a password
        self.add_password_button = QPushButton("Add a new password")

        # Add all widgets to layout
        layout.addWidget(self.welcome_label_widget)
        layout.addWidget(self.password_table)
        layout.addWidget(self.add_password_button)

        self.setLayout(layout)

    def load_password_data(self):
        """
        Loads all password data from the database into the table
        """

        # Get table data and build table
        password_data = self.parent.vault_cnx.fetch_all_passwords()
        self.build_empty_table(password_data)

        # Populate table data
        table_row = 0
        while table_row < len(password_data):
            curr_id = password_data[table_row]["row_id"]
            curr_account = password_data[table_row]["account"]
            curr_password = password_data[table_row]["password"]

            self.password_table.setItem(table_row + 1, 0, QTableWidgetItem(curr_account))

            # Replace password text with asterisks
            password_len = len(curr_password)
            password_hidden = ""
            for index in range(password_len):
                password_hidden += "*"

            self.password_table.setItem(table_row + 1, 1, QTableWidgetItem(password_hidden))

            # Add copy button
            self.copy_button = QPushButton("Copy")
            self.password_table.setCellWidget(table_row + 1, 2, self.copy_button)
            self.copy_button.setToolTip("Copy for 15 seconds")
            self.copy_button.clicked.connect(lambda state, password=curr_password:
                                             self.copy_button_click(password))

            # Add edit button with signal connected to a function that displays edit screen
            edit_button = QPushButton("Edit")
            self.password_table.setCellWidget(table_row + 1, 3, edit_button)
            edit_button.clicked.connect(lambda state,
                                        password_id=curr_id, account=curr_account, password=curr_password:
                                        self.edit_password_button_click(password_id, account, password))

            # Add delete button
            delete_button = QPushButton("Delete")
            self.password_table.setCellWidget(table_row + 1, 4, delete_button)
            delete_button.clicked.connect(lambda state, password_id=curr_id, account=curr_account:
                                          self.show_delete_dialog_box(password_id, account))

            table_row += 1

        # Resize width of first column
        self.password_table.resizeColumnToContents(0)

    def build_empty_table(self, password_data):
        """
        Builds the password table with a header row and no data yet
        """

        # Define table size
        self.password_table.setRowCount(len(password_data) + 1)
        self.password_table.setColumnCount(5)

        # Populate header row
        self.password_table.setItem(0, 0, QTableWidgetItem("Account Name"))
        self.password_table.setItem(0, 1, QTableWidgetItem("Password"))
        self.password_table.setItem(0, 2, QTableWidgetItem("Copy Password"))
        self.password_table.setItem(0, 3, QTableWidgetItem("Edit Password"))
        self.password_table.setItem(0, 4, QTableWidgetItem("Delete Password"))

    def copy_button_click(self, password):
        """
        Copies the given password to the clipboard for 15 seconds then removes
        it from the clipboard using a background thread
        """
        pyperclip.copy(password)

        # Start a new thread to wait 15 seconds then clear clipboard
        thr = threading.Thread(target=clear_clipboard)
        thr.start()

    def edit_password_button_click(self, password_id, account, password):
        """
        Populates the edit screen with the existing account and password and takes
        user to the edit screen
        """
        self.parent.edit_password_screen_widget.password_id = password_id
        self.parent.edit_password_screen_widget.account_input.setText(account)
        self.parent.edit_password_screen_widget.password_input.setText(password)
        self.parent.edit_password_screen_widget.reenter_input.setText(password)
        self.parent.central_widget.setCurrentIndex(4)

    def show_delete_dialog_box(self, password_id, account):
        """
        Displays a popup button when the delete button is pressed
        """
        message_box = QMessageBox()
        message_box.setWindowTitle("Delete Password")

        # Define icon, text, and buttons
        message_box.setIcon(QMessageBox.Information)
        message_box.setText("Password for account '" + account + "' will be permanently deleted.\n"
                                                                 "Are you sure you want to delete this password?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)  # No is default button

        # Show message box
        reply_value = message_box.exec_()

        # Proceed based on which button was pressed
        if reply_value == QMessageBox.Yes:

            # Delete password from database
            delete_status = self.parent.vault_cnx.delete_password(password_id)

            # Check if deletion was successful
            if not delete_status:
                self.parent.statusBar().showMessage("Database error while deleting password.")

            self.load_password_data()


class AddEditPasswordScreen(QWidget):
    """
    This class defines a super class that allows a user to add
    a new password, edit an existing password, an generate a
    random password. This class is meant to be inherited only
    and is not a standalone class.
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()

        # Create an instruction label
        instruct_label_layout = QHBoxLayout()
        self.instruct_label = QLabel("")  # Empty, will be filled in by subclasses
        self.instruct_label.setFont(QFont("Arial", 12))

        # Center the instruction label
        instruct_label_layout.addStretch(-1)
        instruct_label_layout.addWidget(self.instruct_label)
        instruct_label_layout.addStretch(-1)
        self.instruct_label_widget = QWidget(self)
        self.instruct_label_widget.setLayout(instruct_label_layout)

        # Create account name input and account name label widgets
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Enter account name")
        self.account_label = QLabel("Account Name: ")

        # Create horizontal password layout
        account_layout = QHBoxLayout()
        account_layout.addWidget(self.account_label)
        account_layout.addWidget(self.account_input)
        self.account_widget = QWidget(self)
        self.account_widget.setLayout(account_layout)

        # Create password input and password label widgets
        self.password_input = QLineEdit()
        self.password_input.textChanged.connect(self.get_password_strength)
        self.password_input.setPlaceholderText("Enter password here")
        self.password_label = QLabel("Password: ")

        # Create progress bar to display password strength
        self.password_strength_bar = QProgressBar()
        self.password_strength_bar.setValue(0)
        self.password_strength_bar.setFormat("Very Weak")
        self.password_strength_bar.setStyleSheet("QProgressBar::chunk {"
                                                 "background-color: green; }")
        self.password_strength_bar.setAlignment(QtCore.Qt.AlignCenter)

        # Create horizontal password layout
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        self.password_widget = QWidget(self)
        self.password_widget.setLayout(password_layout)

        # Create reenter password input and reenter password label widgets
        self.reenter_input = QLineEdit()
        self.reenter_input.setPlaceholderText("Re-enter password here")
        self.reenter_label = QLabel("Re-enter\nPassword: ")

        # Create horizontal reenter password layout
        reenter_layout = QHBoxLayout()
        reenter_layout.addWidget(self.reenter_label)
        reenter_layout.addWidget(self.reenter_input)
        self.reenter_widget = QWidget(self)
        self.reenter_widget.setLayout(reenter_layout)

        # Create a label to tell user if passwords match or not
        self.password_match_label = QLabel("")

        # Create a widget to generate a random password
        self.generate_widget = GeneratePasswordWidget()
        self.generate_widget.generate_button.clicked.connect(self.generate_password)

        # Add all widgets to layout
        self.layout.addWidget(self.instruct_label_widget)
        self.layout.addWidget(self.account_widget)
        self.layout.addWidget(self.password_widget)
        self.layout.addWidget(self.reenter_widget)
        self.layout.addWidget(self.password_strength_bar)
        self.layout.addWidget(self.password_match_label)
        self.layout.addWidget(self.generate_widget)

    def generate_password(self):
        """
        Calls the RPyC microservice to generate a password of a specified length
        that may contain uppercase, numbers, or special characters depending on
        the user options
        """

        # Get values for password length and user options
        password_length = self.generate_widget.char_length_box.value()
        has_special_chars = self.generate_widget.special_chars_check.isChecked()
        has_number = self.generate_widget.numbers_check.isChecked()
        has_uppercase = self.generate_widget.case_check.isChecked()

        # Call RPyC microservice to generate password
        try:
            conn = rpyc.connect("localhost", 18861)
            generated_password = conn.root.exposed_get_password(password_length, has_uppercase,
                                                                has_number, has_special_chars)
        except ConnectionRefusedError:
            self.parent.statusBar().showMessage("Error connecting to microservice")
        else:
            self.parent.statusBar().showMessage("Ready")
            self.password_input.setText(generated_password)
            self.reenter_input.setText(generated_password)

    def get_password_strength(self):
        """
        This method is called every time the password input field is changed. The
        password bit entropy is calculated and the corresponding strength is
        displayed.
        """
        bit_entropy = password_entropy.get_entropy(self.password_input.text())
        password_strength_text = password_entropy.get_password_strength(bit_entropy)

        # Calculate password strength of out 150 bits
        strength_percentage = int((bit_entropy / 150 * 100))
        if strength_percentage > 100:
            strength_percentage = 100

        # Change progress bar format and text
        self.password_strength_bar.setValue(strength_percentage)
        password_strength_with_bits = password_strength_text + " (" + str(round(bit_entropy, 2)) + " bits)"
        self.password_strength_bar.setFormat(password_strength_with_bits)

        self.set_color_of_password_strength_bar(password_strength_text)

    def set_color_of_password_strength_bar(self, password_strength_text):
        """
        Sets the color of the password strength bar given a string of text
        describing the password strength
        """
        if password_strength_text == "Very Weak" or password_strength_text == "Weak":
            color = "red"
        elif password_strength_text == "Moderately Strong":
            color = "yellow"
        elif password_strength_text == "Strong":
            color = "#80c342"
        else:
            color = "#18b549"

        self.password_strength_bar.setStyleSheet("QProgressBar::chunk { background-color: " + color + "; }")


class GeneratePasswordWidget(QWidget):
    """
    This class defines a widget that allows a user to generate
    a random password with various options on what letters and
    symbols will be included
    """

    def __init__(self):
        super().__init__()
        vertical_layout = QVBoxLayout()

        # Create a instructional label
        self.generate_label = QLabel("Optional: Automatically generate a secure, random password using below options.\n"
                                     "\tWithout options, password will only contain random lowercase letters.")
        self.generate_label.setStyleSheet("border-top: 1px solid gray;"
                                          "border-bottom: 1px solid gray;")
        vertical_layout.addWidget(self.generate_label)

        # Create a horizontal layout with checkboxes for password options
        horizontal_layout = QHBoxLayout()
        self.special_chars_check = QCheckBox("Special Characters")
        self.numbers_check = QCheckBox("Numbers")
        self.case_check = QCheckBox("Upper Case")
        self.generate_button = QPushButton("Generate")

        # Create spinbox and label for password character length input
        self.char_length_box = QSpinBox()
        self.char_length_box.setMinimum(12)
        self.char_length_box.setMaximum(40)
        self.spinbox_label = QLabel("Number of\nCharacters")

        # Create vertical layout and widget for spinbox and label
        spinbox_layout = QVBoxLayout()
        spinbox_layout.addWidget(self.spinbox_label)
        spinbox_layout.addWidget(self.char_length_box)
        self.spinbox_widget = QWidget()
        self.spinbox_widget.setLayout(spinbox_layout)

        # Add checkboxes, spinbox, and button to layout
        horizontal_layout.addWidget(self.special_chars_check)
        horizontal_layout.addWidget(self.numbers_check)
        horizontal_layout.addWidget(self.case_check)
        horizontal_layout.addWidget(self.spinbox_widget)
        horizontal_layout.addWidget(self.generate_button)
        self.horizontal_layout_widget = QWidget(self)
        self.horizontal_layout_widget.setLayout(horizontal_layout)

        # Add checkboxes and button to vertical layout and set layout for this widget
        vertical_layout.addWidget(self.horizontal_layout_widget)
        self.setLayout(vertical_layout)


class AddPasswordScreen(AddEditPasswordScreen):
    """
    This class is a sublcass of the AddEditPasswordScreen widget.
    It defines the user interface that allows the user to add a
    password to the password vault database.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Change label text
        self.instruct_label.setText("Enter the below information to add an account and password.")

        # Create buttons to add password or cancel
        add_cancel_buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Password")
        self.cancel_button = QPushButton("Cancel")
        add_cancel_buttons_layout.addWidget(self.add_button)
        add_cancel_buttons_layout.addWidget(self.cancel_button)
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(add_cancel_buttons_layout)

        # Add button to layout
        self.layout.addWidget(self.buttons_widget)
        self.setLayout(self.layout)


class EditPasswordScreen(AddEditPasswordScreen):
    """
    This class is a subclass of the AddEditPasswordScreen widget.
    Instead of allowing the user to add a new password it allows
    the user to update an existing password.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a data member to store password id
        self.password_id = None

        # Change label text
        self.instruct_label.setText("Change the below information to edit an existing account and password.")

        # Create buttons to edit password or cancel
        edit_cancel_buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit Password")
        self.cancel_button = QPushButton("Cancel")
        edit_cancel_buttons_layout.addWidget(self.edit_button)
        edit_cancel_buttons_layout.addWidget(self.cancel_button)
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(edit_cancel_buttons_layout)

        # Add button to layout
        self.layout.addWidget(self.buttons_widget)
        self.setLayout(self.layout)


def clear_clipboard():
    """
    Waits 15 seconds then clears the clipboard
    """
    time.sleep(15)
    pyperclip.copy("")


def main():
    """
    Creates the GUI for this application
    """
    app = QApplication([])
    main_window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
