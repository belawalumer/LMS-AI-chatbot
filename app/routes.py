from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from app import db, login_manager
from app.models import User
import openai

openai.api_key = 'your-openai-api-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_input = request.json.get('message')
        response = openai.Completion.create(
            engine="text-davinci-004",
            prompt=f"User: {user_input}\nBot:",
            max_tokens=150
        )
        return jsonify({"response": response.choices[0].text.strip()})
    return render_template('chat.html')

