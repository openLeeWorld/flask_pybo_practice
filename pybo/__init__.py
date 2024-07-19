from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy # flask용 ORM class
from sqlalchemy import MetaData
import config
#from flaskext.markdown import Markdown

naming_convention = {
    "ix": 'ix_%(column_0_labels)s', # index
    "uq": "uq_%(table_name)s_%(column_0_name)s", # unique key
    "ck": "ck_%(table_name)s_%(column_0_name)s", #
    "fk": "fk_%(table_name)s_%(column_0_name)s_%%(referred_table_name)s", # foriegn key
    "pk": "pk_%(table_name)s", # primary key
}
# SQLite가 발생시킬 수 있는 제약 조건 오류 해결을 위한 이름 변경

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

from . import models

def create_app():  # application factory
    app = Flask(__name__)  # __name__에는 모듈명이 담김
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown(버그가 있음)
    #Markdown(app, extensions=['n12br', 'fenced_code'])
    # nl1br은 줄바꿈 문자를 <br>로 바꿔준다.
    # fenced_code는 코드 표시 기능을 위해 추가했다.

    return app

# create_app은 플라스크 내부에서 정의된 함수명이므로 변경 금지
