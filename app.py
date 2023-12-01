from flask import Flask, render_template, request, redirect, flash, session, make_response
from surveys import satisfaction_survey, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Do not tell anyone'
app.jinja_env.globals.update(zip=zip)

@app.route('/')
def home():
    """
    Go to home page displaying a selection of surveys
    @return: Response
    """

    session['survey_names'] = [name for name in surveys.keys()]

    return render_template('home.html')


@app.route('/intro')
def show_intro():
    """
    Intro to the selected survey including survey title and instructions
    @return: Response
    """
    session['selected_survey'] = request.args['selected-survey']
    survey = surveys.get(session['selected_survey'])

    return render_template('intro.html',
                           title=survey.title,
                           instructions=survey.instructions)

@app.route('/start')
def start_survey():
    """
    Initialize a survey
    @return:
    """
    # Clear previous survey answers
    session['responses'] = []
    survey = surveys.get(session['selected_survey'])
    if request.cookies.get(survey.title):
        flash('Whoops! Looks like you already completed this survey!')
        return redirect('/')

    return redirect('/questions/0')

@app.route('/questions/<int:question_id>')
def display_question(question_id):
    """
    Display a question and possible answers
    @param question_id: int, question number
    @return: Response
    """

    try:
        # Check if the question is actually the next question
        if question_id != len(session['responses']):
            flash(f"Hey! Don't mess with the order of the questions!")
            return redirect(f"/questions/{len(session['responses'])}")
    except KeyError:
        # The user tried to access a question directly before the starting the survey
        session['responses'] = []
        return redirect("/")

    # Select the survey object
    survey = surveys.get(session['selected_survey'])

    # Select the actual question
    selected_question = survey.questions[question_id]

    return render_template('question.html', title=satisfaction_survey.title,
                           question= selected_question.question, answers=selected_question.choices,
                           allow_text=selected_question.allow_text)


@app.route('/answer', methods=['POST'])
def record_answer():
    survey = surveys.get(session['selected_survey'])
    responses = session['responses']
    responses.append({'choice': request.form['answer'], 'text': request.form.get('answer-text', '')})
    session['responses'] = responses
    print('*' * 20)
    print(session['responses'])
    print('*' * 20)
    if len(session['responses']) < len(survey.questions):
        return redirect(f"/questions/{len(session['responses'])}")
    else:
        return redirect(f'/thank-you')


@app.route('/thank-you')
def thank_you():
    survey = surveys.get(session['selected_survey'])
    questions = [q.question for q in survey.questions]
    response = make_response(render_template('thank-you.html',
                                             questions=questions,
                                             answers=session['responses'],
                                             title=survey.title))
    response.set_cookie(survey.title, 'completed')

    return response

