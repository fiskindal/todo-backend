from flask_restful import Resource, reqparse
from models.todo import TodoModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional


class Todo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int)
    parser.add_argument('todo',
                        type=str,
                        required=True
                        )
    parser.add_argument('isChecked',
                        type=bool)
    @jwt_required
    def get(self, id):
        todo = TodoModel.find_by_id(id)
        if id:
            return todo.json()
        return {'message': 'todo not found'}, 404

    @fresh_jwt_required
    def post(self,id):
        if TodoModel.find_by_id(id):
            return {'message': "An todo'{}' already exists.".format(id) }
        data = Todo.parser.parse_args()

        todo = TodoModel(data['id'], data['todo'], data['isChecked'])
        try:
            todo.save_to_db()
        except:
            return {"message": "an error occurred inserting the todo"}, 500
        return {"message": "Todo created successfully"}, 201

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        todo = TodoModel.find_by_id(id)
        if todo:
            todo.delete_from_db()
            return {'message': 'Todo deleted.'}
        return {'message': 'Todo not found'}

    def put(self, id):
        data = Todo.parser.parse_args()
        todo = TodoModel.find_by_id(id)

        if todo:
            todo.id == data['id']
        else:
            todo = TodoModel(data['id'], data['todo'], data['isChecked'])


class TodoList(Resource):
    @jwt_optional
    def get(self):
        return {'todos': list(map(lambda x: x.json(), TodoModel.query.all()))}
