from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    '''
    In the above relationship a ItemModel object list is created for each
    store. [<Item 1>, <Item 2>] etc.
    You can access the properties off it.

    When a storemodel is created it creates an object for each item in
    corresponding table.
    When you put lazy = dynamic it does not do that.
    However when accessing these records it has to go the database
    everytime which is slower.
    This is a trade off between memory space & speed.
    '''

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in
                self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # SELECT * FROM items WHERE name=name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
