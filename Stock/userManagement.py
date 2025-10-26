from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from cloudant.client import Cloudant
import sys

class SignUpApp(QMainWindow):
    def __init__(self):
        print("I RAN")
        super(SignUpApp, self).__init__()
        loadUi('signup.ui', self)
        self.show()

        self.API_USER = "3fdf89c0-70ae-421c-8a5c-f3f07abc3988-bluemix"
        self.API_KEY = "IGzHN-SnHoE7X-Xn_wlCK0ogL62UusTafB2ZO8CZeXub"

        self.fName = ""
        self.lName = ""
        self.username = ""
        self.password = ""
        self.confPassword = ""

        self.signupbutton.clicked.connect(self.signup_button_clicked)

    def signup_button_clicked(self):
        self.fName = self.firstname_line.text()
        self.lName = self.lastname_line.text()
        self.username = self.username_line.text()
        self.password = self.password_line.text()
        self.confPassword = self.confirm_password_line.text()

        # Check if passwords match before proceeding
        if self.password != self.confPassword:
            print("Passwords do not match!")
            return

        try:
            client = Cloudant.iam(self.API_USER, self.API_KEY, connect=True)
            database = client["users"]

            data = {
                "_id": self.username,
                "username": self.username,
                "password": self.password,
                "first name": self.fName,
                "last name": self.lName,
            }

            my_doc = database.create_document(data)
            print("Document created successfully!")
            self.close()

        except Exception as e:
            print(f"Error: {e}")

