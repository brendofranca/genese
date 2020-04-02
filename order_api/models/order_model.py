import requests
from order_api.db.order_database import order_database as database


class OrderModel(database.Model):
    __tablename__ = 'order'

    id = database.Column(database.Integer, primary_key=True, autoincrement=False)
    user_id = database.Column(database.Integer)
    item_description = database.Column(database.String(50))
    item_quantity = database.Column(database.Integer)
    item_price = database.Column(database.Float())
    total_value = database.Column(database.Float())
    created_at = database.Column(database.DateTime, default=database.func.datetime('now', 'localtime'))
    updated_at = database.Column(database.DateTime, default=database.func.datetime('now', 'localtime'),
                                 onupdate=database.func.datetime('now', 'localtime'))

    def __init__(self, id, user_id, item_description, item_quantity, item_price):
        self.id = id
        self.user_id = user_id
        self.item_description = item_description
        self.item_quantity = item_quantity
        self.item_price = item_price
        self.total_value = item_quantity * item_price

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_description": self.item_description,
            "item_quantity": self.item_quantity,
            "item_price": self.item_price,
            "total_value": self.total_value,
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
        database.session.add(self)
        database.session.commit()

    def update_order(self, user_id, item_description, item_quantity, item_price):
        self.user_id = user_id
        self.item_description = item_description
        self.item_quantity = item_quantity
        self.item_price = item_price
        self.total_value = item_quantity * item_price

    def delete_order(self):
        database.session.delete(self)
        database.session.commit()


class UserService:
    @classmethod
    def get_user(cls, user_id):
        url_user = 'http://127.0.1.1:5000/api/user/' + str(user_id)

        try:
            url_response = requests.get(url_user)
        except:
            return False

        if url_response.status_code == 200:
            return True
        else:
            return False
