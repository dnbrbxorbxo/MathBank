import pymysql
import numpy as np

conn = pymysql.connect(host="호스팅 주소", user="아이디", password="비밀번호", database="DB명")

cursor = conn.cursor()
cursor.execute("set names utf8")
