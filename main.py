import sys
from pprint import pprint
from PyQt5.QtWidgets import QApplication, QWidget
from sources.akinator_database_cursor import SubjectAkinatorDatabaseCursor, Question
from PyQt5 import QtCore, QtGui, QtWidgets

from settings import DB_FILENAME


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

        icon = QtGui.QIcon('resources\\akinator_clear.ico')
        Form.setWindowIcon(icon)

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

    def btn_start_clicked(self):
        self.child = QuestionsWindowWidget(self)
        self.child.show()
        self.close()

    def restart(self):
        self.child.close()
        self.child = None
        self.show()


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
        self.question_label.setWordWrap(True)
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

        icon = QtGui.QIcon('resources\\akinator_clear.ico')
        Form.setWindowIcon(icon)

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
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent

        self.game_is_over = False
        self.predicted_subject = None
        self.subjects_list_is_empty = False

        self.last_questions = []

        self.db_cursor = SubjectAkinatorDatabaseCursor(DB_FILENAME)
        self.current_subjects = [x[0] for x in self.db_cursor.get_all_subjects()]
        self.current_question = self._get_question_with_max_profit()
        self.questions_count = 1

        # print(self.current_question)
        # pprint(self.current_subjects)
        print('[INFO] Loaded subjects:', len(self.current_subjects))

        self.btn_answer_yes.clicked.connect(self.btn_answer_yes_clicked)
        self.btn_answer_no.clicked.connect(self.btn_answer_no_clicked)

        self.update_interface()

    def btn_answer_yes_clicked(self):
        print('-' * 40, '\n', "[INFO] get 'YES' answer")
        if not self.game_is_over:
            self.print_statistics()
            self.current_subjects = list(
                set(self.current_subjects) & set(self.current_question.subjects_ids))
            self.check_list()
            self.set_new_question()
        else:
            self.question_label.setText("Спасибо за игру! Я отгадал :)")
            self.btn_answer_no.hide()
            self.btn_answer_yes.setText('Начать заново')
            self.btn_answer_yes.clicked.connect(self.restart)

    def btn_answer_no_clicked(self):
        print('-' * 40, '\n', "[INFO] get 'NO' answer")
        if not self.game_is_over:
            self.print_statistics()
            self.current_subjects = list(
                set(self.current_subjects) - set(self.current_question.subjects_ids))
            self.check_list()
            self.set_new_question()
        else:
            self.question_label.setText("Грустно...! Я не смог отгадать :(")
            self.btn_answer_no.hide()
            self.btn_answer_yes.setText('Начать заново')
            self.btn_answer_yes.clicked.connect(self.restart)

    def set_new_question(self):
        self.last_questions.append(self.current_question.question_id)
        self.last_questions = list(set(self.last_questions))

        if self.check_predict():
            self.game_is_over = True
            self.predicted_subject = self.db_cursor.get_subject(self.current_subjects[0])

        current_probably_answer_count = len(self.current_subjects)
        print("Current probably subjects count:", current_probably_answer_count)

        self.current_question = self._get_question_with_max_profit()
        self.questions_count += 1
        self.update_interface()

    def update_interface(self):
        if self.subjects_list_is_empty:
            self.empty_list_event()
            return
        if not self.game_is_over:
            self.current_question: Question
            self.question_label.setText(self.current_question.question_text)
            self.question_number_label.setText(f"{self.questions_count}/10")
        else:
            self.question_label.setText(f"Это '{self.predicted_subject[1]}'?")

    def _get_question_with_max_profit(self):
        current_subjects_count = len(self.current_subjects)

        res = self.db_cursor.get_question_with_max_separate(self.current_subjects,
                                                            self.last_questions)

        # pprint(res)

        res = [(x[0], x[1],
                len(set(self.current_subjects) - set(self.db_cursor.get_question(x[0])[0][2]))) for x
               in res]
        res = sorted(res, key=lambda x: (x[2] - current_subjects_count // 2) ** 2)
        # pprint(res)

        question = self.db_cursor.get_question(res[0][0])[0]
        temp = Question()
        temp.question_text = question[1]
        temp.question_id = question[0]
        temp.subjects_ids = question[2]
        return temp

    def print_statistics(self):
        and_list = list(set(self.current_subjects) & set(self.current_question.subjects_ids))
        sub_list = list(set(self.current_subjects) - set(self.current_question.subjects_ids))

        print("question #", self.questions_count, "\n",
              "state 'game_is_over':", self.game_is_over, "\n",
              "last questions:", self.last_questions, "\n"
                                                      "current subjects:",
              len(self.current_subjects), self.current_subjects, "\n",
              "question subjects:", len(self.current_question.subjects_ids),
              self.current_question.subjects_ids, "\n",
              "AND:", len(and_list), and_list, "\n",
              "SUB:", len(sub_list), sub_list
              )

    def check_predict(self):
        if len(self.current_subjects) == 1:
            return True
        elif len(self.current_subjects) == 2:
            if self.db_cursor.get_subject(self.current_subjects[0])[1] == \
                    self.db_cursor.get_subject(self.current_subjects[1])[1]:
                return True
        return False

    def check_list(self):
        self.subjects_list_is_empty = not bool(self.current_subjects)

    def restart(self):
        self.parent.restart()

    def empty_list_event(self):
        self.question_label.setText("Увы, но я не знаю такого предмета.. Может сыграем еще разок?")
        self.btn_answer_no.clicked.connect(self.close)
        self.btn_answer_yes.clicked.connect(self.restart)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindowWidget()
    ex.show()
    sys.exit(app.exec())
