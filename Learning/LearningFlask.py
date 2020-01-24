import json

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


class archives(db.Model):
    __tablename__ = 'archives'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    article = db.Column(db.String(1000))
    timestamp = db.Column(db.String(40))

    def __init__(self, author, article, timestamp):
        self.author = author
        self.article = article
        self.timestamp = timestamp

# Data visuals

class departments_data(db.Model):
    __tablename__ = 'departments'
    name = db.Column(db.String(50), primary_key=True)
    workforce = db.Column(db.Integer)
    lateness = db.Column(db.Integer)
    sickness = db.Column(db.Integer)
    accidents = db.Column(db.Integer)

    def __init__(self, name, workforce, lateness, sickness, accidents):
        self.name = name
        self.workforce = workforce
        self.lateness = lateness
        self.sickness = sickness
        self.accidents = accidents

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

@app.route('/departmens', methods=['POST', 'GET'])
def departments():
    if session['username']:
        db_object = workers.query.get(session['username'])
        if 'Admin' in db_object.Position:
            departments_object = departments_data.query.all()
            departments_list = []
            for department in departments_object:
                department_dict = {}
                department_dict['name'] = department.name
                department_dict['workforce'] = department.workforce
                department_dict['lateness'] = department.lateness
                department_dict['sickness'] = department.sickness
                department_dict['accidents'] = department.accidents
                departments_list.append((department_dict))
            departments_prepared = json.dumps(departments_list)
            return render_template('departments.html', name=session['username'], departments_object=departments_object
                                   , departments_prepared=departments_prepared)
        else:
            flash('No permission. Please log-in.')
            return redirect(url_for('index.html'))
    else:
        flash('Something went wrong. Please log-in.')
        return redirect(url_for('index.html'))

@app.route('/add_department', methods=['POST', 'GET'])
def add_departments():
    if request.method == 'POST':
        department_name = request.form["name"]
        department_workforce = request.form["workforce"]
        department_lateness = request.form["lateness"]
        department_sickness = request.form["sickness"]
        department_accidents = request.form["accidents"]
        new_department = departments_data(name=department_name, workforce=department_workforce, lateness=department_lateness, sickness=department_sickness, accidents=department_accidents)
        try:
            db.session.add(new_department)
            db.session.commit()
            departments_object = departments_data.query.all()
            return redirect(url_for('departments', name=session['username'], departments_object=departments_object))
        except Exception as e:
            print(e)
            return "Oops, something went wrong"
    else:
        return "Oops, something went wrong"


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
    new_archive = archives(author=article.author, article=article.article, timestamp=article.timestamp)
    db.session.add(new_archive)
    db.session.commit()
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('verify', name=session['username']))

if __name__ == '__main__':
    db.create_all()
    app.run('127.0.0.1', 8333, debug=True)