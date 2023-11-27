from flask import Flask, render_template, request
from surveys import satisfaction_survey

responses = []

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html',
                           title=satisfaction_survey.title,
                           instructions=satisfaction_survey.instructions)
