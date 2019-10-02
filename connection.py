import csv
from datetime import datetime


def get_all_questions():
    with open('sample_data/question.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        questions = []
        for line in csv_reader:
            dt_object = None
            for key, value in line.items():
                if key == "submission_time":
                    dt_object = str(datetime.fromtimestamp(int(value)))
                    line[key] = dt_object

            questions.append(dict(line))
            questions.sort(key=lambda x: x['submission_time'], reverse=True)

    return questions


def get_all_answers():
    with open('sample_data/answer.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        answers = []
        for line in csv_reader:
            dt_object = None
            for key, value in line.items():
                if key == "submission_time":
                    dt_object = str(datetime.fromtimestamp(int(value)))
                    line[key] = dt_object

            answers.append(dict(line))
            answers.sort(key=lambda x: x['submission_time'], reverse=True)

    return answers

