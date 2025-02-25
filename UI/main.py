from PyQt6 import QtWidgets


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setGeometry(100, 100, 720, 450)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(10, 10, 702, 300)

        self.addButton = QtWidgets.QPushButton("Добавить", self.centralwidget)
        self.addButton.setGeometry(10, 320, 100, 30)

        self.editButton = QtWidgets.QPushButton("Редактировать", self.centralwidget)
        self.editButton.setGeometry(120, 320, 100, 30)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)