import csv
from datetime import datetime
import os

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions():
    with open('sample_data/question.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        questions = []
        for line in csv_reader:
            questions.append(dict(line))

    return questions


def get_all_answers():
    with open('sample_data/answer.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        answers = []
        for line in csv_reader:
            answers.append(dict(line))

    return answers


def add_new_answer(answers):
    with open("sample_data/answer.csv", mode="w") as data_file:
        fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message']
        data_writer = csv.DictWriter(data_file, delimiter=',', fieldnames=fieldnames)
        data_writer.writeheader()

        for data in answers:
            data_writer.writerow(data)

def add_new_question(questions):

    with open("sample_data/question.csv", mode="w") as data_file:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        data_writer = csv.DictWriter(data_file, delimiter=',', fieldnames=fieldnames)
        data_writer.writeheader()

        for data in questions:
            data_writer.writerow(data)
