from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']db = SQLAlchemy()
db.init_app(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'id': m.id, 'text': m.text} for m in messages])

@app.route('/messages', methods=['POST'])
def add_message():
    text = request.json['text']
    m = Message(text=text)
    db.session.add(m)
    db.session.commit()
    return jsonify({'id': m.id}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
