from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager
import csv
from datetime import datetime
app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = connection.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id: int):
    actual_question = data_manager.get_actual_question(question_id)
    actual_answers = data_manager.get_actual_answer(question_id)

    return render_template('question.html', actual_question=actual_question, actual_answers=actual_answers)


@app.route('/new_question', methods=['GET', 'POST'])
def route_new_question():
    if request.method == 'POST':
        questions = connection.get_all_questions()
        new_data = {}
        id_list = []
        for i in questions:
            for key, value in i.items():
                if key == "id":
                    id_list.append(value)
        new_id = max(id_list)

        new_data["submission_time"] = "20191111"
        new_data["view_number"] = 0
        new_data["vote_number"] = 0
        new_data["title"] = request.form.get("title")
        new_data["message"] = request.form.get("message")
        new_data["image"] = ""
        new_data["id"] = str(int(new_id) + 1)
        new_id= str(int(new_id) + 1)
        questions.append(new_data)

        with open("sample_data/question.csv", mode="w") as data_file:
            fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
            data_writer = csv.DictWriter(data_file, delimiter=',', fieldnames=fieldnames)
            data_writer.writeheader()

            for data in questions:
                data_writer.writerow(data)

        actual_question = data_manager.get_actual_question(new_id)
        actual_answers = data_manager.get_actual_answer(new_id)

        return render_template('question.html', actual_question=actual_question, actual_answers=actual_answers)

    return render_template("new_question.html")




@app.route('/answer')
def route_answer():
    return render_template('answer.html')



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )