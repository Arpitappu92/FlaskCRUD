# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class AddForm(FlaskForm):

    name = StringField('Name of Puppy: ')
    submit = SubmitField('Add Puppy')

class DelForm(FlaskForm):

    id = IntegerField("Id no. of Puppy to Remove: ")
    submit = SubmitField("Remove Puppy")

class AddOwn(FlaskForm):
    pup_id = IntegerField("Id no. of Puppy to add to owner: ")
    name = StringField('Name of Owner: ')
    submit = SubmitField('Add Owner')
