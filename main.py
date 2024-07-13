from application import app
from flask import session
import DefaultCategory
from models import initialize_db, Paper


# 플래그를 사용하여 데이터베이스 초기화 및 기본 카테고리 설정이 한 번만 실행되도록 설정
initialized = False

@app.before_request
def initialize():
    global initialized
    if not initialized:
        initialize_db()
        DefaultCategory.SetDefaultCategory(Paper)
        initialized = True

if __name__ == "__main__":
    app.debug=True
    app.secret_key = "temp key"
    app.run(port=5010)
    app.run()