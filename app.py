from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#database models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    #Adds new thing to list and attempts to append to database.
    if request.method == 'POST':
        thing_content = request.form['content']
        new_thing = Todo(content=thing_content)

        try:
            db.session.add(new_thing)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your thing'
#Displays list of things in database by date created.
    else:
        things = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', things=things)

@app.route('/delete/<int:id>')
def delete(id):
    thing_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(thing_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that thing'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    thing = Todo.query.get_or_404(id)

    if request.method == 'POST':
        thing.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the thing'

    else:
        return render_template('update.html', thing=thing)     


if __name__ == "__main__":
    app.run(debug=True)    

