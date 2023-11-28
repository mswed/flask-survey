from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey

responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Do not tell anyone'


@app.route('/')
def home():
    return render_template('home.html',
                           title=satisfaction_survey.title,
                           instructions=satisfaction_survey.instructions)


@app.route('/start')
def start_survey():
    session['responses'] = []
    print('redirecting to first question ')
    return redirect('/questions/0')
@app.route('/questions/<int:question_id>')
def display_question(question_id):
    print('SESSION IS', session)
    # Check if the question is actually the next question
    if question_id != len(session['responses']):
        flash(f"Hey! Don't mess with the order of the questions! {question_id} {len(session['responses'])}")
        return redirect(f"/questions/{len(session['responses'])}")

    # Select the actual question
    selected_question = satisfaction_survey.questions[question_id]
    question = selected_question.question
    answers = selected_question.choices

    return render_template('question.html', title=satisfaction_survey.title,
                           question=question, answers=answers)


@app.route('/answer', methods=['POST'])
def record_answer():
    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses
    print('session is now', session['responses'])
    if len(session['responses']) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(session['responses'])}")
    else:
        return redirect(f'/thank-you')


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

