import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db
from security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///data.db')
# sqlite can be MySQL,Oracle etc. Default value given to run local instance.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

'''When using uwsgi below block does not run it gets app from above
 & runs by itself including app.run does not run.
'''
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)  # Gives htmlpage to check errors
