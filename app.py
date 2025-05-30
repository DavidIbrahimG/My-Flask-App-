from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy




### Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

## Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    

## Create the database and tables
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        new_task = User(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your task'
    else:
        tasks = User.query.order_by(User.date_created).all()
        return render_template('index.html', tasks=tasks)

## Delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting that task'
    
## Update task completion status
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = User.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.completed = 1 if request.form.get('completed') == 'on' else 0
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f'There was a problem updating that task: {e}'
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)