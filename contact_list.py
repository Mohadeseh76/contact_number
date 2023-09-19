import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QMessageBox, QHeaderView, QScrollArea
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QColor

class PhoneBookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.createDatabase()
        self.loadContacts()

    def initUI(self):
        self.setWindowTitle('Phone Book')
        self.resize(1400, 400)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.tableWidget = QTableWidget(self.scrollArea)
        self.scrollArea.setWidget(self.tableWidget)

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Number', 'Job', 'Email'])

        # تغییر رنگ زمینه هدرهای جدول به زرد با استفاده از CSS
        header_style = "QHeaderView::section { background-color: #8DB6CD; font-size: 18px; font-weight: bold; }"
        self.tableWidget.horizontalHeader().setStyleSheet(header_style)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)  # افزودن اسکرول بار افقی

        self.searchButton = QPushButton('Search', self)
        self.searchButton.setFixedSize(115, 30)
        self.searchButton.clicked.connect(self.searchContacts)

        self.addButton = QPushButton('Add', self)
        self.addButton.setFixedSize(115, 30)
        self.addButton.clicked.connect(self.showAddDialog)

        self.editButton = QPushButton('Edit', self)
        self.editButton.setFixedSize(115, 30)
        self.editButton.clicked.connect(self.editContact)

        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.setFixedSize(115, 30)
        self.deleteButton.clicked.connect(self.deleteContact)

        self.clearAllButton = QPushButton('Clear All', self)
        self.clearAllButton.setFixedSize(115, 30)
        self.clearAllButton.clicked.connect(self.clearAllContacts)

        self.searchLineEdit = QLineEdit(self)
        self.searchLineEdit.setPlaceholderText('Search')
        self.searchLineEdit.setFixedWidth(115)  # Set a fixed width for the search bar

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.searchLineEdit)
        buttonLayout.addWidget(self.searchButton)
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.clearAllButton)
        buttonLayout.addSpacing(10)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.scrollArea)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        
        # ایجاد یک فونت جدید با سایز بزرگ و ضخامت بیشتر
        button_font = QFont("Arial", 12)  # اینجا می‌توانید سایز و نوع فونت مورد نظر خود را تنظیم کنید
        button_font.setBold(True)

        self.searchButton.setFont(button_font)
        self.addButton.setFont(button_font)
        self.editButton.setFont(button_font)
        self.deleteButton.setFont(button_font)
        self.clearAllButton.setFont(button_font)

        button_style = "background-color: #607B8B; color: white;"
        self.searchButton.setStyleSheet(button_style)
        self.addButton.setStyleSheet(button_style)
        self.editButton.setStyleSheet(button_style)
        self.deleteButton.setStyleSheet(button_style)
        self.clearAllButton.setStyleSheet(button_style)

        input_font = QFont("Arial", 16)  # اینجا می‌توانید سایز و نوع فونت مورد نظر خود را تنظیم کنید
        self.searchLineEdit.setFont(input_font)

    def createDatabase(self):
        self.conn = sqlite3.connect('phonebook.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT,
                             number TEXT,
                             job TEXT,
                             email TEXT)''')
        self.conn.commit()

    def loadContacts(self):
        self.cur.execute("SELECT name, number, job, email FROM contacts")
        contacts = self.cur.fetchall()

        self.tableWidget.setRowCount(len(contacts))

        # تغییر فونت مخاطبان به حروف بزرگتر
        contact_font = QFont("Arial", 12)  # اینجا می‌توانید سایز و نوع فونت مورد نظر خود را تنظیم کنید

        for row, contact in enumerate(contacts):
            for col, value in enumerate(contact):
                item = QTableWidgetItem(str(value))
                
                # تنظیم فونت برای هر سلول
                item.setFont(contact_font)
                
                self.tableWidget.setItem(row, col, item)
                self.tableWidget.setRowHeight(row, 80)

        # تنظیم رنگ سلول‌های عمودی به ترتیب
        for row in range(self.tableWidget.rowCount()):
            if row % 2 == 0:
                cell_color = QColor("#B8B8B8")  # رنگ طوسی
            else:
                cell_color = QColor("white")  # رنگ سفید

            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item:
                    item.setBackground(cell_color)
    def showAddDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Contact')
        dialog.setGeometry(800, 400, 400, 200)

        formLayout = QFormLayout()

        nameLineEdit = QLineEdit()
        numberLineEdit = QLineEdit()
        jobLineEdit = QLineEdit()
        emailLineEdit = QLineEdit()

        input_font = QFont("Arial", 16)
        nameLineEdit.setFont(input_font)
        numberLineEdit.setFont(input_font)
        jobLineEdit.setFont(input_font)
        emailLineEdit.setFont(input_font)

        formLayout.addRow('Name:', nameLineEdit)
        formLayout.addRow('Number:', numberLineEdit)
        formLayout.addRow('Job:', jobLineEdit)
        formLayout.addRow('Email:', emailLineEdit)

        saveButton = QPushButton('Save', dialog)
        saveButton.clicked.connect(lambda: self.saveContact(nameLineEdit, numberLineEdit, jobLineEdit, emailLineEdit))

        formLayout.addRow(saveButton)

        dialog.setLayout(formLayout)

        dialog.exec_()

    def saveContact(self, nameLineEdit, numberLineEdit, jobLineEdit, emailLineEdit):
        name = nameLineEdit.text()
        number = numberLineEdit.text()
        job = jobLineEdit.text()
        email = emailLineEdit.text()

        self.cur.execute("INSERT INTO contacts (name, number, job, email) VALUES (?, ?, ?, ?)",
                         (name, number, job, email))
        self.conn.commit()

        self.loadContacts()
        
        nameLineEdit.clear()
        numberLineEdit.clear()
        jobLineEdit.clear()
        emailLineEdit.clear()

    def __del__(self):
        self.conn.close()

    def deleteContact(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return

        # Get the name of the selected contact (the first column)
        selected_name = selected_items[0].text()

        # Delete the contact from the database
        self.cur.execute("DELETE FROM contacts WHERE name=?", (selected_name,))
        self.conn.commit()

        # Remove the selected row from the table
        selected_row = self.tableWidget.currentRow()
        self.tableWidget.removeRow(selected_row)

    def clearAllContacts(self):
        msg_box = QMessageBox.question(self, 'Clear All Contacts', 'Are you sure you want to clear all contacts?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msg_box == QMessageBox.Yes:
            self.cur.execute("DELETE FROM contacts")
            self.conn.commit()
            self.tableWidget.setRowCount(0)

    def editContact(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return

        # Get the name of the selected contact (the first column)
        selected_name = selected_items[0].text()

        # Retrieve the contact details from the database
        self.cur.execute("SELECT * FROM contacts WHERE name=?", (selected_name,))
        contact = self.cur.fetchone()
        if not contact:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('Edit Contact')
        dialog.setGeometry(800, 400, 400, 200)

        formLayout = QFormLayout()

        nameLineEdit = QLineEdit()
        nameLineEdit.setText(contact[1])
        numberLineEdit = QLineEdit()
        numberLineEdit.setText(contact[2])
        jobLineEdit = QLineEdit()
        jobLineEdit.setText(contact[3])
        emailLineEdit = QLineEdit()
        emailLineEdit.setText(contact[4])

        input_font = QFont("Arial", 16)
        nameLineEdit.setFont(input_font)
        numberLineEdit.setFont(input_font)
        jobLineEdit.setFont(input_font)
        emailLineEdit.setFont(input_font)

        formLayout.addRow('Name:', nameLineEdit)
        formLayout.addRow('Number:', numberLineEdit)
        formLayout.addRow('Job:', jobLineEdit)
        formLayout.addRow('Email:', emailLineEdit)

        saveButton = QPushButton('Save', dialog)
        saveButton.clicked.connect(lambda: self.saveEditedContact(nameLineEdit, numberLineEdit, jobLineEdit, emailLineEdit))

        formLayout.addRow(saveButton)

        dialog.setLayout(formLayout)

        dialog.exec_()

    def saveEditedContact(self, nameLineEdit, numberLineEdit, jobLineEdit, emailLineEdit):
        name = nameLineEdit.text()
        number = numberLineEdit.text()
        job = jobLineEdit.text()
        email = emailLineEdit.text()

        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return

        # Get the name of the selected contact (the first column)
        selected_name = selected_items[0].text()

        # Update the contact details in the database
        self.cur.execute("UPDATE contacts SET name=?, number=?, job=?, email=? WHERE name=?",
                         (name, number, job, email, selected_name))
        self.conn.commit()

        self.loadContacts()

        nameLineEdit.clear()
        numberLineEdit.clear()
        jobLineEdit.clear()
        emailLineEdit.clear()

    def searchContacts(self):
        search_text = self.searchLineEdit.text()
        
        if not search_text:
            self.loadContacts()
        else:
            self.cur.execute("SELECT name, number, job, email FROM contacts WHERE name LIKE ?", ('%' + search_text + '%',))
            search_results = self.cur.fetchall()
            
            self.tableWidget.setRowCount(0)
            
            for row, contact in enumerate(search_results):
                self.tableWidget.insertRow(row)
                for col, value in enumerate(contact):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)
        
        self.searchLineEdit.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhoneBookApp()
    window.show()
    sys.exit(app.exec_())
