from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from akinator_database_cursor import Subject


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(429, 127)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(429, 127))
        Form.setMaximumSize(QtCore.QSize(429, 127))
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 427, 125))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.subject_name = QtWidgets.QLineEdit(self.widget)
        self.subject_name.setMinimumSize(QtCore.QSize(300, 0))
        self.subject_name.setObjectName("lineEdit")
        self.horizontalLayout_5.addWidget(self.subject_name)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_1_course = QtWidgets.QRadioButton(self.widget)
        self.radioButton_1_course.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton_1_course)
        self.radioButton_2_course = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2_course.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2_course)
        self.radioButton_3_course = QtWidgets.QRadioButton(self.widget)
        self.radioButton_3_course.setObjectName("radioButton_3")
        self.horizontalLayout.addWidget(self.radioButton_3_course)
        self.radioButton_4_course = QtWidgets.QRadioButton(self.widget)
        self.radioButton_4_course.setObjectName("radioButton_4")
        self.horizontalLayout.addWidget(self.radioButton_4_course)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        self.btn_cancel.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.btn_cancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_accept = QtWidgets.QPushButton(self.widget)
        self.btn_accept.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.btn_accept)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор предмета"))
        self.label.setText(_translate("Form", "Название предмета"))
        self.label_2.setText(_translate("Form", "Номер курса"))
        self.radioButton_1_course.setText(_translate("Form", "1"))
        self.radioButton_2_course.setText(_translate("Form", "2"))
        self.radioButton_3_course.setText(_translate("Form", "3"))
        self.radioButton_4_course.setText(_translate("Form", "4"))
        self.label_3.setText(_translate("Form", "Класс предмета"))
        self.btn_cancel.setText(_translate("Form", "Отмена"))
        self.btn_accept.setText(_translate("Form", "Принять"))


class SubjectEditorWindowWidget(QWidget, Ui_Form):
    def __init__(self, parent=None, subject_object=None):
        super().__init__()
        self.setupUi(self)
        self.childs = []
        self.parent = parent
        self.subject_object = subject_object

        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_accept.clicked.connect(self.btn_accept_clicked)

        self.fill_combobox()

        if self.subject_object is not None:
            self.fill_fields()

    def fill_fields(self):
        self.subject_name.setText(self.subject_object.subject_name)
        radio_button = getattr(self, f"radioButton_{self.subject_object.subject_course}_course")
        radio_button.setChecked(True)
        self.set_combobox()

    def btn_accept_clicked(self):
        subject = Subject()
        for i in range(1, 5):
            if getattr(self, f'radioButton_{i}_course').isChecked():
                subject.subject_course = i
                break

        subject.subject_way_of_study = self.comboBox.currentText()
        subject.subject_name = self.subject_name.text().strip()

        if self.subject_object is not None:
            subject.subject_id = self.subject_object.subject_id
            self.parent.my_cursor.edit_subject(subject)
        else:
            self.parent.my_cursor.add_subject(subject)

        self.parent.update_table()
        self.close()

    def fill_combobox(self):
        ways_of_study = self.parent.my_cursor.get_all_ways_of_study()
        for i in range(len(ways_of_study)):
            name = ways_of_study[i][1]
            self.comboBox.addItems([name])
            self.comboBox.setCurrentIndex(i)

    def set_combobox(self):
        for i in range(self.comboBox.count()):
            if self.comboBox.itemText(i) == self.subject_object.subject_way_of_study:
                self.comboBox.setCurrentIndex(i)
                break

    def btn_cancel_clicked(self):
        self.close()
