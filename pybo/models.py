from pybo import db # __init__.py에서 선언한 db객체

question_voter = db.Table( # 질문이나 답변의 추천인
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'),
        primary_key=True)
) # ManyToMany 관계를 위해 연결 테이블 생성

answer_voter = db.Table( # 질문이나 답변의 추천인
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'),
        primary_key=True)
) # ManyToMany 관계를 위해 연결 테이블 생성

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 플라스크 pk로 설정시 자동으로 증가
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False)
    # user_id추가하고 nullable=False로 db upgrade하면 기존 데이터 때문에 오류가 남
    # 따라서 server_default를 추가하여 기존 데이터에도 기본값을 저장시킴
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter,
        backref=db.backref('question_voter_set'))
    # secondary로 테이블 객체를 지정해서 저장된 정보를 연결함
    # backref 이름은 중복될 수 없다.


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                        nullable=False)
    # user_id추가하고 nullable=False로 db upgrade하면 기존 데이터 때문에 오류가 남
    # 따라서 server_default를 추가하여 기존 데이터에도 기본값을 저장시킴
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter,
        backref=db.backref('answer_voter_set'))

# question 칼럼은 답변 모델에서 연결된 질문 모델을 참조함 ex)answer.question.subject
# backref는 역참조를 위함(질문에 달린 답변들 참조)
# backref=db.backref('answer_set', cascade='all, delete-orphan))
# ㄴ 위는 질문 데이터를 삭제할 때 연관 답변 모두를 같이 삭제한다.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)














