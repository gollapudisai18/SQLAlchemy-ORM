from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://username:password@localhost:1521/xe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50))
    def __init__(self,id,name,email):
        self.id = id
        self.name = name
        self.email = email



@app.route('/users', methods=['POST'])
def create_user():
    id  = request.json['id']
    name = request.json['name']
    email = request.json['email']
    new_user = User(id = id,name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return 'User created successfully'

@app.route('/users', methods=['GET'])
def read_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.name = request.json['name']
    user.email = request.json['email']
    db.session.commit()
    return 'User updated successfully'

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return 'User deleted successfully'

if __name__ == '__main__':
    
    with app.app_context():
      db.create_all()
    app.run(debug = True)
