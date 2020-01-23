from flask import Flask, render_template, flash, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:@localhost:5432/workers'
app.secret_key = 'SomethingHere'
db = SQLAlchemy(app)


class workers(db.Model):
    __tablename__ = 'workers'
    Name = db.Column(db.String(200), primary_key=True)
    Position = db.Column(db.String(200))
    Password = db.Column(db.String(200))

    def __init__(self, Name, Position, Password):
        self.position = Name
        self.name = Position
        self.password = Password


class articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    article = db.Column(db.String(1000))
    timestamp = db.Column(db.String(40))

    def __init__(self, author, article, timestamp):
        self.author = author
        self.article = article
        self.timestamp = timestamp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        data = request.form
        form_name = (data['name_value'])
        form_password = (data['password'])
        db_object = workers.query.get(form_name)
        article_objects = articles.query.all()
        if db_object:
            db_password = db_object.Password
            db_name = db_object.Name
            db_position = db_object.Position
            if form_name == db_name and form_password == db_password:
                if 'Admin' in db_position:
                    session['username'] = db_name
                    all_workers = workers.query.all()
                    return render_template('verify.html', name=db_name, all_workers=all_workers, article_objects=article_objects)
                else:
                    session['username'] = db_name
                    return render_template('regular.html', name=db_name, article_objects=article_objects)
            else:
                flash('Wrong username or password !')
                return render_template('index.html')
        else:
            return 'Oops, something went wrong !'
    elif session['username']:
         db_object = workers.query.get(session['username'])
         if 'Admin' in db_object.Position:
            article_objects = articles.query.all()
            all_workers = workers.query.all()
            return render_template('verify.html', name=session['username'], all_workers=all_workers, article_objects=article_objects)
         else:
             article_objects = articles.query.all()
             return render_template('regular.html', name=session['username'], article_objects=article_objects)
    else:
        return 'Oops, something went wrong'


@app.route('/add_article', methods=['POST', 'GET'])
def add_article():
    if request.method == 'POST':
        article_content = request.form["article"]
        new_article = articles(author=session['username'], article=article_content, timestamp=date.today())
        try:
            db.session.add(new_article)
            db.session.commit()
            return redirect(url_for('verify', name=session['username']))
        except Exception as e:
            print(e)
            return "Oops, something went wrong"

@app.route('/delete_article/<id>', methods=['DELETE', 'POST', 'GET'])
def delete_article(id):
    article = articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('verify', name=session['username']))

if __name__ == '__main__':
    db.create_all()
    app.run('127.0.0.1', 8333, debug=True)