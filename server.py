from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager
import csv
from datetime import datetime
app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.convert_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id: int):
    actual_question = data_manager.get_actual_question(question_id)
    actual_answers = data_manager.get_actual_answer(question_id)

    return render_template('question.html', actual_question=actual_question, actual_answers=actual_answers)


@app.route('/question/<question_id>/<question_vote>')
def route_question_vote(question_id, question_vote):
    questions = connection.get_all_questions()

    for line in questions:
        if line["id"] == question_id:
            if question_vote == "up":
                line["vote_number"] = int(line["vote_number"])+1

            if question_vote == "down" and int(line["vote_number"]):
                line["vote_number"] = int(line["vote_number"])-1

    connection.add_new_question(questions)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/new_question', methods=['GET', 'POST'])
def route_new_question():
        if request.method == 'POST':
            questions = connection.get_all_questions()

            id_list = []
            for i in questions:
                for key, value in i.items():
                    if key == "id":
                        id_list.append(int(value))
            new_id = max(id_list) + 1

            new_question_data = {
                "submission_time": data_manager.current_submission_time(),
                "view_number": 0,
                "vote_number": 0,
                "title": request.form.get("title"),
                "message": request.form.get("message"),
                "image": "",
                "id": new_id
            }
            questions.append(new_question_data)
            connection.add_new_question(questions)

            return redirect(url_for('route_question', question_id=new_id))

        return render_template("new_question.html")


@app.route('/answer/<actual_id>', methods=['GET', 'POST'])
def route_answer(actual_id):
    if request.method == 'POST':
        answers = connection.get_all_answers()
        id_list = []
        for i in answers:
            for key, value in i.items():
                if key == "id":
                    id_list.append(int(value))
        new_id = max(id_list) + 1

        new_answer_data = {
            "submission_time": data_manager.current_submission_time(),
            "vote_number": 0,
            "question_id": int(actual_id),
            "message": request.form.get("answer"),
            "id": new_id
        }

        answers.append(new_answer_data)
        connection.add_new_answer(answers)

        return redirect(url_for('route_question', question_id=actual_id))

    return render_template('answer.html', form_url=url_for('route_answer', actual_id=actual_id))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def route_delete_question(question_id):
    questions = data_manager.delete_question(question_id)
    connection.add_new_question(questions)

    return redirect('/')

@app.route('/answer/<actual_id>/<question_id>/delete', methods=['GET', 'POST'])
def route_delete_answer(actual_id, question_id):
    answers = data_manager.delete_answer(actual_id)
    connection.add_new_answer(answers)

    return redirect(url_for('route_question', question_id=question_id))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )