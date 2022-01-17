# Author: Ian Docherty
# Date: 1/16/2022
# Description: This module defines all of the classes and methods for the
#              password vault graphical user interface.

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QPushButton, \
                            QLabel, QVBoxLayout, QLineEdit, QHBoxLayout
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

        # Add all screen widgets to stacked widget indexes
        self.central_widget.addWidget(self.login_screen_widget)  # Index 0
        self.central_widget.addWidget(self.create_account_screen_widget)  # Index 1
        self.central_widget.addWidget(self.main_screen_widget)  # Index 2
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
        self.central_widget.setCurrentIndex(2)
        self.setGeometry(600, 500, 600, 400)

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


class LoginScreen(QWidget):
    """
    This class defines the login screen from the GUI
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

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

        # Create a button to create account and login
        self.create_account_button = QPushButton("Create account and login")

        # Add all widgets to this layout
        layout.addWidget(self.account_icon_widget)
        layout.addWidget(self.instruct_label_widget)
        layout.addWidget(self.name_widget)
        layout.addWidget(self.password_widget)
        layout.addWidget(self.reenter_widget)
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

        self.instruct_label = QLabel("Main application screen.")
        self.instruct_label.setFont(QFont("Arial", 12))

        layout.addWidget(self.instruct_label)

        self.setLayout(layout)


class AddPasswordScreen(QWidget):
    """
    This class defines the add password screen for the GUI
    where the user can add a password to the database
    """


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