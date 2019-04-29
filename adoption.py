import os
from forms import AddForm,DelForm,AddOwn
from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY']='mysecretkey'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Puppy(db.Model):
    __tablename__='puppies'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner',backref='Puppy',uselist=False)

    def __init__(self,name):
        self.name = name


    def __repr__(self):
        if self.owner:
            return("{} puppy has owner and owner name is {} ").format(self.name,self.owner.name)
        else:
            return("{} puppy has no owner ").format(self.name)

class Owner(db.Model):
    __tablename__='owner'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    puppy_id=db.Column(db.Integer,db.ForeignKey('puppies.id'))

    def __init__(self,name,puppy_id):
        self.name = name
        self.puppy_id = puppy_id
    def __repr__(self):
        return f"Owner name: (self.name)"









@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add',methods=['GET','POST'])
def add_pup():

    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data

        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('add.html',form=form)

@app.route('/list')
def list_pup():

    puppies = Puppy.query.all()
    return render_template('list.html',puppies=puppies)





@app.route('/delete',methods=['GET','POST'])
def del_pup():

    form = DelForm()
    if form.validate_on_submit():
        id = form.id.data

        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('delete.html',form=form)



@app.route('/owner',methods=['GET','POST'])
def owner():

    form=AddOwn()
    if form.validate_on_submit():
        name=form.name.data
        id = form.pup_id.data
        owner=Owner(name,id)
        db.session.add(owner)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('owner.html',form=form)



if __name__=='__main__':
    app.run(debug=True)
