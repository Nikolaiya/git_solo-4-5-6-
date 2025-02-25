import sys
import sqlite3
from PyQt6 import QtWidgets, uic


def setup_database():
    conn = sqlite3.connect("coffee.sqlite")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS coffee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "Сорт" TEXT NOT NULL,
        "Степень_обжарки" TEXT NOT NULL,
        "Молотый_или_В_зернах" TEXT NOT NULL,
        "Описание" TEXT NOT NULL,
        "Цена" REAL NOT NULL,
        "Объем" INTEGER NOT NULL
    )
    """)

    cur.execute("SELECT COUNT(*) FROM coffee")
    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO coffee ("Сорт", "Степень_обжарки", "Молотый_или_В_зернах", "Описание", "Цена", "Объем") VALUES 
        (?, ?, ?, ?, ?, ?)
        """, [
            ("Эспрессо", "Тёмная обжарка", "В зернах", "Насыщенный, крепкий", 2000, 360),
            ("Капучино", "Средняя обжарка", "Растворимый", "Мягкий, сливочный", 1600, 300),
            ("Латте", "Светлая обжарка", "Растворимый", "Молочный", 1499, 350)
        ])

    conn.commit()
    conn.close()


setup_database()


class AddEditCoffeeForm(QtWidgets.QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.coffee_id = coffee_id

        self.nameInput = self.findChild(QtWidgets.QLineEdit, "nameEdit")
        self.roastInput = self.findChild(QtWidgets.QLineEdit, "roastEdit")
        self.groundInput = self.findChild(QtWidgets.QLineEdit, "groundEdit")
        self.descInput = self.findChild(QtWidgets.QLineEdit, "descEdit")
        self.priceInput = self.findChild(QtWidgets.QLineEdit, "priceEdit")
        self.volumeInput = self.findChild(QtWidgets.QLineEdit, "volumeEdit")
        self.okButton = self.findChild(QtWidgets.QPushButton, "okButton")

        if coffee_id:
            self.load_data()

        self.okButton.clicked.connect(self.save_data)

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        data = cur.fetchone()
        conn.close()

        if data:
            self.nameInput.setText(data[1])
            self.roastInput.setText(data[2])
            self.groundInput.setText(data[3])
            self.descInput.setText(data[4])
            self.priceInput.setText(str(data[5]))
            self.volumeInput.setText(str(data[6]))

    def save_data(self):
        try:
            data = (
                self.nameInput.text(),
                self.roastInput.text(),
                self.groundInput.text(),
                self.descInput.text(),
                float(self.priceInput.text()),
                int(self.volumeInput.text())
            )

            conn = sqlite3.connect("coffee.sqlite")
            cur = conn.cursor()

            if self.coffee_id:
                cur.execute("""
                    UPDATE coffee
                    SET "Сорт"=?, "Степень_обжарки"=?, "Молотый_или_В_зернах"=?, "Описание"=?, "Цена"=?, "Объем"=?
                    WHERE id=?
                """, data + (self.coffee_id,))
            else:
                cur.execute("""
                    INSERT INTO coffee ("Сорт", "Степень_обжарки", "Молотый_или_В_зернах", "Описание", "Цена", "Объем")
                    VALUES (?, ?, ?, ?, ?, ?)
                """, data)

            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения данных: {e}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM coffee")
        data = cur.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Сорт", "Степень обжарки", "Молотый/В зернах", "Описание", "Цена", "Объем"])
        self.tableWidget.verticalHeader().setVisible(False)

        for row_idx, row in enumerate(data):
            for col_idx, cell in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell)))

    def add_coffee(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec():
            self.load_data()

    def edit_coffee(self):
        selected = self.tableWidget.currentRow()
        if selected != -1:
            coffee_id = int(self.tableWidget.item(selected, 0).text())
            dialog = AddEditCoffeeForm(self, coffee_id)
            if dialog.exec():
                self.load_data()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
