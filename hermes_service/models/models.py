import requests
from hermes_service.database.database import db


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(), primary_key=True, autoincrement=False, index=True)
    username_id = db.Column(db.String())
    item_id = db.Column(db.String())
    item_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.datetime('now', 'localtime'))
    updated_at = db.Column(db.DateTime, default=db.func.datetime('now', 'localtime'),
                           onupdate=db.func.datetime('now', 'localtime'))

    def __init__(self, id, username_id, item_id, item_quantity):
        self.id = id
        self.username_id = username_id
        self.item_id = item_id
        self.item_quantity = item_quantity

    def json(self):
        return {
            "id": self.id,
            "username": self.username_id,
            "item_id": self.item_id,
            "item_quantity": self.item_quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def find_order(cls, id):
        order = cls.query.filter_by(id=id).first()
        if order:
            return order
        return None

    def save_order(self):
        db.session.add(self)
        db.session.commit()

    def update_order(self, username_id, item_id, item_quantity):
        self.username_id = username_id
        self.item_id = item_id
        self.item_quantity = item_quantity

    def delete_order(self):
        db.session.delete(self)
        db.session.commit()


class UserLoginServices:
    @classmethod
    def check_username(cls, username_id):
        url_service = 'http://127.0.0.1:8000/api/v1.0/user/' + str(username_id)
        try:
            request = requests.get(url_service)
        except:
            return False
        if request.status_code == 200:
            return True
        else:
            return False

