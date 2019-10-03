import connection
import csv
import time
from datetime import datetime


def convert_questions():
    converted_time = None
    converted_questions = connection.get_all_questions()
    for line in converted_questions:
        for key, value in line.items():
            if key == "submission_time":
                converted_time = datetime.fromtimestamp(int(value))
                line[key] = str(converted_time)
    return converted_questions

def convert_answers():
    converted_time = None
    converted_answers = connection.get_all_answers()
    for line in converted_answers:
        for key, value in line.items():
            if key == "submission_time":
                converted_time = datetime.fromtimestamp(int(value))
                line[key] = str(converted_time)
    return converted_answers

def get_next_id():
    existing_data = connection.get_all_questions()
    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)

def current_submission_time():

    submission_time = int(time.time())

    return submission_time

def get_actual_question(question_id):
    questions = convert_questions()
    actual_question = []
    for line in questions:
        for key, value in line.items():
            if value == question_id:
                actual_question.append(dict(line))
    return actual_question

def get_actual_answer(question_id):
    answers = convert_answers()
    actual_answers = []
    for answer in answers:
        if answer["question_id"] == question_id:
            actual_answers.append(dict(answer))
    return actual_answers


def delete_question(question_id):
    questions = connection.get_all_questions()
    for question in questions:
        if question["id"] == question_id:
            questions.remove(question)
    return questions

def delete_answer(actual_id):
    answers = connection.get_all_answers()
    for answer in answers:
        if answer["id"] == actual_id:
            answers.remove(answer)
    return answers
