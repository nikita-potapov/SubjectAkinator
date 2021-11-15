import sqlite3


class Subject:
    subject_id = None
    subject_name = None
    subject_course = None
    subject_way_of_study = None


class Question:
    question_id = None
    question_text = None
    subjects_ids = []

    def __str__(self):
        return f"<Question> id:[{self.question_id}] " \
               f"text:\"{self.question_text}\" " \
               f"ids:[{', '.join([str(x) for x in self.subjects_ids])}]"


class SubjectAkinatorDatabaseCursor:
    def __init__(self, db_filename):
        self.db_filename = db_filename

        self.db_connection = sqlite3.connect(db_filename)
        try:
            self.db_connection.cursor()
            self.is_exist = False
        except Exception:
            self.db_connection = None
            self.is_exist = True

    def get_question(self, question_id):
        cursor = self.db_connection.cursor()
        query = f"""SELECT id, text
                        FROM questions
                        WHERE id = {question_id}"""

        result = cursor.execute(query).fetchall()

        if not result:
            return None

        query = f"""SELECT subject_id FROM question_to_subjects
                        WHERE question_id = {question_id}"""

        sub_result = cursor.execute(query).fetchall()

        sub_result = [x[0] for x in sub_result]

        for i in range(len(result)):
            result[i] = (*result[i], sub_result)
        return result

    def get_all_questions(self):
        cursor = self.db_connection.cursor()
        query = """SELECT questions.id, questions.text
         FROM questions ORDER BY questions.id"""

        result = cursor.execute(query).fetchall()

        if not result:
            return None

        return result

    def add_question(self, question):
        cursor = self.db_connection.cursor()
        query = f"""INSERT INTO questions (text) VALUES (\'{question.question_text}\')"""
        cursor.execute(query)
        self.db_connection.commit()

        query = """SELECT id FROM questions ORDER BY id DESC"""
        result = cursor.execute(query).fetchone()

        last_question_id = result[0]
        for i in range(len(question.subjects_ids)):
            query = f"""INSERT INTO question_to_subjects (question_id, subject_id)
                            VALUES ({last_question_id}, {question.subjects_ids[i]})"""
            cursor.execute(query)
        self.db_connection.commit()

    def edit_question(self, question):
        cursor = self.db_connection.cursor()

        query = f"""UPDATE questions
                    SET text = '{question.question_text}'
                     WHERE id = {question.question_id}"""
        cursor.execute(query)

        query = f"""DELETE FROM question_to_subjects WHERE question_id = {question.question_id}"""
        cursor.execute(query)

        subjects_ids = question.subjects_ids
        for subject_id in subjects_ids:
            query = f"""INSERT INTO question_to_subjects (question_id, subject_id)
             VALUES ({question.question_id}, {subject_id})"""
            cursor.execute(query)

        self.db_connection.commit()

    def delete_question(self, question_id):
        cursor = self.db_connection.cursor()
        query = f"""DELETE FROM questions WHERE id = {question_id}"""
        cursor.execute(query)

        query = f"""DELETE FROM question_to_subjects WHERE question_id = {question_id}"""
        cursor.execute(query)

        self.db_connection.commit()

    def add_subject(self, subject):
        query = f"""SELECT way_of_study.id FROM way_of_study
                                WHERE way_of_study.name = '{subject.subject_way_of_study}'"""

        cursor = self.db_connection.cursor()
        way_of_study_id = cursor.execute(query).fetchone()[0]

        subject: Subject
        query = f"""INSERT INTO subjects
                    (name, way_of_study, course)
                    VALUES ('{subject.subject_name}', {way_of_study_id}, {subject.subject_course})"""
        cursor.execute(query)

        self.db_connection.commit()

    def get_subject(self, subject_id):
        cursor = self.db_connection.cursor()
        query = f"""SELECT subjects.id, subjects.name, subjects.course,
         way_of_study.name FROM subjects LEFT JOIN way_of_study 
         ON subjects.way_of_study = way_of_study.id WHERE subjects.id = {subject_id}"""

        result = cursor.execute(query).fetchone()

        if not result:
            return None

        return result

    def edit_subject(self, subject):
        query = f"""SELECT way_of_study.id FROM way_of_study
                        WHERE way_of_study.name = '{subject.subject_way_of_study}'"""

        cursor = self.db_connection.cursor()
        way_of_study_id = cursor.execute(query).fetchone()[0]

        query = f"""UPDATE subjects SET name = '{subject.subject_name}',
                                        way_of_study = {way_of_study_id},
                                        course = {subject.subject_course}
                    WHERE id = {subject.subject_id}"""
        cursor.execute(query)

        self.db_connection.commit()

    def delete_subject(self, subject_id):
        cursor = self.db_connection.cursor()
        query = f"""DELETE FROM subjects WHERE id = {subject_id}"""
        cursor.execute(query)

        query = f"""DELETE FROM question_to_subjects WHERE subject_id = {subject_id}"""
        cursor.execute(query)

        self.db_connection.commit()

    def get_all_subjects(self):
        cursor = self.db_connection.cursor()
        query = """SELECT subjects.id, subjects.name, way_of_study.name
                    FROM subjects LEFT JOIN way_of_study
                     ON subjects.way_of_study = way_of_study.id ORDER BY subjects.id"""

        result = cursor.execute(query).fetchall()

        if not result:
            return None

        return result

    def get_all_ways_of_study(self):
        cursor = self.db_connection.cursor()
        query = """SELECT way_of_study.id, way_of_study.name
                 FROM way_of_study ORDER BY way_of_study.id"""

        result = cursor.execute(query).fetchall()

        if not result:
            return None

        return result

    def get_question_with_max_separate(self, current_subjects, last_questions):
        query = f"""
            SELECT *,
       (
           SELECT COUNT( * ) 
             FROM question_to_subjects
            WHERE question_to_subjects.question_id = questions.id AND 
                  subject_id IN ({', '.join([str(x) for x in current_subjects])})
        )
        AS CUTOFF_COUNT
        FROM questions
        WHERE questions.id NOT IN ({', '.join([str(x) for x in last_questions])})
        ORDER BY CUTOFF_COUNT DESC;
        """
        cursor = self.db_connection.cursor()
        result = cursor.execute(query).fetchall()

        return result
