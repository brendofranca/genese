from user_api.db.user_database import user_database as database


class UserModel(database.Model):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True, autoincrement=False)
    name = database.Column(database.String(50))
    cpf = database.Column(database.Integer, unique=True)
    email = database.Column(database.String(120))
    phone_number = database.Column(database.Integer)
    created_at = database.Column(database.DateTime, default=database.func.datetime('now', 'localtime'))
    updated_at = database.Column(database.DateTime, default=database.func.datetime('now', 'localtime'),
                                 onupdate=database.func.datetime('now', 'localtime'))

    def __init__(self, id, name, cpf, email, phone_number):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.email = email
        self.phone_number = phone_number

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "cpf": self.cpf,
            "email": self.email,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_user(cls, id):
        user = cls.query.filter_by(id=id).first()

        if user:
            return user
        return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def update_user(self, name, cpf, email, phone_number):
        self.name = name
        self.cpf = cpf
        self.email = email
        self.phone_number = phone_number

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
