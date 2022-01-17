# Author: Ian Docherty
# Date: 1/16/2022
# Description: This module defines all of the classes and methods for the
#              password vault graphical user interface.

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QPushButton, \
                            QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, \
                            QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QFont


class MainWindow(QMainWindow):
    """
    This class defines the main window for the GUI where all
    widgets for this application reside
    """

    def __init__(self):
        """
        Create a MainWindow object and start at the login screen
        """
        super().__init__()

        # Create stacked widget and set central widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create a LoginScreen object and define slot button slots
        self.login_screen_widget = LoginScreen()
        self.login_screen_widget.login_button.clicked.connect(self.login_button_click)
        self.login_screen_widget.create_account_button.clicked.connect(self.create_account_button_click)

        # Create a CreateAccountScreen object and define button slots
        self.create_account_screen_widget = CreateAccountScreen()
        self.create_account_screen_widget.create_account_button.clicked.connect(self.create_login_button_click)

        # Create a MainScreen object and define button slots
        self.main_screen_widget = MainScreen()
        self.main_screen_widget.add_password_button.clicked.connect(self.add_password_button_click)

        # Create an AddPasswordScreen object and define button slots
        self.add_password_screen_widget = AddPasswordScreen()
        self.add_password_screen_widget.cancel_button.clicked.connect(self.add_password_cancel_button_click)

        # Add all screen widgets to stacked widget indexes
        self.central_widget.addWidget(self.login_screen_widget)  # Index 0
        self.central_widget.addWidget(self.create_account_screen_widget)  # Index 1
        self.central_widget.addWidget(self.main_screen_widget)  # Index 2
        self.central_widget.addWidget(self.add_password_screen_widget)  # Index 3
        self.central_widget.setCurrentIndex(0)  # Start at LoginScreen

        # Set window geometry and show window
        self.setGeometry(600, 500, 400, 250)
        self.setWindowTitle('PasswordVault')
        self.setWindowIcon(QIcon("./icons/key_icon.png"))
        self.statusBar().showMessage("Ready")
        self.show()

    def login_button_click(self):
        """
        Attempts to login to master account
        """
        print("Login attempted")
        self.central_widget.setCurrentIndex(2)  # To main screen
        self.setGeometry(600, 500, 550, 400)  # Make window larger

    def create_account_button_click(self):
        """
        Creates and shows the CreateAccountScreen widget to allow user
        to create a master account and password
        """
        print("Create account")
        self.central_widget.setCurrentIndex(1)

    def create_login_button_click(self):
        """
        Creates a master account and logs user into the main screen
        """
        print("Account created")
        self.central_widget.setCurrentIndex(0)  # Route back to login page

    def add_password_button_click(self):
        """
        Takes user to a new screen to add a new password to the vault
        """
        print("Add a password")
        self.central_widget.setCurrentIndex(3)

    def add_password_cancel_button_click(self):
        """
        Takes user back to main screen
        """

        # Clear user inputs and route back to main screen
        self.add_password_screen_widget.account_input.clear()
        self.add_password_screen_widget.password_input.clear()
        self.add_password_screen_widget.reenter_input.clear()
        self.central_widget.setCurrentIndex(2)  # Back to main screen


