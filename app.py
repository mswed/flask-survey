from flask import Flask, render_template, request, redirect, flash
from surveys import satisfaction_survey

responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Do not tell anyone'


@app.route('/')
def home():
    return render_template('home.html',
                           title=satisfaction_survey.title,
                           instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:question_id>')
def display_question(question_id):
    # Check if the question is actually the next question
    if question_id != len(responses):

        flash("Hey! Don't mess with the order of the questions!")
        return redirect(f'/questions/{len(responses)}')

    # Select the actual question
    selected_question = satisfaction_survey.questions[question_id]
    question = selected_question.question
    answers = selected_question.choices

    return render_template('question.html', title=satisfaction_survey.title,
                           question=question, answers=answers)


@app.route('/answer', methods=['POST'])
def record_answer():
    responses.append(request.form['answer'])
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect(f'/thank-you')


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

