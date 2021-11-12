from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidgetItem, QShortcut
from functions import update_table
from PyQt5.QtCore import Qt

from akinator_database_cursor import Question


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(690, 480)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")

        self.error_label = QtWidgets.QLabel(Form)
        self.error_label.setObjectName("error_label")

        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")

        self.horizontal_layout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.horizontal_layout.addWidget(self.error_label)

        self.verticalLayout.addLayout(self.horizontal_layout)

        self.question_text_edit = QtWidgets.QLineEdit(Form)
        self.question_text_edit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.question_text_edit)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.subject_search_phrase = QtWidgets.QLineEdit(Form)
        self.subject_search_phrase.setAlignment(QtCore.Qt.AlignCenter)
        self.subject_search_phrase.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.subject_search_phrase)
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.verticalHeader().hide()
        self.verticalLayout.addWidget(self.table)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_add_decline = QtWidgets.QPushButton(Form)
        self.btn_add_decline.setObjectName("btn_add_decline")
        self.horizontalLayout.addWidget(self.btn_add_decline)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_add_accept = QtWidgets.QPushButton(Form)
        self.btn_add_accept.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_add_accept.setObjectName("btn_add_accept")
        self.horizontalLayout.addWidget(self.btn_add_accept)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор вопроса"))
        self.label.setText(_translate("Form", "Текст вопроса"))
        self.subject_search_phrase.setPlaceholderText(_translate("Form", "Поиск по названию..."))
        self.btn_add_decline.setText(_translate("Form", "Отмена"))
        self.btn_add_accept.setText(_translate("Form", "Добавить"))


class QuestionEditorWindowWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None, question_object=None):
        super().__init__()
        self.setupUi(self)
        self.childs = []
        self.parent = parent
        self.question_object = question_object

        self.current_found_item = None
        self.found_items = []

        self.btn_add_accept.clicked.connect(self.btn_add_accept_clicked)
        self.btn_add_decline.clicked.connect(self.btn_add_decline_clicked)

        self.subject_search_phrase.textChanged.connect(self.search_phrase_edited)

        self.table.verticalHeader().hide()
        self.table.adjustSize()

        self.tableCheckBoxes = {}

        self.shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        self.shortcut.activated.connect(self.key_tab_pressed)

        subjects = self.parent.my_cursor.get_all_subjects()

        for i in range(len(subjects)):
            new_subject = (*subjects[i], QtWidgets.QCheckBox())
            subjects[i] = new_subject

        self.update_table(subjects, headers=['ID', 'Текст', 'Тип', ''])

        if question_object is not None:
            self.fill_fields()

    def btn_add_accept_clicked(self):
        self.error_label.setText('')
        question_text = self.question_text_edit.text()
        if not question_text:
            self.error_label.setText('Текст вопроса не может быть пустым')
            return
        subjects_ids = []
        for row in range(self.table.rowCount()):
            check_box_item = self.tableCheckBoxes[self.table.item(row, 0).text()]

            if check_box_item.checkState():
                subjects_ids.append(self.table.item(row, 0).text())

        if self.question_object is None:
            question = Question()
            question.question_text = question_text
            question.subjects_ids = subjects_ids
            self.parent.my_cursor.add_question(question)
        else:
            self.question_object.question_text = question_text
            self.question_object.subjects_ids = subjects_ids
            self.parent.my_cursor.edit_question(self.question_object)

        self.parent.update_table()
        self.close()

    def btn_add_decline_clicked(self):
        self.close()

    def search_phrase_edited(self):
        phrase = self.subject_search_phrase.text().strip()
        self.found_items = []
        self.current_found_item = None
        self.search_phrase_in_table(self.table, phrase)

    def search_phrase_in_table(self, table, phrase):
        table.setCurrentItem(None)
        founded = table.findItems(phrase, Qt.MatchContains)

        self.found_items = [x for x in founded if x is not None]
        self.current_found_item = -1
        self.key_tab_pressed()

    def update_table(self, data, headers=None):
        # Заполним размеры таблицы
        self.table.setColumnCount(len(data[0]))
        self.table.setRowCount(0)
        if headers is not None:
            self.table.setHorizontalHeaderLabels(headers)

        # Заполняем таблицу элементами
        for i, row in enumerate(data):
            self.table.setRowCount(
                self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if isinstance(elem, QtWidgets.QCheckBox):
                    self.table.setCellWidget(i, j, elem)
                    self.tableCheckBoxes[str(i + 1)] = elem
                else:
                    self.table.setItem(i, j, QTableWidgetItem(str(elem)))

        self.table.resizeColumnsToContents()

    def key_tab_pressed(self):
        if self.current_found_item is not None and self.found_items:
            self.found_items[self.current_found_item].setSelected(False)

            self.current_found_item += 1
            self.current_found_item %= len(self.found_items)

            self.table.setCurrentItem(self.found_items[self.current_found_item])
            self.found_items[self.current_found_item].setSelected(True)

    def fill_fields(self):
        self.question_object: Question
        self.question_text_edit.setText(self.question_object.question_text)
        checked_subjects = self.question_object.subjects_ids
        for subject_id in checked_subjects:
            self.tableCheckBoxes[str(subject_id)].setChecked(True)
