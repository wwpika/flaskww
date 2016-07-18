from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import os
from flask_sqlalchemy import SQLAlchemy

#hello
basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']=\
		'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=true

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
db=SQLAlchemy(app)

class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users=db.relationship('User',backref='role',lazy='dynamic')
	
	def _repr_(self):
		return '<Role %r>' %self.name
	
class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=Ture,index=True)
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
	
	def __repr__(self):
		return '<User %r>' %self.username

class NameForm(Form):
	name=StringField('what is your name?',validators=[Required()])
	submit=SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
   return render_template('500.html'), 500

@app.route('/',methods=['GET','POST'])
def index():

	form=NameForm()
	if form.validate_on_submit():
		old_name=session.get('name')
		if old_name is not None and old_name!=form.name.data:
			flash('Looks like you have changed your name!')
		session['name']=form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'))
	


if __name__=='__main__':
	db.create_all()
	manager.run()
	