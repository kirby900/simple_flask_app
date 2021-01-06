import os
from flask import Flask, render_template, redirect, request, url_for
from flask_restful import Api

from db import db

# from user_model import UserModel
# from user_resource import UserListResource, UserResource
from widget.widget_model import WidgetModel

# from widget.widget_resource import WidgetListResource, WidgetResource


app = Flask(__name__)

# Look for environment variable DATABASE_URL.
# If found, use it; otherwise, use local SQLite file.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.template_filter("hide_none")
def suppress_none(value):
    """Suppress converting NoneType to 'None' """
    return value if value is not None else ""


api = Api(app)

# API endpoints
# api.add_resource(UserListResource, "/api/users")
# api.add_resource(UserResource, "/api/users/<id>")

# api.add_resource(WidgetListResource, "/api/widgets")
# api.add_resource(WidgetResource, "/api/widgets/<id>")


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# @app.route("/users")
# def users():
#     # query all users
#     users = UserModel.query.order_by(UserModel.id).all()
#     return render_template("users.html", users=users)


@app.route("/widgets")
def get_widgets():
    # query all widgets
    widgets = WidgetModel.query.order_by(WidgetModel.name).all()
    return render_template("widget_list.html", widgets=widgets)


@app.route("/widgets", methods=["POST"])
def post_widgets():
    name = request.form.get("name")
    color = request.form.get("color")
    weight = request.form.get("weight")
    new_widget = WidgetModel(name=name, color=color, weight=weight)
    db.session.add(new_widget)
    db.session.commit()
    return redirect(url_for("get_widgets"))


@app.route("/widgets/<id>/edit")
def get_edit_widget(id):
    widget = WidgetModel.find_by_id(id)
    return render_template("widget_edit.html", widget=widget)


@app.route("/widgets/<id>/edit", methods=["POST"])
def post_edit_widget(id):
    widget = WidgetModel.find_by_id(id)
    if widget:
        widget.name = request.form.get("name")
        widget.color = request.form.get("color")
        weight = request.form.get("weight", "")
        widget.weight = weight if len(weight) > 0 else None
        db.session.commit()
    else:
        print(f"POST to {request.url} found no matching entry")
    return redirect(url_for("get_widgets"))


@app.route("/widgets/<id>/delete")
def delete_widget(id):
    widget = WidgetModel.find_by_id(id)
    if widget:
        db.session.delete(widget)
        db.session.commit()
    else:
        print(f"Request to {request.url} found no match -- ignored")
    return redirect(url_for("get_widgets"))


if __name__ == "__main__":
    app.run()