class LoginScreen(QWidget):
    """
    This class defines the login screen from the GUI
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
        self.welcome_label = QLabel("   Welcome to your password vault!\nPlease enter your password to login.")
        self.welcome_label.setFont(QFont("Arial", 12))

        # Center the welcome label
        welcome_label_layout.addStretch(-1)
        welcome_label_layout.addWidget(self.welcome_label)
        welcome_label_layout.addStretch(-1)
        self.welcome_widget = QWidget(self)
        self.welcome_widget.setLayout(welcome_label_layout)

        # Create password input and password label widgets
        self.password_input = QLineEdit()
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
        self.password_incorrect_label.setText("Password incorrect. Please enter correct password.")
        self.password_incorrect_label.setStyleSheet("background-color: yellow;")

        # Create login button layout
        self.login_button = QPushButton("Login")

        # Create a label to explain how to create an account
        # TODO: This only happens if a user not already created in database
        self.create_account_label = QLabel("\nNew user? Click below to create a master account and password.")
        self.create_account_label.setFont(QFont("Arial", 10))

        # Create a "Create Account" button
        # TODO: This only happens if a user not already created in database
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
        layout = QVBoxLayout()

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
        self.password_match_label.setText("Passwords must match")
        self.password_match_label.setStyleSheet("background-color: yellow;")

        # Create a button to create account and login
        self.create_account_button = QPushButton("Create Account")

        # Add all widgets to this layout
        layout.addWidget(self.account_icon_widget)
        layout.addWidget(self.instruct_label_widget)
        layout.addWidget(self.name_widget)
        layout.addWidget(self.password_widget)
        layout.addWidget(self.reenter_widget)
        layout.addWidget(self.password_match_label)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)


class MainScreen(QWidget):
    """
    This class defines the main screen for the GUI where the
    user can view all accounts and passwords and take action
    as necessary
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create welcome label
        welcome_label_layout = QHBoxLayout()
        self.welcome_label = QLabel("Welcome, " + "<User>")
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

        # Get table data from database
        # TODO: connect table to database
        sample_data = [{"account": "Amazon", "password": "12345password"},
                       {"account": "Gmail", "password": "1password"},
                       {"account": "eBay", "password": "15password"},
                       {"account": "OSU", "password": "badpassword"},
                       {"account": "Some MySQL Database", "password": "verylongpassword1231231"}]

        # Define table size
        self.password_table.setRowCount(len(sample_data) + 1)
        self.password_table.setColumnCount(5)

        # Populate header row
        self.password_table.setItem(0, 0, QTableWidgetItem("Account Name"))
        self.password_table.setItem(0, 1, QTableWidgetItem("Password"))
        self.password_table.setItem(0, 2, QTableWidgetItem("Copy Password"))
        self.password_table.setItem(0, 3, QTableWidgetItem("Edit Password"))
        self.password_table.setItem(0, 4, QTableWidgetItem("Delete Password"))

        # Populate table data
        table_row = 0
        while table_row < len(sample_data):
            self.password_table.setItem(table_row + 1, 0, QTableWidgetItem(sample_data[table_row]["account"]))

            # Replace password text with asterisks
            password_len = len(sample_data[table_row]["password"])
            password_hidden = ""
            for index in range(password_len):
                password_hidden += "*"

            self.password_table.setItem(table_row + 1, 1, QTableWidgetItem(password_hidden))

            # Add copy, edit and delete buttons
            self.copy_button = QPushButton("Copy")
            self.password_table.setCellWidget(table_row + 1, 2, self.copy_button)
            self.edit_button = QPushButton("Edit")
            self.password_table.setCellWidget(table_row + 1, 3, self.edit_button)
            self.delete_button = QPushButton("Delete")
            self.password_table.setCellWidget(table_row + 1, 4, self.delete_button)

            table_row += 1

        # Resize width of first column
        self.password_table.resizeColumnToContents(0)

        # Create button to add a password
        self.add_password_button = QPushButton("Add a new password")

        # Add all widgets to layout
        layout.addWidget(self.welcome_label_widget)
        layout.addWidget(self.password_table)
        layout.addWidget(self.add_password_button)

        self.setLayout(layout)


class AddPasswordScreen(QWidget):
    """
    This class defines the add password screen for the GUI
    where the user can add a password to the database
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create an instruction label
        instruct_label_layout = QHBoxLayout()
        self.instruct_label = QLabel("Enter below information to add a new account and password.")
        self.instruct_label.setFont(QFont("Arial", 12))

        # Center the instruction label
        instruct_label_layout.addStretch(-1)
        instruct_label_layout.addWidget(self.instruct_label)
        instruct_label_layout.addStretch(-1)
        self.instruct_label_widget = QWidget(self)
        self.instruct_label_widget.setLayout(instruct_label_layout)

        # Create buttons to add password or cancel
        add_cancel_buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Password")
        self.cancel_button = QPushButton("Cancel")
        add_cancel_buttons_layout.addWidget(self.add_button)
        add_cancel_buttons_layout.addWidget(self.cancel_button)
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(add_cancel_buttons_layout)

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
        self.password_match_label.setText("Passwords must match")
        self.password_match_label.setStyleSheet("background-color: yellow;")

        # Create a widget to generate a random password
        self.generate_widget = GeneratePasswordWidget()

        # Add all widgets to layout
        layout.addWidget(self.instruct_label_widget)
        layout.addWidget(self.account_widget)
        layout.addWidget(self.password_widget)
        layout.addWidget(self.reenter_widget)
        layout.addWidget(self.password_match_label)
        layout.addWidget(self.generate_widget)
        layout.addWidget(self.buttons_widget)
        self.setLayout(layout)


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
        self.generate_label = QLabel("Optional: Automatically generate a random password using below options.\n"
                                     "\tWithout options, password will only contain random lowercase letters.")
        vertical_layout.addWidget(self.generate_label)

        # Create a horizontal layout with checkboxes for password options
        horizontal_layout = QHBoxLayout()
        self.special_chars_check = QCheckBox("Special Characters")
        self.numbers_check = QCheckBox("Numbers")
        self.case_check = QCheckBox("Upper Case")
        self.generate_button = QPushButton("Generate")

        # Add checkboxes and button to layout
        horizontal_layout.addWidget(self.special_chars_check)
        horizontal_layout.addWidget(self.numbers_check)
        horizontal_layout.addWidget(self.case_check)
        horizontal_layout.addWidget(self.generate_button)
        self.horizontal_layout_widget = QWidget(self)
        self.horizontal_layout_widget.setLayout(horizontal_layout)

        # Add checkboxes and button to vertical layout and set layout for this widget
        vertical_layout.addWidget(self.horizontal_layout_widget)
        self.setLayout(vertical_layout)


class EditPasswordScreen(AddPasswordScreen):
    """
    This class is similar to the AddPasswordScreen widget
    but instead of allowing the user to add a new password
    it allows the user to update an existing password.
    """


def main():
    """
    Creates the GUI for this application
    """
    app = QApplication([])
    main_window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()