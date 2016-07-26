import os
from app import create_app, db
from app.models import User, Role,Permission,Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

 
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
 
 
def make_shell_context():
     return dict(app=app, db=db, User=User, Role=Role,Permission=Permission,Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)



     
@manager.command
def test_password():
     import unittest
     
     suite=unittest.TestLoader().discover('tests')
     unittest.TextTestRunner(verbosity=2).run(suite)
     '''
     suite = unittest.TestLoader().loadTestsFromTestCase(UserModelTestCase)
     unittest.TextTestRunner(verbosity=2).run(suite)
     '''
 

  
if __name__ == '__main__':
     manager.run()