from user_model import UserModel, db
from flask_restful import Resource, request


class UserListResource(Resource):
    def get(self):
        sort = request.args.get("sort", "id")
        users = UserModel.query.all()
        return {"users": [u.json() for u in users]}

    def post(self):
        data = request.get_json()
        user = UserModel(username=data["username"], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return user.json(), 201


class UserResource(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)
        return user.json()

    def put(self, id):
        data = request.get_json()
        user = UserModel.find_by_id(id)
        user.username = data["username"]
        user.password = data["password"]
        db.session.add(user)
        db.session.commit()
        return user.json()

    def delete(self, id):
        user = UserModel.find_by_id(id)
        db.session.delete(user)
        db.session.commit()
        return user.json()
