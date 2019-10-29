import connection
import csv
import time
from datetime import datetime


@connection.connection_handler
def view_counter(cursor, id):
    cursor.execute("UPDATE question SET view_number = view_number + 1 WHERE id= %(id)s",
                   {'id': id})


@connection.connection_handler
def get_questions_sql(cursor, order):
    if order == "submission_time":
        cursor.execute("SELECT * FROM question ORDER BY submission_time DESC;")
        all_questions = cursor.fetchall()
    if order == "title":
        cursor.execute("SELECT * FROM question ORDER BY title;")
        all_questions = cursor.fetchall()
    if order == "message":
        cursor.execute("SELECT * FROM question ORDER BY message;")
        all_questions = cursor.fetchall()
    if order == "vote_number":
        cursor.execute("SELECT * FROM question ORDER BY vote_number DESC;")
        all_questions = cursor.fetchall()
    if order == "view_number":
        cursor.execute("SELECT * FROM question ORDER BY view_number DESC;")
        all_questions = cursor.fetchall()

    return all_questions


@connection.connection_handler
def get_questions_titled(cursor):
    cursor.execute("SELECT * FROM question ORDER BY title;")
    all_questions = cursor.fetchall()

    return all_questions


@connection.connection_handler
def get_questions_limited(cursor):
    cursor.execute("SELECT * FROM question ORDER BY submission_time DESC LIMIT 5;")
    limited_questions = cursor.fetchall()

    return limited_questions


@connection.connection_handler
def add_new_question(cursor, new_data):
    cursor.execute(
        "INSERT INTO question VALUES (DEFAULT, %(submission_time)s,%(view_number)s,"
        "%(vote_number)s, %(title)s ,%(message)s,NULL) RETURNING id;",
        {'submission_time': new_data["submission_time"],
         'view_number': new_data["view_number"],
         'vote_number': new_data["vote_number"],
         'title': new_data["title"],
         'message': new_data["message"]})
    question_id = cursor.fetchall()
    return question_id


@connection.connection_handler
def add_new_answer(cursor, new_data):
    cursor.execute("INSERT INTO answer VALUES (DEFAULT, %(submission_time)s,"
                   "%(vote_number)s,%(question_id)s,%(message)s, NULL) RETURNING id;",
                   {'submission_time': new_data["submission_time"],
                    'question_id': new_data["question_id"],
                    'vote_number': new_data["vote_number"],
                    'message': new_data["message"]})


@connection.connection_handler
def add_new_comment(cursor, new_data):
    cursor.execute("INSERT INTO comment VALUES (DEFAULT, %(question_id)s,"
                   "%(answer_id)s,%(message)s,%(submission_time)s, NULL) RETURNING id;",
                   {'question_id': new_data["question_id"],
                    'answer_id': new_data["answer_id"],
                    'message': new_data["message"],
                    'submission_time': new_data["submission_time"]})


def current_submission_time():
    submission_time = int(time.time())
    converted_time = datetime.fromtimestamp(int(submission_time))
    timestamp = str(converted_time)
    return timestamp


@connection.connection_handler
def get_actual_question(cursor, id):
    cursor.execute("SELECT * FROM question WHERE id=%(id)s ORDER BY id;",
                   {'id': id})
    actual_question = cursor.fetchall()
    return actual_question


@connection.connection_handlerquestion_id
def get_actual_answer(cursor, id):
    cursor.execute("SELECT * FROM answer WHERE question_id=%(id)s ORDER BY id;",
                   {'id': id})
    actual_answer = cursor.fetchall()
    return actual_answer


@connection.connection_handler
def get_answer_to_edit(cursor,id):
    cursor.execute("SELECT message FROM answer WHERE id= %(id)s", {'id': id})
    answer_to_edit = cursor.fetchall()

    return answer_to_edit


@connection.connection_handler
def get_question_to_edit(cursor,id):
    cursor.execute("SELECT title, message FROM question WHERE id= %(id)s", {'id': id})
    question_to_edit = cursor.fetchall()
    print(question_to_edit)

    return question_to_edit


@connection.connection_handler
def get_answer_to_comment(cursor,id):
    cursor.execute("SELECT id FROM answer WHERE id= %(id)s", {'id': id})
    answer_to_comment = cursor.fetchall()

    return answer_to_comment


@connection.connection_handler
def get_actual_comment(cursor, id):
    cursor.execute("SELECT * FROM comment WHERE id=%(id)s ORDER BY id;",
                   {'id': id})
    actual_comment = cursor.fetchall()
    return actual_comment


