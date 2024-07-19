from flask import Blueprint, url_for, current_app
from werkzeug.utils import redirect
# url_for로 main에서 redirect 기능 수행
# werkzeug는 WSGI web application 라이브러리로 개발자가 필요한 모듈만 이용

bp = Blueprint('main', __name__, url_prefix="/")


# __name__은 모듈명인 main_views가 전달된다.
# main은 bp의 별칭이며 url_for함수에서 사용된다.

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index(): # 질문을 최근 순으로 얻어서 template에 전달
    current_app.logger.info("INFO 레벨로 출력")
    # current_app은 플라스크 앱 app 의미하며 request와 같은 컨텍스트 객체이다.
    return redirect(url_for('question._list'))
#url_for(<블루프린트 이름>.<라우트 함수명>) -> 매핑 url 리턴