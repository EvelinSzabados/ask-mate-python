import psycopg2
import psycopg2.extras
from datetime import datetime
import os

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()

        return ret_value

    return wrapper

# def get_all_questions():
#     with open('sample_data/question.csv') as csv_file:
#         csv_reader = csv.DictReader(csv_file, delimiter=',')
#         questions = []
#         for line in csv_reader:
#             questions.append(dict(line))
#
#     return questions
#
#
# def get_all_answers():
#     with open('sample_data/answer.csv') as csv_file:
#         csv_reader = csv.DictReader(csv_file, delimiter=',')
#         answers = []
#         for line in csv_reader:
#             answers.append(dict(line))
#
#     return answers
#
#
# def add_new_answer(answers):
#     with open("sample_data/answer.csv", mode="w") as data_file:
#         fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message']
#         data_writer = csv.DictWriter(data_file, delimiter=',', fieldnames=fieldnames)
#         data_writer.writeheader()
#
#         for data in answers:
#             data_writer.writerow(data)
#
# def add_new_question(questions):
#
#     with open("sample_data/question.csv", mode="w") as data_file:
#         fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
#         data_writer = csv.DictWriter(data_file, delimiter=',', fieldnames=fieldnames)
#         data_writer.writeheader()
#
#         for data in questions:
#             data_writer.writerow(data)