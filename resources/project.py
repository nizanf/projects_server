from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.project import ProjectModel


class Project(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return project.json()
        return {'message': 'Project not found'}, 404

    def post(self, name):
        if ProjectModel.find_by_name(name):
            return {'message': "A project with name '{}' already exists.".format(name)}, 400

        data = Project.parser.parse_args()

        project = ProjectModel(name, **data)

        try:
            project.save_to_db()
        except:
            return {"message": "An error occurred inserting the project.py."}, 500

        return project.json(), 201

    def delete(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            project.delete_from_db()
            return {'message': 'project deleted.'}
        return {'message': 'project not found.'}, 404

    def put(self, name):
        data = Project.parser.parse_args()

        project = ProjectModel.find_by_name(name)

        if project:
            project.date = data['date']
        else:
            project = ProjectModel(name, **data)

        project.save_to_db()

        return project.json()


class ProjectList(Resource):
    def get(self):
        return {'projects': [project.json() for project in ProjectModel.query.all()]}
