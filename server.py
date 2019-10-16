from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager
import csv
from datetime import datetime
app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    limited_questions = data_manager.get_questions_limited()
    return render_template('list.html', limited_questions=limited_questions)


@app.route('/list_all')
def route_all_list():
    questions = data_manager.get_questions_sql()
    return render_template('all_questions.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id):
    actual_question = data_manager.get_actual_question(question_id)
    actual_answers = data_manager.get_actual_answer(question_id)
    referrer = request.headers.get("Referer")
    if referrer == "http://0.0.0.0:7000" or referrer == "http://0.0.0.0:7000/list_all" \
            or referrer !="http://0.0.0.0:7000/question/{}".format(question_id):
        data_manager.view_counter(question_id)

    actual_comment = data_manager.get_actual_comment(question_id)
    return render_template('question.html', actual_question=actual_question, actual_answers=actual_answers,
                           actual_comment=actual_comment)


@app.route('/question/<question_id>/<question_vote>')
def route_question_vote(question_id, question_vote):

    data_manager.question_vote(question_vote, question_id)

    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/<answer_vote>/<answer_id>')
def route_answer_vote(question_id, answer_vote, answer_id):
    data_manager.answer_vote(answer_vote, answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/new_question', methods=['GET', 'POST'])
def route_new_question():
    if request.method == 'POST':

        new_question_data = {
                "submission_time": data_manager.current_submission_time(),
                "view_number": 0,
                "vote_number": 0,
                "title": request.form.get("title"),
                "message": request.form.get("message"),
                "image": ""
            }
        question_id = data_manager.add_new_question(new_question_data)
        return redirect(url_for('route_question', question_id=question_id[0]["id"]))

    return render_template("new_question.html")


@app.route('/answer/<actual_id>', methods=['GET', 'POST'])
def route_answer(actual_id):
    if request.method == 'POST':
        new_answer_data = {
            "submission_time": data_manager.current_submission_time(),
            "vote_number": 0,
            "question_id": int(actual_id),
            "message": request.form.get("answer")
        }
        data_manager.add_new_answer(new_answer_data)

        return redirect(url_for('route_question', question_id=actual_id))

    return render_template('answer.html', form_url=url_for('route_answer', actual_id=actual_id))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def route_delete_question(question_id):
    data_manager.delete_question(question_id)

    return redirect('/')


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def route_delete_answer(answer_id):
    question_id = data_manager.get_actual_question_by_answer_id(answer_id)[0]['question_id']
    data_manager.delete_answer(answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        searched = request.args.get("searched_word")
        search_results = data_manager.search(searched)
        return render_template('search_results.html', search_results=search_results)


@app.route('/answer/<answer_id>/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id: int, question_id: int):

    if request.method == 'POST':
        new_message = request.form.get("message")
        data_manager.edit_answer(new_message, answer_id)

        return redirect(url_for('route_question', question_id=question_id))
    actual_answer = data_manager.get_answer_to_edit(answer_id)
    if len(actual_answer) > 0:
        answer_to_edit = actual_answer[0]["message"]
        return render_template("edit_answer.html", form_url=url_for('route_edit_answer', answer_id=answer_id, question_id=question_id),
                               actual_answer=answer_to_edit, redirect_url=url_for('route_question', question_id=question_id))
    else:
        #todo: handle this
        pass


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )