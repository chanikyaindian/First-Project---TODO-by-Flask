from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Todo(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(20), unique=False, nullable=False)
  description = db.Column(db.String(120), unique=False, nullable=False)
  time = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self) -> str:
    return f"{self.sno} {self.title}"


with app.app_context():
  db.create_all()


@app.route('/')
def home():
  return redirect('/todo')


# @app.route('/tasks')
# def show_tasks():
#   tasks = Todo.query.all()
#   return render_template('tasks.html', tasks=tasks)


@app.route('/todo', methods=['GET', 'POST'])
def todo():
  if request.method == 'POST':
    title = request.form['title']
    description = request.form['description']

    new_task = Todo(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

  tasks = Todo.query.all()
  return render_template('todo.html', tasks=tasks)


@app.route('/delete/<int:sno>')
def delete(sno):
  task = Todo.query.filter_by(sno=sno).first()
  db.session.delete(task)
  db.session.commit()

  return redirect('/todo')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
  if request.method == 'POST':

    task = Todo.query.filter_by(sno=sno).first()
    title = request.form['title']
    description = request.form['description']

    task.title = title
    task.description = description

    db.session.add(task)
    db.session.commit()
    return redirect('/todo')

  task = Todo.query.filter_by(sno=sno).first()
  return render_template('update.html', task=task)


if __name__ == '__main__':
  app.run(debug=True)
