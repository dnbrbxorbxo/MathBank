from application import app
import page.user_config as uconfig
import database
import numpy as np

from flask import session
from flask import redirect, url_for, render_template


def dialog_request():
    database.cursor.execute("SELECT * FROM chatbot_users;")
    user_reg = database.cursor.fetchall()
    user_tong = user_reg
    
    user_length = len(user_reg)
    use = np.array(range(1, user_length+1))
    use = list(use)

    user_reg = np.array(user_reg)
    user_join = user_reg[:, 3]
    user_reg = user_reg[:, 1]

    chat_box = []
    keys = ("user", "question", "answer")

    '''
    for i in user_reg:
        uid = i
        database.cursor.execute(f"SELECT user_id, question, answer FROM chatbot_chat WHERE user_id='{uid}';")
        rows = database.cursor.fetchall()
    
        for row in rows:
            myzip = zip(keys, row)
            mydict = dict(myzip)
            chat_box.append(mydict)

    return user_reg, chat_box # list
    '''
    for i in user_reg:
        uid = i
        database.cursor.execute(f"SELECT user_id, question, answer FROM chatbot_chat WHERE user_id='{uid}';")
        rows = database.cursor.fetchall()
    # print(type(rows)) 튜플

        for row in rows:
            chat_box.append(row)

    

    return user_reg, chat_box, user_length, use, user_join, user_tong


@app.route("/dialog")
def dialog():
    if uconfig.sid in session:
        if session[uconfig.sid] == uconfig.aid: # 관리자 로그인 여부
            user_reg, chat_box, user_length, use, user_join, user_tong = dialog_request()
            print(user_reg, chat_box, user_length, use, user_join, user_tong)
            return render_template("dialog.html", user_reg=user_reg, chat_box=chat_box,
                                    user_length=user_length, use=use, user_join=user_join,
                                    user_tong=user_tong)
    
    return redirect(url_for("index"))