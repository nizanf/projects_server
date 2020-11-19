from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'nizan'  # should be secured
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/user/name
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port = 5000, debug=True)

# 404 ERROR
# 400 BAD REQUEST
# 200 success
# 201 created
# 500 internal Server Error
