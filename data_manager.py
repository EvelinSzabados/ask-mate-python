import connection
import csv
import time
from datetime import datetime

def get_next_id():
    existing_data = connection.get_all_questions()
    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)


def current_submission_time():

    submission_time = int(time.time())
    new_object = str(datetime.fromtimestamp(int(submission_time)))
    return new_object


def get_actual_question(question_id):
    questions = connection.get_all_questions()
    actual_question = []
    for line in questions:
        for key, value in line.items():
            if value == question_id:
                actual_question.append(dict(line))
    return actual_question


def get_actual_answer(question_id):
    answers = connection.get_all_answers()
    actual_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            actual_answers.append(dict(answer))
    return actual_answers
