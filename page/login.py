import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from application import app
import page.user_config as uconfig

from flask import session, request
from flask import redirect, url_for, render_template

# 로그인
@app.route("/login", methods=("GET", "POST"))
def login():
    # 에러 메시지
    error = None

    if request.method == "POST":
        # html에서 넘어오는 아이디와 비밀번호
        id_form = request.form["user_id"]
        pw_form = request.form["user_pw"]

        # 아이디나 비밀번호가 비어있을 때
        if not id_form:
            error = "아이디를 입력해주세요."
        elif not pw_form:
            error = "비밀번호를 입력해주세요."

        # 아이디 또는 비밀번호를 잘못 입력했을 때
        elif not id_form == uconfig.aid or not pw_form == uconfig.apw:
            error = "아이디 또는 비밀번호가 틀렸습니다."

        # 정상 입력 시
        if error is None:
            session.clear()
            session[uconfig.sid] = uconfig.aid # 세션에 아이디를 저장
            return redirect(url_for("index"))

    return render_template("login.html", error=error)

# 로그아웃
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))