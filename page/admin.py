from application import app
import page.user_config as uconfig

from flask import session
from flask import redirect, url_for, render_template

@app.route("/admin")
def admin():
    if uconfig.sid in session:
        if session[uconfig.sid] == uconfig.aid: # 관리자 로그인 여부
            return render_template("admin.html")
    
    return redirect(url_for("index"))