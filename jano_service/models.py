from jano_service.database import db
from jano_service.extras import create_hash_id, create_hash_pwd


class UserLoginModel(db.Model):
    __tablename__ = 'userlogin'
    hash_id = db.Column(db.String(128), primary_key=True, autoincrement=False, default=create_hash_id())
    username = db.Column(db.String(32), primary_key=True, autoincrement=False, index=True)
    hash_pwd = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.datetime('now', 'localtime'))
    updated_at = db.Column(db.DateTime, default=db.func.datetime('now', 'localtime'),
                           onupdate=db.func.datetime('now', 'localtime'))

    def __init__(self, username, hash_pwd):
        self.username = username
        self.hash_pwd = hash_pwd

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

    def save_user_login(self, hash_pwd):
        self.hash_pwd = create_hash_pwd(hash_pwd)
        db.session.add(self, hash_pwd)
        db.session.commit()

    def update_user_login(self, username, hash_pwd):
        self.username = username
        self.hash_pwd = create_hash_pwd(hash_pwd)

    def delete_user_login(self):
        db.session.delete(self)
        db.session.commit()