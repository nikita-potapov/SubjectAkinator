import sys
from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget

from PyQt5 import QtCore, QtGui, QtWidgets

SUBJECTS_FILENAME = "subjects.csv"


class Ui_Form_Start_Window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 500)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(223, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.text_label = QtWidgets.QLabel()
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout.addWidget(self.text_label)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.btn_start = QtWidgets.QPushButton(Form)
        self.btn_start.setObjectName("btn_start")
        self.verticalLayout.addWidget(self.btn_start)

        self.error_text_line = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.error_text_line)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(223, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SubjectAkinator"))
        self.text_label.setText(_translate("Form", "Введите название предмета"))
        self.btn_start.setText(_translate("Form", "Начать"))


class StartWindowWidget(QWidget, Ui_Form_Start_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.child = None
        self.btn_start.clicked.connect(self.btn_start_clicked)

        self.subjects = []
        self.load_subjects()

    def btn_start_clicked(self):
        subject_name = self.lineEdit.text().strip()
        result = self.check_subject_name(subject_name)
        if not result:
            return
        self.child = QuestionsWindowWidget()
        self.child.show()
        self.close()

    def check_subject_name(self, subject_name):
        if not subject_name:
            self.error_text_line.setText(f'Ошибка! Введите название предмета')
            return False
        if subject_name not in self.subjects:
            self.error_text_line.setText(f'Предмет \"{subject_name}\" не найден')
            return False
        return True

    def load_subjects(self):
        with open(SUBJECTS_FILENAME, encoding='UTF-8') as file:
            data = file.read()
        data = [x.split(';') for x in data.split('\n')]

        print(len(data), len(data[0]))


class Ui_Form_Questions_Window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(709, 509)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(57, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.question_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.question_label.setFont(font)
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_label.setObjectName("question_label")
        self.verticalLayout.addWidget(self.question_label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_answer_no = QtWidgets.QPushButton(Form)
        self.btn_answer_no.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btn_answer_no.setFont(font)
        self.btn_answer_no.setObjectName("btn_answer_no")
        self.horizontalLayout.addWidget(self.btn_answer_no)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.btn_answer_yes = QtWidgets.QPushButton(Form)
        self.btn_answer_yes.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btn_answer_yes.setFont(font)
        self.btn_answer_yes.setObjectName("btn_answer_yes")
        self.horizontalLayout.addWidget(self.btn_answer_yes)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(56, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.question_number_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_number_label.setFont(font)
        self.question_number_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.question_number_label.setObjectName("question_number_label")
        self.horizontalLayout_2.addWidget(self.question_number_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SubjectAkinator"))
        self.question_label.setText(_translate("Form", "TextLabel"))
        self.btn_answer_no.setText(_translate("Form", "Нет"))
        self.btn_answer_yes.setText(_translate("Form", "Да"))
        self.question_number_label.setText(_translate("Form", "3/10"))


class QuestionsWindowWidget(QWidget, Ui_Form_Questions_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindowWidget()
    ex.show()
    sys.exit(app.exec())
