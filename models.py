import json

from peewee import *

# SQLite 데이터베이스 연결
db = SqliteDatabase('MathBank.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    grade = IntegerField()
    parent_contact = CharField()
    user_class = CharField()
    school = CharField()
    username = CharField(unique=True)
    password = CharField()
    approved = BooleanField(default=True)


class Paper(BaseModel):
    category = BooleanField(default=True)
    title = CharField()
    description = TextField()
    difficulty = IntegerField()
    question_type = CharField()  # 'objective' or 'subjective'
    options = TextField(null=True)  # JSON string to store multiple choice options
    correct_answer = CharField()
    answer = TextField(null=True)  # Answer to the question
    solution = TextField()
    explanation_pdf = CharField(null=True)
    explanation_image = CharField(null=True)
    explanation_video_link = CharField(null=True)
    parent = ForeignKeyField('self', null=True, backref='children')

class Worksheet(BaseModel):
    title = CharField()
    description = TextField()
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    papers_json = TextField(default='[]')  # JSON string to store related papers
    pdf_file = TextField()

    option1 = IntegerField()
    option2 = IntegerField()
    option3 = IntegerField()


# 데이터베이스 초기화
db.connect()

def initialize_db():
    print(User.table_exists())
    if not User.table_exists():
        db.create_tables([User], safe=True)
    if not Paper.table_exists():
        db.create_tables([Paper], safe=True)

    if not Worksheet.table_exists():
        db.create_tables([Worksheet], safe=True)



