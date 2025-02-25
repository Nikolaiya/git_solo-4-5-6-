import sys
import sqlite3
from PyQt6 import QtWidgets
from UI.main import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_AddEditCoffeeForm


def setup_database():
    conn = sqlite3.connect("data/coffee.sqlite")
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


class AddEditCoffeeForm(QtWidgets.QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.coffee_id = coffee_id

        if coffee_id:
            self.load_data()

        self.okButton.clicked.connect(self.save_data)

    def load_data(self):
        conn = sqlite3.connect("data/coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        data = cur.fetchone()
        conn.close()

        if data:
            self.nameEdit.setText(data[1])
            self.roastEdit.setText(data[2])
            self.groundEdit.setText(data[3])
            self.descEdit.setText(data[4])
            self.priceEdit.setText(str(data[5]))
            self.volumeEdit.setText(str(data[6]))

    def save_data(self):
        try:
            conn = sqlite3.connect("data/coffee.sqlite")
            cur = conn.cursor()

            data = (
                self.nameEdit.text(),
                self.roastEdit.text(),
                self.groundEdit.text(),
                self.descEdit.text(),
                float(self.priceEdit.text()),
                int(self.volumeEdit.text())
            )

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


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Запускаем UI
        self.load_data()

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect("data/coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM coffee")
        data = cur.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Сорт", "Степень обжарки", "Молотый/В зернах", "Описание", "Цена", "Объем"]
        )
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
