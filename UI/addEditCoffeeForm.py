from PyQt6 import QtWidgets


class Ui_AddEditCoffeeForm:
    def setupUi(self, AddEditCoffeeForm):
        AddEditCoffeeForm.setGeometry(100, 100, 300, 300)

        self.centralwidget = QtWidgets.QWidget(AddEditCoffeeForm)

        self.nameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nameEdit.setGeometry(10, 10, 280, 30)
        self.nameEdit.setPlaceholderText("Введите сорт")

        self.roastEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.roastEdit.setGeometry(10, 50, 280, 30)
        self.roastEdit.setPlaceholderText("Введите Степень прожарки")

        self.groundEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.groundEdit.setGeometry(10, 90, 280, 30)
        self.groundEdit.setPlaceholderText("В зернах или молотый?")

        self.descEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.descEdit.setGeometry(10, 130, 280, 30)
        self.descEdit.setPlaceholderText("Введите описание")

        self.priceEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.priceEdit.setGeometry(10, 170, 280, 30)
        self.priceEdit.setPlaceholderText("Введите цену")

        self.volumeEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.volumeEdit.setGeometry(10, 210, 280, 30)
        self.volumeEdit.setPlaceholderText("Введите объем")

        self.okButton = QtWidgets.QPushButton("OK", self.centralwidget)
        self.okButton.setGeometry(10, 250, 280, 40)

        AddEditCoffeeForm.setLayout(QtWidgets.QVBoxLayout())
        AddEditCoffeeForm.layout().addWidget(self.centralwidget)
