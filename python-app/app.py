from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import func
import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.static_folder = 'static'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'<Message {self.id}>'

@app.route('/')
def index():
    messages = db.session.query(Message).all()
    formatted_messages = []
    for message in messages:
        moscow_time = message.created_at + datetime.timedelta(hours=3)
        formatted_messages.append((message, moscow_time.strftime('%H:%M:%S %d.%m.%Y')))
    return render_template('index.html', messages=formatted_messages)

@app.route('/create', methods=['GET', 'POST'])
def create_message():
    if request.method == 'POST':
        text = request.form['text']
        m = Message(text=text)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
