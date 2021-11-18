import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QMessageBox

from sources.question_editor import QuestionEditorWindowWidget
from sources.subject_editor import SubjectEditorWindowWidget
from sources.functions import update_table
from sources.akinator_database_cursor import SubjectAkinatorDatabaseCursor, Subject, Question
from settings import DB_FILENAME


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(745, 458)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_mode = QtWidgets.QComboBox(Form)
        self.comboBox_mode.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_mode)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_delete = QtWidgets.QPushButton(Form)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.btn_add = QtWidgets.QPushButton(Form)
        self.btn_add.setMinimumSize(QtCore.QSize(150, 0))
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.search_phrase_lineEdit = QtWidgets.QLineEdit(Form)
        self.search_phrase_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.search_phrase_lineEdit.setObjectName("search_phrase")
        self.verticalLayout.addWidget(self.search_phrase_lineEdit)
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setTabKeyNavigation(False)
        self.verticalLayout.addWidget(self.table)

        icon = QtGui.QIcon('resources\\akinator_configurator.ico')
        Form.setWindowIcon(icon)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SubjectAkinatorConfiguration"))
        self.comboBox_mode.setItemText(0, _translate("Form", "Предметы"))
        self.comboBox_mode.setItemText(1, _translate("Form", "Вопросы"))
        self.btn_delete.setText(_translate("Form", "Удалить"))
        self.btn_add.setText(_translate("Form", "Добавить"))
        self.search_phrase_lineEdit.setPlaceholderText(_translate("Form", "Поиск..."))


class MyApplication(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.childs = []

        self.current_mode = None

        self.comboBox_mode.currentTextChanged.connect(self.combo_box_changed)
        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_clicked)

        self.table.doubleClicked.connect(self.table_item_double_clicked)

        self.my_cursor = SubjectAkinatorDatabaseCursor(DB_FILENAME)
        self.combo_box_changed()

        self.search_phrase_lineEdit.textChanged.connect(self.search_phrase_edited)
        self.found_items = []
        self.current_found_item = None

        self.shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        self.shortcut.activated.connect(self.key_tab_pressed)

    def btn_add_clicked(self):
        child = None
        if self.current_mode == 'Вопросы':
            child = QuestionEditorWindowWidget(parent=self)
        elif self.current_mode == 'Предметы':
            child = SubjectEditorWindowWidget(parent=self)

        if child:
            self.childs.append(child)
            child.show()

    def btn_delete_clicked(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        selected_id = int(selected_items[0].text())

        print(selected_id)

        if self.current_mode == 'Предметы':
            self.my_cursor.delete_subject(selected_id)
        if self.current_mode == 'Вопросы':
            self.my_cursor.delete_question(selected_id)

        self.update_table()

    def combo_box_changed(self):
        self.current_mode = self.comboBox_mode.currentText()

        data = None
        headers = None

        if self.current_mode == 'Предметы':
            data = self.my_cursor.get_all_subjects()
            headers = ['ID', 'Название', 'класс']

        elif self.current_mode == 'Вопросы':
            data = self.my_cursor.get_all_questions()
            headers = ['ID', 'Текст', 'Отсеивает']

        update_table(self.table, data, headers=headers)

    def table_item_double_clicked(self):
        items_selected = self.table.selectedItems()
        if not items_selected:
            return
        item_selected_id = int(items_selected[0].text())

        if self.current_mode == 'Предметы':
            subject = self.my_cursor.get_subject(item_selected_id)[0]

            subject_object = Subject()
            subject_object.subject_id = subject[0]
            subject_object.subject_name = subject[1]
            subject_object.subject_course = subject[2]
            subject_object.subject_way_of_study = subject[3]

            child = SubjectEditorWindowWidget(parent=self, subject_object=subject_object)
            self.childs.append(child)
            child.show()

        if self.current_mode == 'Вопросы':
            question = self.my_cursor.get_question(item_selected_id)[0]

            question_object = Question()
            question_object.question_id = question[0]
            question_object.question_text = question[1]
            question_object.subjects_ids = question[2]

            child = QuestionEditorWindowWidget(parent=self, question_object=question_object)
            self.childs.append(child)
            child.show()

    def update_table(self):
        self.combo_box_changed()

    def search_phrase_edited(self):
        phrase = self.search_phrase_lineEdit.text().strip()
        self.found_items = []
        self.current_found_item = None
        self.search_phrase_in_table(phrase)

    def search_phrase_in_table(self, phrase):
        self.table.setCurrentItem(None)
        founded = self.table.findItems(phrase, Qt.MatchContains)
        self.found_items = [x for x in founded if x is not None]
        self.current_found_item = -1
        self.key_tab_pressed()

    def key_tab_pressed(self):
        if self.current_found_item is not None and self.found_items:
            self.found_items[self.current_found_item].setSelected(False)

            self.current_found_item += 1
            self.current_found_item %= len(self.found_items)

            self.table.setCurrentItem(self.found_items[self.current_found_item])
            self.found_items[self.current_found_item].setSelected(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        for child in self.childs:
            child.close()

    def my_close(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApplication()
    ex.show()
    sys.exit(app.exec())
