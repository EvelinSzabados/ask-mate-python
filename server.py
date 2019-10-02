from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager
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


@app.route('/new_question', methods=['GET', 'POST'])
def route_new_question():
    new_id = data_manager.get_next_id()
    if request.method == 'POST':
        new_question = {
            'id': new_id,
            'submission_time': data_manager.current_submission_time(),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': None
        }

        connection.add_new_question(new_question)
        return redirect('/')

    return render_template('question.html', question_id=new_id)



@app.route('/answer')
def route_answer():
    return render_template('answer.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )