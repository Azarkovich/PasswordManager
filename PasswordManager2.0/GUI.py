""" Password Manager 2.0 """

# ------------------------------------------ IMPORTS ---------------------------------------
from PySide2.QtWidgets import QLabel
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
from API import Passgen
import json
import random
import string
import PySide2.QtCore



# ----------------------------------------- UI SETUP ------------------------------------------
class App(QtWidgets.QWidget):
    def __init__(self):

        super().__init__()

        self.setWindowTitle("Password Manager 2.0")
        self.setup_ui()
        self.resize(720,432)
        self.setup_icon()
        self.setup_connections()

    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self) # => Main window 
        
        # Label
        self.la_website = QLabel("Website URL: ")
        self.la_username = QLabel("Email / Username: ")
        self.la_password = QLabel("Password: ")
        self.la_password_list = QLabel("Password List: ")

        #Line Edit 
        self.le_website_entry = QtWidgets.QLineEdit(self)
        self.le_website_entry.setPlaceholderText("https://Azarkovich.de")
        self.le_username_entry = QtWidgets.QLineEdit(self)
        self.le_username_entry.setPlaceholderText("youremail.com")
        self.le_username_entry.size()
        self.le_password_entry = QtWidgets.QLineEdit(self)
        self.le_password_entry.setPlaceholderText("123Password")
        
        # Button
        self.btn_generate_password = QtWidgets.QPushButton("Generate Password")
        self.btn_add_password = QtWidgets.QPushButton("Add Password")
        self.btn_remove_password = QtWidgets.QPushButton("Remove Password")

        #Line Widget
        self.lw_password_list = QtWidgets.QListWidget()

        #Add Widget
        self.main_layout.addWidget(self.la_website)
        self.main_layout.addWidget(self.le_website_entry)

        self.main_layout.addWidget(self.la_username)
        self.main_layout.addWidget(self.le_username_entry)

        self.main_layout.addWidget(self.la_password)
        self.main_layout.addWidget(self.le_password_entry)
        self.main_layout.addWidget(self.btn_generate_password)
        self.main_layout.addWidget(self.btn_add_password)

        self.main_layout.addWidget(self.la_password_list)
        self.main_layout.addWidget(self.lw_password_list)
        self.main_layout.addWidget(self.btn_remove_password)

    def setup_icon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)


    def setup_connections(self):
        self.btn_generate_password.clicked.connect(self.generate_password)
        self.btn_add_password.clicked.connect(self.add_password)
        self.btn_remove_password.clicked.connect(self.remove_password)


# ------------------------------------------- PASSGEN ----------------------------------
    def generate_password(self):
        min_password = 8
        max_password = 32 
        allchars = string.ascii_letters + string.punctuation + string.digits
        password = "".join(random.choice(allchars) for char in range (random.randint(min_password, max_password)))
        self.le_password_entry.setText(password)
        print("Password Generated ! ")


    def add_password(self):
        url = self.le_website_entry.text()
        username = self.le_username_entry.text()
        password = self.le_password_entry.text()
        if url and username and password:
            password_item = QtWidgets.QListWidgetItem(f"URL: {url}, Username: {username}, Password: {password}")
            self.lw_password_list.addItem(password_item)

            data = {
                'url' : url,
                'username' : username,
                'password' : password
            }
            
            with open ("passwords_list.json", "a") as f:
                json.dump(data, f, indent=4)
                f.write('\n')


            with open ("passwords_list.txt", "a") as jfile:
                json.dump(data, jfile, indent=4)
                jfile.write('\n')

            self.clear_input_fields()

    def clear_input_fields(self):
        self.le_username_entry.clear()
        self.le_website_entry.clear()
        self.le_password_entry.clear()


    def remove_password(self):
        for selected_item in self.lw_password_list.selectedItems():
            password = selected_item.data(QtCore.Qt.UserRole) 
            password.remove_password()
            self.lw_password_list.takeItem(self.lw_password_list.row(selected_item))




app = QtWidgets.QApplication([])
wdw = App()
wdw.show()
app.exec_()
