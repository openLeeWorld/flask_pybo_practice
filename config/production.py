from config.default import *

# 아래는 sqlite 사용 안하면 삭제함
#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'Zb3\x81\xdb\xf1\xd9\xd7-Knb\x8eB\xa5\x18'
# 서버 환경에서 python -c "import os; print(os.urandom(16))"으로
# SECRET_KEY = <붙여넣음>

# 운영 환경 로깅 설정 (DEBUG=False이므로 로그를 파일로 저장한다.)
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/myproject.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

# postgresql 연동 설정
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, '.env')) # 서버에 따로 .env생성 후 작성함

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=os.getenv('DB_USER'),
    pw=os.getenv('DB_PASSWORD'),
    url=os.getenv('DB_HOST'),
    db=os.getenv('DB_NAME'),
)
