from application import app
from flask import session
import page.user_config as uconfig

if __name__ == "__main__":
    app.debug=True
    app.secret_key = "temp key"
    app.run()