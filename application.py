import json
import os
import random
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import User, Paper , Worksheet
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

app.config['UPLOAD_FOLDER'] = 'PaperFile/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 디버깅을 위한 로그 설정
logging.basicConfig(level=logging.DEBUG)

app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/DownloadPaper/<filename>')
def download_file(filename):
    return send_from_directory('PaperFile', filename)

@app.route('/')
def home():
    try:
        if 'user_id' not in session:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('main'))
    except KeyError as e:
        print(f"Session Key Error: {e}")
        session.clear()
        return redirect(url_for('login'))
    except Exception as e:
        print(f"Unexpected Error: {e}")

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


@app.route('/worksheet')
def worksheet():
    if 'user_id' in session:
        current_user = User.get(User.id == session['user_id'])
    else:
        current_user = None
    worksheet = Worksheet.select().order_by(Worksheet.created_at.desc())

    return render_template('worksheet.html', user=current_user , worksheet = worksheet)


@app.route('/save-paper', methods=['POST'])
def save_paper():
    data = request.form
    file_question = request.files.get('question_file')
    file_explanation = request.files.get('explanation_file')

    if 'id' in data and data['id']:
        paper = Paper.get_by_id(data['id'])
    else:
        paper = Paper()

    paper.category = (data['category'] == 1)
    paper.title = data['title']
    paper.difficulty = data['difficulty']
    paper.question_type = data['question_type']
    paper.correct_answer = data['correct_answer']
    paper.description = data['description']
    paper.options = data['options']
    paper.parent_id = data['parent_id']

    if file_question:
        filename_question = secure_filename(file_question.filename)
        file_question.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_question))
        paper.solution = filename_question

    if file_explanation:
        filename_explanation = secure_filename(file_explanation.filename)
        file_explanation.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_explanation))
        paper.explanation_pdf = filename_explanation
        paper.explanation_image = filename_explanation

    paper.save()

    return jsonify({'status': 'success'})


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

import random

def create_worksheet(title , worksheet_paper_list, rows=2, cols=2):
    """
        Create an HTML string for a worksheet from a list of Paper objects with images.

        :param worksheet_paper_list: List of Paper objects containing question images.
        :param rows: Number of rows in the grid.
        :param cols: Number of columns in the grid.
        :return: HTML string representing the worksheet.
        """
    random.shuffle(worksheet_paper_list)  # Randomize the order of questions

    total_items = len(worksheet_paper_list)
    items_per_page = rows * cols
    total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page != 0 else 0)

    html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #fff;
            }}
            .page {{
                page-break-after: always;
                margin-bottom: 50px;
                padding: 20px;
                border: 1px solid #000;
                background-color: #fff;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .grid-container {{
                display: grid;
                grid-template-columns: repeat({cols}, 1fr);
                grid-template-rows: repeat({rows}, 1fr);
                gap: 20px;
                margin-bottom: 30px;
                height: calc(100vh - 40px);
            }}
            .question {{
                background-color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }}
            .question img {{
                max-width: 100%;
                height: auto;
                margin-bottom: 10px;
            }}
            .question-number {{
                font-weight: bold;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
    """

    # Add images to the grid, page by page
    for page in range(total_pages):
        html_content += f'<div class="page"><div class="header">' \
                        f'<h2>{title}</h2>' \
                        f'<h5>페이지 {page + 1}</h5></div>' \
                        f'<div class="grid-container" style = "border-top: 1px solid black;">'

        for i in range(items_per_page):
            index = page * items_per_page + i
            if index < total_items:
                paper = worksheet_paper_list[index]
                img_path = paper.solution  # Access the image path from the Paper object
                difficulty = paper.difficulty  # Access the image path from the Paper object
                html_content += f"""
                    <div class="question">
                        <div class="question-number">문제 {index + 1} 번 ( 난이도 {difficulty} )</div>
                        <img src="/DownloadPaper/{img_path}" alt="Question Image">
                    </div>
                    """
        html_content += '</div></div>'

    html_content += """
    </body>
    </html>
    """

    return html_content


@app.route('/save-worksheet', methods=['POST'])
def save_worksheet():
    try:
        # Parse form data
        title = request.form.get('title')
        description = request.form.get('description')
        option1 = int(request.form.get('option1', 0))
        option2 = int(request.form.get('option2', 0))
        option3 = int(request.form.get('option3', 0))
        papers_json = request.form.get('papers_json')


        # Parse JSON data into an array
        try:
            papers = json.loads(papers_json)
        except json.JSONDecodeError:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data for papers'}), 400

        worksheet_paper_list = []

        # Filter and collect papers based on difficulty, category, and parent_id
        for difficulty, count in [("상", option1), ("중", option2), ("하", option3)]:
            # Extract parent_ids from papers
            parent_ids = [p['id'] for p in papers]

            # Fetch papers for the given difficulty, category N, and parent IDs
            matching_papers = Paper.select().where(
                (Paper.parent_id.in_(parent_ids)) &  # Use parent_id for filtering
                (Paper.difficulty == difficulty) &  # Use correct difficulty filtering
                (Paper.category == False)  # Assuming N is represented as False
            ).limit(count)

            # Append the matched papers to the worksheet_paper_list
            worksheet_paper_list.extend(matching_papers)

            # Print the titles of the matched papers for debugging
            print(f"Difficulty Level {difficulty}:")
            for paper in matching_papers:
                print(f"- {paper.title}")

        # Shuffle the worksheet_paper_list to randomize the order
        random.shuffle(worksheet_paper_list)  # Correct use of random.shuffle

        html_content = create_worksheet(title , worksheet_paper_list, rows=2, cols=2)



        # Create a new Worksheet instance
        worksheet = Worksheet.create(
            title=title,
            description=description,
            option1=option1,
            option2=option2,
            option3=option3,
            papers_json=papers_json,  # Store as JSON string
            pdf_file = html_content
        )

        return jsonify({'status': 'success', 'message': 'Worksheet saved successfully', 'worksheet_id': worksheet.id , "worksheet_form" : html_content})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

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
