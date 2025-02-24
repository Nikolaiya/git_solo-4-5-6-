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

    # Проверяем, есть ли уже данные
    cur.execute("SELECT COUNT(*) FROM coffee")
    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO coffee ("Сорт", "Степень_обжарки", "Молотый_или_В_зернах", "Описание", "Цена", "Объем") VALUES 
        (?, ?, ?, ?, ?, ?)
        """, [
            ("Эспрессо", "Тёмная обжарка", "В зернах", "Насыщенный, крепкий", 2000, 360),
            ("Капучино", "Средняя обжарка", "Растворимый", "Мягкий, сливочный", 1600, 300),
            ("Латте", "Светлая обжарка", "Растворимый", "молочный", 1499, 350)
        ])

    conn.commit()
    conn.close()

setup_database()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.tableWidget = None
        uic.loadUi("main.ui", self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM coffee")
        data = cur.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)

        stolb = ["ID", "Сорт", "Степень обжарки", "Молотый/В зернах", "Описание", "Цена", "Объем"]
        self.tableWidget.setHorizontalHeaderLabels(stolb)

        self.tableWidget.verticalHeader().setVisible(False)

        for row_idx, row in enumerate(data):
            for col_idx, cell in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell)))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())