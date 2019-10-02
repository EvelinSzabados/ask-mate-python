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


def add_new_question(question, append=True):
    existing_data = get_all_questions()

    with open('question.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        writer.writeheader()

        for row in existing_data:
            if not append:
                if row['id'] == question['id']:
                    row = question

            writer.writerow(row)

        if append:
            writer.writerow(question)
