import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Paper
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

# 디버깅을 위한 로그 설정
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('main'))

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

                if not user.approved:
                    app.logger.debug("No auth")
                    flash('접근 권한이 없습니다. 관리자에게 문의하여 주세요.')
                else:
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


@app.route('/userlist')
def userlist():
    if 'user_id' in session:
        current_user = User.get(User.id == session['user_id'])
    else:
        current_user = None

    userlist = User.select()
    return render_template('userlist.html', userlist=userlist, user=current_user)


@app.route('/category')
def category():
    if 'user_id' in session:
        current_user = User.get(User.id == session['user_id'])
    else:
        current_user = None

    return render_template('category.html', user=current_user)

@app.route('/paper', methods=['POST'])
def create_paper():
    data = request.json
    parent_id = data.get('parent_id')
    parent = Paper.get(Paper.id == parent_id) if parent_id else None

    print(data)

    Paper.create(
        category=data.get('category') == 'true',
        title=data.get('title'),
        description=data.get('description'),
        difficulty=data.get('difficulty'),
        question_type=data.get('question_type'),
        options=data.get('options'),
        correct_answer=data.get('correct_answer'),
        answer=data.get('answer'),
        solution=data.get('solution'),
        explanation_pdf=data.get('explanation_pdf'),
        explanation_image=data.get('explanation_image'),
        explanation_video_link=data.get('explanation_video_link'),
        parent=parent
    )
    return redirect(url_for('get_papers'))

@app.route('/paper/<int:paper_id>', methods=['POST'])
def update_paper(paper_id):
    data = request.json
    parent_id = data.get('parent_id')
    parent = Paper.get(Paper.id == parent_id) if parent_id else None
    paper = Paper.get(Paper.id == paper_id)
    paper.category = data.get('category') == 'true'
    paper.title = data.get('title')
    paper.description = data.get('description')
    paper.difficulty = data.get('difficulty')
    paper.question_type = data.get('question_type')
    paper.options = data.get('options')
    paper.correct_answer = data.get('correct_answer')
    paper.answer = data.get('answer')
    paper.solution = data.get('solution')
    paper.explanation_pdf = data.get('explanation_pdf')
    paper.explanation_image = data.get('explanation_image')
    paper.explanation_video_link = data.get('explanation_video_link')
    paper.parent = parent
    paper.save()
    return redirect(url_for('get_papers'))

@app.route('/paper/<int:paper_id>/delete', methods=['POST'])
def delete_paper(paper_id):
    paper = Paper.get(Paper.id == paper_id)
    paper.delete_instance(recursive=True)
    return redirect(url_for('get_papers'))

@app.route('/papers', methods=['GET'])
def get_papers():
    papers = Paper.select().dicts()
    return jsonify(list(papers))

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    user_id = data.get('id')
    new_password = data.get('password')

    try:
        user = User.get(User.id == user_id)
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        user.save()
        return jsonify({'message': '비밀번호가 성공적으로 변경되었습니다.'})
    except User.DoesNotExist:
        return jsonify({'message': '사용자를 찾을 수 없습니다.'}), 404


@app.route('/toggle_approval', methods=['POST'])
def toggle_approval():
    data = request.get_json()
    user_id = data.get('id')

    try:
        user = User.get(User.id == user_id)
        user.approved = not user.approved
        user.save()
        return jsonify({'approved': user.approved, 'message': '접근 권한 상태가 변경되었습니다.'})
    except User.DoesNotExist:
        return jsonify({'message': '사용자를 찾을 수 없습니다.'}), 404


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
