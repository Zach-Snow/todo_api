from flask import Flask
from flask_restful import Api
from root import Root
from todo_module import todo

app = Flask(__name__)
api = Api(app)

# Root path
api.add_resource(Root, "/", "/v1/" )

api.add_resource(todo, "/v1/todo/<todoID>",
                            "/v1/todo/")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)