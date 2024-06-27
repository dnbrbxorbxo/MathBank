import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

# 디버깅을 위한 로그 설정
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        app.logger.debug(f"Received username: {username}")
        app.logger.debug(f"Received password: {password}")

        try:
            user = User.get(User.username == username)
            app.logger.debug(f"User found: {user.username}")
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                app.logger.debug("Password check passed")
                return redirect(url_for('main'))
            else:
                app.logger.debug("Password check failed")
                flash('아이디 또는 비밀번호가 잘못되었습니다.')
        except User.DoesNotExist:
            app.logger.debug("User does not exist")
            flash('아이디 또는 비밀번호가 잘못되었습니다.')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        grade = int(request.form['grade'])
        parent_contact = request.form['parent_contact']
        user_class = request.form['class']
        school = request.form['school']
        username = request.form['username']
        password = request.form['password']

        if len(password) < 4:
            flash('비밀번호는 최소 4자리 이상이어야 합니다.')
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            user = User.get(User.username == username)
            flash('이미 존재하는 사용자 이름입니다.')
        except User.DoesNotExist:
            user = User.create(
                name=name,
                grade=grade,
                parent_contact=parent_contact,
                user_class=user_class,
                school=school,
                username=username,
                password=hashed_password
            )
            flash('회원가입이 완료되었습니다. 로그인 해주세요.')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    try:
        user = User.get_by_id(user_id)
        return render_template('main.html', user=user)
    except User.DoesNotExist:
        flash('사용자 정보를 찾을 수 없습니다.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
