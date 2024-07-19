from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False # 이벤트 처리 옵션
# 데이터베이스 파일은 홈 디렉터리 바로 밑에 pybo.db로 저장됨
SECRET_KEY = "dev" # CSRF 토큰 생성 시 활용
# CSRF 토큰은 폼으로 전송된 데이터가 실제 웹 페이지에서 작성된 데이터인지를 판단