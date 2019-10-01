import csv


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

