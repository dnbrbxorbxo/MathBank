from application import app
import page.user_config as uconfig
import database

from flask import session, request
from flask import redirect, url_for, render_template

def dbEntityCounting(entity, word):
    print(entity, word)
    if entity=='location':
        query = f"SELECT ifnull (entity, '없음'), COUNT(*) FROM `chatbot_statistics` WHERE location = '{word}' GROUP BY entity"
    elif entity=='entity':
        query = f"SELECT ifnull (location, '없음'), COUNT(*) FROM `chatbot_statistics` WHERE entity = '{word}' GROUP BY location"
    print(query)
    database.cursor.execute(query)
    
    return database.cursor.fetchall()
    

@app.route('/serach_entity', methods=("GET", "POST"))
def to_serach_entity():
    if uconfig.sid in session:
        if session[uconfig.sid] == uconfig.aid: # 관리자 로그인 여부
            entity = request.args.get('rdi_entity')
            word = request.args.get('search_word')
    
            result = dbEntityCounting(entity, word)
            print(result)

            return render_template('serach_entity.html', result = result, entity = entity)
    
    return redirect(url_for('index'))

# query = "SELECT ifnull (location, '없음'), COUNT(*) FROM `chatbot_statistics` WHERE intent = %s and entity = %s GROUP BY location"
# cursor.execute(query, ('맛집', '치킨'))

# print(cursor.fetchall())

# query = "SELECT ifnull (entity, '없음'), COUNT(*) FROM `chatbot_statistics` WHERE intent = %s and location = %s GROUP BY entity"
# cursor.execute(query, ('맛집', '서울'))

# print(cursor.fetchall())