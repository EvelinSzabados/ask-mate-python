import connection
import csv
import time
from datetime import datetime


@connection.connection_handler
def get_questions_sql(cursor):
    cursor.execute("SELECT * FROM question;")
    all_questions = cursor.fetchall()

    return all_questions


@connection.connection_handler
def add_new_question(cursor, new_data):
    cursor.execute(
        "INSERT INTO question VALUES (DEFAULT, %(submission_time)s,%(view_number)s,%(vote_number)s, %(title)s ,%(message)s,NULL) RETURNING id;",
        {'submission_time': new_data["submission_time"],
         'view_number': new_data["view_number"],
         'vote_number': new_data["vote_number"],
         'title': new_data["title"],
         'message': new_data["message"]})
    question_id = cursor.fetchall()
    return question_id


# def convert_questions():
#
#     converted_questions = connection.get_all_questions()
#     for line in converted_questions:
#         for key, value in line.items():
#             if key == "submission_time":
#                 converted_time = datetime.fromtimestamp(int(value))
#                 line[key] = str(converted_time)
#     converted_questions.sort(key=lambda x: x['submission_time'], reverse=True)
#     return converted_questions
#
#
# def convert_answers():
#
#     converted_answers = connection.get_all_answers()
#     for line in converted_answers:
#         for key, value in line.items():
#             if key == "submission_time":
#                 converted_time = datetime.fromtimestamp(int(value))
#                 line[key] = str(converted_time)
#     converted_answers.sort(key=lambda x: x['submission_time'], reverse=True)
#     return converted_answers
#
# def get_next_id():
#     existing_data = connection.get_all_questions()
#     if len(existing_data) == 0:
#         return '1'
#
#     return str(int(existing_data[-1]['id']) + 1)


def current_submission_time():
    submission_time = int(time.time())
    converted_time = datetime.fromtimestamp(int(submission_time))
    timestamp = str(converted_time)
    return timestamp


@connection.connection_handler
def get_actual_question(cursor, id):
    cursor.execute("SELECT * FROM question WHERE id=%(id)s;",
                   {'id': id})
    actual_question = cursor.fetchall()
    return actual_question


#     questions = convert_questions()
#     actual_question = []
#     for line in questions:
#         if line["id"] == question_id:
#             actual_question.append(dict(line))
#     return actual_question
#
@connection.connection_handler
def get_actual_answer(cursor, id):
    cursor.execute("SELECT * FROM answer WHERE id=%(id)s;",
                   {'id': id})
    actual_answer = cursor.fetchall()
    return actual_answer
#     answers = convert_answers()
#     actual_answers = []
#     for answer in answers:
#         if answer["question_id"] == question_id:
#             actual_answers.append(dict(answer))
#     return actual_answers
#
#
# def delete_question(question_id):
#     questions = connection.get_all_questions()
#     for question in questions:
#         if question["id"] == question_id:
#             questions.remove(question)
#
#     return questions
#
#
# def delete_answer(actual_id):
#     answers = connection.get_all_answers()
#     for answer in answers:
#         if answer["id"] == actual_id:
#             answers.remove(answer)
#     return answers
