from application import app
import page.index
import page.login
import page.admin
import page.dialog
import page.purpose
import page.entity
import page.serach_entity

from flask import session
import page.user_config as uconfig

if __name__ == "__main__":
    app.debug=True
    app.secret_key = "temp key"
    app.run()