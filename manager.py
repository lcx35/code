from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import app, db
#from app import app
import sys

sys.path.append("/data/www/code/")

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

#manager.add_command("runserver", Server('0.0.0.0', port=5000))
#manager.add_command("runserver", Server('0.0.0.0', port=8080))
#manager.add_command("createall", Server('0.0.0.0', port=8080))

@manager.command
def createall():
    from app.models_sql import User
    from werkzeug.security import generate_password_hash

    db.create_all()

    password_hash = generate_password_hash("123456")
    admin = User(id=1, username="admin", password=password_hash, master="admin")
    db.session.add(admin)
    db.session.commit()

@manager.command
def dropall():
    db.drop_all()

if __name__ == "__main__":
    manager.run()
#	app.run(host='0.0.0.0', debug=True, port=8080, threaded=True)
