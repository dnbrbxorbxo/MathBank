# import os
# import sys

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from application import app
import page.user_config as uconfig

from flask import session
from flask import redirect, url_for

@app.route("/")
def index():
    # 자동 로그인
    
    # 로그인 여부
    if uconfig.sid in session:
        if session[uconfig.sid] == uconfig.aid:
            return redirect(url_for("admin"))

    return redirect(url_for("login"))