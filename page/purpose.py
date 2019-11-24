from application import app
import page.user_config as uconfig
import database

from flask import session
from flask import redirect, url_for, render_template

import random

def dataRequest():
    database.cursor.execute("SELECT intent, COUNT(*) FROM chatbot_statistics GROUP BY intent")
    rows = database.cursor.fetchall()
    rows = dict(rows)
    labels = list(rows.keys())
    data = list(rows.values())
    return labels, data

def rankRequest(intent):
    query = f"SELECT ifnull (location, '없음'), COUNT(*) FROM chatbot_statistics WHERE intent = '{intent}' GROUP BY location"
    database.cursor.execute(query)
    rows = database.cursor.fetchall()
    rows = dict(rows)
    labels = list(rows.keys())
    data = list(rows.values())
    print(labels, data, intent)
    return labels, data

@app.route('/purpose')
def purpose():
    if uconfig.sid in session:
        if session[uconfig.sid] == uconfig.aid: # 관리자 로그인 여부
            labels, data = dataRequest()
            attraction_label, attraction_data = rankRequest('관광지')
            travel_label, travel_data = rankRequest('여행지')
            restaurant_label, restaurant_data = rankRequest('맛집')
            weather_label, weather_data = rankRequest('날씨')
            dust_label, dust_data = rankRequest('먼지')

            return render_template('purpose.html', label = labels, count = data,
                                    attraction_label = attraction_label,
                                    attraction_data = attraction_data,

                                    travel_label = travel_label,
                                    travel_data = travel_data,

                                    restaurant_label = restaurant_label,
                                    restaurant_data = restaurant_data,

                                    weather_label = weather_label,
                                    weather_data = weather_data,
                                    
                                    dust_label = dust_label,
                                    dust_data = dust_data)

    return redirect(url_for('index'))