@connection.connection_handler
def get_actual_comment(cursor, id):
    cursor.execute("SELECT * FROM comment WHERE question_id=%(id)s ORDER BY id;",
                   {'id': id})
    actual_comment = cursor.fetchall()
    return actual_comment


@connection.connection_handler
def get_actual_question_by_answer_id(cursor, answer_id):
    cursor.execute("SELECT question_id FROM answer WHERE answer.id=%(answer_id)s;",
                   {'answer_id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_question(cursor, id):

    cursor.execute("SELECT id FROM answer WHERE question_id=%(id)s", {'id': id})
    answer_id = cursor.fetchall()
    if answer_id:
        cursor.execute("DELETE FROM comment WHERE question_id=%(id)s", {'id': id})
        cursor.execute("DELETE FROM comment WHERE answer_id=%(id)s", {'id': answer_id[0]["id"]})
        cursor.execute("DELETE FROM answer WHERE question_id=%(id)s", {'id': id})
        cursor.execute("DELETE FROM question_tag WHERE question_id=%(id)s", {'id': id})
    cursor.execute("DELETE FROM question WHERE id=%(id)s", {'id': id})


@connection.connection_handler
def delete_answer(cursor, id):
    cursor.execute("DELETE FROM comment WHERE answer_id=%(id)s", {'id': id})
    cursor.execute("DELETE FROM answer WHERE id=%(id)s", {'id': id})


@connection.connection_handler
def question_vote(cursor, vote, id):
    if vote == "up":
        cursor.execute("UPDATE question SET vote_number = vote_number + 1 WHERE id=%(id)s",
                        {'id': id})
    else:
        cursor.execute("UPDATE question SET vote_number = vote_number - 1 WHERE id=%(id)s",
                        {'id': id})


@connection.connection_handler
def answer_vote(cursor, vote, id):
    if vote == "up":
        cursor.execute("UPDATE answer SET vote_number = vote_number + 1 WHERE id=%(id)s",
                        {'id': id})
    else:
        cursor.execute("UPDATE answer SET vote_number = vote_number - 1 WHERE id=%(id)s",
                        {'id': id})


@connection.connection_handler
def search_question(cursor,searched):
    cursor.execute("SELECT title, id FROM question WHERE LOWER(title) like %(searched)s "
                   "or LOWER(message) like %(searched)s",
                   {'searched': '%{}%'.format(searched)})
    search_results = cursor.fetchall()

    return search_results


@connection.connection_handler
def search_answer(cursor,searched):
    cursor.execute("SELECT message, question_id FROM answer WHERE LOWER(message) like %(searched)s ",
                   {'searched': '%{}%'.format(searched)})

    search_results = cursor.fetchall()

    def get_question_by_answer(cursor):
        new_list = []
        for line in search_results:
            cursor.execute("SELECT title, id FROM question WHERE id =%(question_id)s",
                       {'question_id': line['question_id']})
            question_by_answer = cursor.fetchone()
            new_list.append(question_by_answer)
        return new_list

    question_from_answer = get_question_by_answer(cursor)
    return question_from_answer


@connection.connection_handler
def edit_answer(cursor, new_message, id):
    cursor.execute("UPDATE answer SET message = %(new_message)s WHERE id=%(id)s", {'id': id, 'new_message': new_message})


@connection.connection_handler
def edit_question(cursor, id, new_title, new_message):
    cursor.execute("UPDATE question SET title = %(new_title)s, message = %(new_message)s"
                   "WHERE id=%(id)s", {'id': id, 'new_title': new_title, 'new_message': new_message})


@connection.connection_handler
def delete_comment(cursor, id):

    cursor.execute("DELETE FROM comment WHERE id=%(id)s", {'id': id})


@connection.connection_handler
def get_question_id_by_comment_id(cursor, id):
    cursor.execute("SELECT question_id FROM comment WHERE id= %(id)s", {'id': id})
    question_id = cursor.fetchall()

    return question_id

@connection.connection_handler
def create_user(cursor, new_data):
    cursor.execute(
        "INSERT INTO users VALUES (DEFAULT, %(register_date)s,"
        "%(username)s, %(password)s) RETURNING id;",
        {'register_date': new_data["register_date"],
         'username': new_data["username"],
         'password': new_data["password"]})
    user_id = cursor.fetchall()
    return user_id
