from flask import Flask, render_template, request, redirect, url_for
import connection
app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = connection.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/question')
def route_question():
    questions = connection.get_all_questions()
    return render_template('question.html',questions=questions)


@app.route('/new_question')
def route_new_question():
    return render_template('new_question.html')

@app.route('/answer')
def route_answer():
    return render_template('answer.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=4000,
        debug=True,
    )