from application import app
from flask import session
import DefaultCategory
from models import initialize_db, Paper


if __name__ == "__main__":
    app.debug=True
    initialize_db()
    app.secret_key = "temp key"
    app.run(port=5010)
    app.run()