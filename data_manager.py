import connection
import csv
import time


def get_next_id():
    existing_data = connection.get_all_questions()
    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)


def current_submission_time():
    submission_time = int(time.time())
    return submission_time


