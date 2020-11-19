from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.activity import ActivityModel


class Activity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('project_id',
                        type=int,
                        required=True,
                        help="every activity needs a project id"
                        )

    @jwt_required()
    def get(self, name):
        activity = ActivityModel.find_by_name(name)
        if activity:
            return activity.json()
        return {'message': 'activity not found'}, 404

    def post(self, name):
        if ActivityModel.find_by_name(name):
            return {'message': "An activity with name '{}' already exists.".format(name)}, 400

        data = Activity.parser.parse_args()
        activity = ActivityModel(name, **data)

        try:
            activity.save_to_db()
        except:
            return {"message": "An error occurred inserting the activity."}, 500

        return activity.json(), 201

    def delete(self, name):
        activity = ActivityModel.find_by_name(name)
        if activity:
            activity.delete_from_db()
            return {'message': 'activity deleted.'}
        return {'message': 'activity not found.'}, 404

    def put(self, name):
        data = Activity.parser.parse_args()

        activity = ActivityModel.find_by_name(name)

        if activity:
            activity.name = data['name']
        else:
            activity = ActivityModel(name, **data)

        activity.save_to_db()

        return activity.json()


class ActivityList(Resource):
    def get(self):
        return {'activity': [activity.json() for activity in ActivityModel.query.all()]}
