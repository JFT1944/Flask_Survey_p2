from flask import Flask, render_template, request, session, redirect, flash
from surveys import personality_quiz, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Big Time Secret'

# responses = []
questions_answered = 0

@app.route('/')
def index():
    quiz_type = satisfaction_survey.title
    quiz_inst = satisfaction_survey.instructions
    print(session['responses'])
    return render_template('Homepage.html', quiz_type=quiz_type, quiz_inst=quiz_inst)

@app.route('/', methods=['POST'])
def clearingsesh():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions')
def qs():
    return 'Question page'

@app.route('/questions/<qnum>')
def show_question(qnum):
    num = int(qnum)
    quiz_qs = satisfaction_survey.questions[num].question
    quiz_answ = satisfaction_survey.questions[num].choices
    print(len(session['responses']))
    
    

    next_num = int(qnum) + 1
    return render_template('questions.html', quiz_qs=quiz_qs, quiz_answ=quiz_answ, next_num=next_num, num=num)

@app.route('/questions/<qnum>', methods=['POST'])
def posting_questions(qnum):
    num = int(qnum)
    answer = request.form[f'q{num}']
    print(answer)
    # -------
    correct_page_num = len(session['responses'])
    if num != len(session['responses']):
        print(num)
        print(len(session['responses']))
        flash("Oops! You missed a question. You've been directed back")
        return redirect(f'/questions/{correct_page_num}')
    # append session here
    newresponses = session['responses']
    newresponses.append(answer)
    session['responses'] = newresponses
    print(session['responses'])
    # -------
    # responses.append(answer)
    # print(responses)
    
    
    # # quiz_qs = satisfaction_survey.questions[num].question
    # # quiz_answ = satisfaction_survey.questions[num].choices
    next_num = int(qnum) + 1
    question_length = len(satisfaction_survey.questions)
    if next_num == question_length:
        return redirect('/thankyou')
    return redirect(f'/questions/{next_num}')

@app.route('/thankyou')
def thankyou():
    return '<h2>Thank you for completing this Survey</h2>'