from jano_service.database.database import db
from jano_service.tools.extras import create_random_id, create_password_hash


class UserLoginModel(db.Model):
    __tablename__ = 'userlogin'
    id = db.Column(db.String(), primary_key=True, autoincrement=False, index=True)
    username = db.Column(db.String(32), primary_key=True, autoincrement=False, index=True)
    password = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=db.func.datetime('now', 'localtime'))
    updated_at = db.Column(db.DateTime, default=db.func.datetime('now', 'localtime'),
                           onupdate=db.func.datetime('now', 'localtime'))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            "username": self.username,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_user_login(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user
        return None

    def save_user_login(self, password):
        self.id = create_random_id()
        self.password = create_password_hash(password)
        db.session.add(self, password)
        db.session.commit()

    def update_user_login(self, username, password):
        self.username = username
        self.password = password

    def delete_user_login(self):
        db.session.delete(self)
        db.session.commit()