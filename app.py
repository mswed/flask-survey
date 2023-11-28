from flask import Flask, render_template, request, redirect
from surveys import satisfaction_survey

responses = []

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html',
                           title=satisfaction_survey.title,
                           instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:question_id>')
def display_question(question_id):
    selected_question = satisfaction_survey.questions[question_id]
    question = selected_question.question
    answers = selected_question.choices

    return render_template('question.html', title=satisfaction_survey.title,
                           question=question, answers=answers)

@app.route('/answer', methods=['POST'])
def record_answer():
    responses.append(request.form['answer'])

    return redirect(f'/questions/{len(responses)}')
