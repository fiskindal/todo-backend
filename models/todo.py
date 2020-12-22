from db import db

class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80))
    isChecked = db.Column(db.Boolean)

    def __init__(self, id, todo,isChecked):
        self.id = id
        self.todo = todo
        self.isChecked = isChecked
    
    def json(self):
        return {
            'id':self.id,
            'todo':self.todo,
            'isChecked':self.isChecked
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_todo(cls,_todo):
        return cls.query.filter_by(todo=_todo).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()