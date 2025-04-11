from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import random,os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
bcrypt = Bcrypt(app)

# MongoDB setup
client = MongoClient("mongodb+srv://akshatneema01:h2myDpyt4gebfCIR@motivation.lbiliq8.mongodb.net/?retryWrites=true&w=majority&appName=Motivation")
db = client['motivationalApp']
users = db['users']

# Sample quotes
QUOTES = [
    "Believe in yourself and all that you are.",
    "The future depends on what you do today.",
    "Push yourself, because no one else is going to do it for you.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Your limitation—it’s only your imagination.",
    "Dream it. Wish it. Do it.",
    "Sometimes later becomes never. Do it now.",
    "Great things never come from comfort zones.",
    "Hardships often prepare ordinary people for an extraordinary destiny.",
    "Do what you can with all you have, wherever you are."
]

@app.route('/')
def home():
    if 'email' in session:
        return render_template('index.html', email=session['email'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        if users.find_one({'_id': email}):
            return 'User already exists!'
        users.insert_one({'_id': email, 'password': password, 'favorites': []})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users.find_one({'_id': request.form['email']})
        if user and bcrypt.check_password_hash(user['password'], request.form['password']):
            session['email'] = user['_id']
            return redirect(url_for('home'))
        return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/quote')
def get_quote():
    return jsonify({'quote': random.choice(QUOTES)})

@app.route('/favorites', methods=['GET', 'POST'])
def handle_favorites():
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user = users.find_one({'_id': session['email']})
    if request.method == 'POST':
        quote = request.json['quote']
        if quote not in user['favorites']:
            users.update_one({'_id': session['email']}, {'$push': {'favorites': quote}})
    return jsonify({'favorites': user['favorites']})
