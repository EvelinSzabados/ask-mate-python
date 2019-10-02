from flask import Flask, render_template, request, redirect, url_for
import connection
app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = connection.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id: int):
    questions = connection.get_all_questions()
    answers = connection.get_all_answers()
    actual_question = []
    actual_answers = []
    for line in questions:
        for key, value in line.items():
            if value == question_id:
                actual_question.append(dict(line))
    for answer in answers:
        if answer["question_id"] == question_id:
            actual_answers.append(dict(answer))

    return render_template('question.html', actual_question=actual_question, actual_answers=actual_answers)


@app.route('/new_question')
def route_new_question():
    return render_template('new_question.html')


@app.route('/answer')
def route_answer():
    return render_template('answer.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )