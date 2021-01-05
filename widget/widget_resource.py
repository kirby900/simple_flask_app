from widget.widget_model import WidgetModel, db
from flask_restful import Resource, request


class WidgetListResource(Resource):
    def get(self):
        sort = request.args.get("sort", "id")
        widgets = WidgetModel.query.all()
        return {"widgets": [w.json() for w in widgets]}

    def post(self):
        data = request.get_json()
        widget = WidgetModel(
            name=data["name"], color=data["color"], weight=data.get("weight", None)
        )
        db.session.add(widget)
        db.session.commit()
        return widget.json(), 201


class WidgetResource(Resource):
    def get(self, id):
        sort = request.args.get("sort", "id")
        widget = WidgetModel.find_by_id(id)
        return widget.json()

    def put(self, id):
        data = request.get_json()
        widget = WidgetModel.find_by_id(id)
        widget.name = data["name"]
        widget.color = data["color"]
        widget.weight = data.get("weight", None)
        db.session.add(widget)
        db.session.commit()
        return widget.json()

    def delete(self, id):
        widget = WidgetModel.find_by_id(id)
        db.session.delete(widget)
        db.session.commit()
        return widget.json()
