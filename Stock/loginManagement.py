from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from cloudant.client import Cloudant
from userManagement import SignUpApp
from findStock import findStock
from portfolio import Portfolio

class LoginApp(QMainWindow):
    # Class attribute to store the username
    username = ""

    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi('login.ui', self)
        self.API_USER = "3fdf89c0-70ae-421c-8a5c-f3f07abc3988-bluemix"
        self.API_KEY = "IGzHN-SnHoE7X-Xn_wlCK0ogL62UusTafB2ZO8CZeXub"

        self.password = ""

        self.loginButton.clicked.connect(self.login_button_clicked)
        self.signupButton.clicked.connect(self.signup_button_clicked)

    def login_button_clicked(self):
        # Update the class attribute
        LoginApp.username = self.username_line.text()
        self.password = self.password_line.text()

        client = Cloudant.iam(self.API_USER, self.API_KEY, connect=True)
        database = client["users"]

        if LoginApp.username in database:
            user_doc = database[LoginApp.username]
            stored_password = user_doc.get("password", "")

            if self.password != stored_password:
                QMessageBox.information(self, "Alert", "Username or Password Is Incorrect", QMessageBox.Ok)
                return
            else:
                self.stockprice_window = Portfolio()
                self.stockprice_window.show()
                self.close()
        else:
            QMessageBox.information(self, "Alert", "Username or Password Is Incorrect", QMessageBox.Ok)
            return

    def signup_button_clicked(self):
        self.signup_window = SignUpApp()
        self.signup_window.show()
