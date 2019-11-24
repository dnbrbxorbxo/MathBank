from application import app
import page.user_config as uconfig
import database

from flask import session,request
from flask import redirect, url_for, render_template

def dbEntityCounting():

    # entity 개수
    query = "SELECT ifnull (entity, '없음'), COUNT(*) FROM `chatbot_statistics` WHERE intent = %s GROUP BY entity"
    
    database.cursor.execute(query, '관광지')
    attraction = database.cursor.fetchall()

    database.cursor.execute(query, '여행지')
    travel = database.cursor.fetchall()

    database.cursor.execute(query, '맛집')
    restaurant = database.cursor.fetchall()

    # location 개수
    query = "SELECT ifnull (location, '없음'), COUNT(*) FROM `chatbot_statistics` WHERE intent = %s GROUP BY location"

    database.cursor.execute(query, '날씨')
    weather = database.cursor.fetchall()
    
    database.cursor.execute(query, '먼지')
    dust = database.cursor.fetchall()

    return attraction, travel, restaurant, weather, dust

@app.route('/entity')
def entity():
    if uconfig.sid in session:
        if session[uconfig.sid] == uconfig.aid: # 관리자 로그인 여부
            attraction, travel, restaurant, weather, dust = dbEntityCounting()

            return render_template('entity.html',
                                    attraction = attraction,
                                    travel = travel,
                                    restaurant = restaurant,
                                    weather = weather,
                                    dust = dust)
    
    return redirect(url_for('index'))