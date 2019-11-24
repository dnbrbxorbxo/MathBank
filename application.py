from flask import Flask

app = Flask(__name__)

# jinja2의 조건문(break)을 제약없이 쓰기 위한 문구
app.jinja_env.add_extension("jinja2.ext.loopcontrols")