import connection
import csv
import time
from datetime import datetime

@connection.connection_handler
def view_counter(cursor, id):
    cursor.execute("UPDATE question SET view_number = view_number + 1 WHERE id= %(id)s",
                   {'id': id})


@connection.connection_handler
def get_questions_sql(cursor):
    cursor.execute("SELECT * FROM question;")
    all_questions = cursor.fetchall()

    return all_questions


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


@connection.connection_handler
def get_actual_answer(cursor, id):
    cursor.execute("SELECT * FROM answer WHERE question_id=%(id)s ORDER BY id;",
                   {'id': id})
    actual_answer = cursor.fetchall()
    return actual_answer


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