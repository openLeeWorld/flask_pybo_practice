from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
# flash는 프로그램 논리 오류를 발생시키는 함수 -> 템플릿에 표시 가능
# generate_password_hash함수로 암호화하면 복호화 불가능
from pybo import db
from pybo.forms import UserCreateFrom, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateFrom()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                password=generate_password_hash(form.password1.data),
                email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.') 
    return render_template('auth/signup.html', form=form) # GET

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None: # 플라스크 세션에 사용자 정보 저장
            session.clear() 
            session['user_id'] = user.id # 플라스크 user_id문자열에 키로 id값 저장
            _next = request.args.get('next', '')
            if _next: # next 파라미터가 있으면 원래 가려던 페이지로 다시 이동시킴
                return redirect(_next)
            else: # 없으면 홈페이지로 이동
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request # 라우팅 함수보다 항상 먼저 실행되는 애노테이션
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None # g는 플라스크의 컨텍스트 변수
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear() # session의 user_id 삭제 및 g.user도 None
    return redirect(url_for('main.index'))

# g.user가 있는지 조사하여 없으면 로그인 URL로 리다이렉트하고 있으면 원래 함수를 실행하는
# 애너테이션 지정
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None: # 로그아웃 상태
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs) # 원래 함수 실행
    return wrapped_view # 애노테이션 적용시킴, 함수 자체를 반환해야 함









