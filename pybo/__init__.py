from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy # flask용 ORM class
from sqlalchemy import MetaData

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

def page_not_found(e): # e는 오류 내용(템플릿에 e 전달 가능)
    return render_template('404.html'), 404 # 404 오류 페이지라고 명시

"""
def server_error(e):
    return render_template('500.html'), 500 # 500 오류 페이지 명시
"""
def create_app():  # application factory
    app = Flask(__name__)  # __name__에는 모듈명이 담김
    app.config.from_envvar('APP_CONFIG_FILE') # 환경변수에 담긴 파일을 환경 파일로 사용

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

    # 오류 페이지
    app.register_error_handler(404, page_not_found)
    #app.register_error_handler(500, server_error)

    return app

# create_app은 플라스크 내부에서 정의된 함수명이므로 변경 금지
