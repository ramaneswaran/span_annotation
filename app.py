import os
import numpy as np
import pandas as pd 
import json
import pickle


from flask import Flask
from flask import render_template
from flask import jsonify , request
from flask import session , redirect
from flask_cors import CORS, cross_origin
from flask import send_file

app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret'    


@app.route('/')
def home():
    return redirect('/tag/')

@app.route('/tag/')
def tag():

    if 'idx' not in session:
        f = open('session.txt', 'r')
        idx = f.read()
        f.close()
        session['idx'] = int(idx)


    if session['idx'] < 0: session['idx'] = 0

    if session['idx'] >= df.shape[0]: session['idx'] = df.shape[0]-1

    
    tweet_text = df.iloc[session['idx']]['text']

    current_count = f'{session["idx"]} of {df.shape[0]-1}'
    
    status = df.iloc[session['idx']]['status']

    label = df.iloc[session['idx']]['sentiment']
    

    return render_template('tag.html', tweet_text = tweet_text, count=current_count, status=status, label=label)

@app.route('/api/meta')
@cross_origin()
def get_meta():

    stimulus_text = df.iloc[session['idx']]['substring']

    payload = {
        'stimulus_text': stimulus_text,
    }

    return jsonify(payload)



@app.route('/form/save', methods =["GET", "POST"])
def get_form():
    form_data = request.form.to_dict()

    stimulus_text = form_data['stimulus']

    df.loc[int(session['idx']), 'substring'] = stimulus_text

    df.to_csv('backup.csv', index=None)

    return redirect('/api/update')

@app.route('/api/update/', methods=["GET"])
def update():
    
    df.loc[int(session['idx']), 'status'] = 'updated'
    df.to_csv(app.config['data_path'], index=None)
    session['idx'] += 1

    if session['idx'] % 50 == 0:
        f = open('session.txt', 'w')
        f.write(str(session['idx']))
        f.close()

    return redirect('/tag/')


@app.route('/back/', methods=["GET"])
def back():
    session['idx'] -=1
    return redirect('/tag/')

@app.route('/forward/', methods=["GET"])
def forward():
    session['idx'] += 1
    return redirect('/tag/')

    
if __name__ == '__main__':

    
    app.config['data_path'] = 'sentimix_sample.csv'
    

    df = pd.read_csv(app.config['data_path'])

    if 'substring' not in df.columns:
        df['substring'] = None
    
    if 'status' not in df.columns:
        df['status'] = np.nan

    
    app.run(debug=True)
