from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.project import Project, ProjectList
from resources.activity import Activity, ActivityList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'nizan'  # should be secured
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

api.add_resource(Project, '/project/<string:name>')  # http://127.0.0.1:5000/user/name
api.add_resource(ProjectList, '/project')  # TBD
api.add_resource(Activity, '/activity/<string:name>') # TBD
api.add_resource(ActivityList, '/activity')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)

# 404 ERROR
# 400 BAD REQUEST
# 200 success
# 201 created
# 500 internal Server Error
