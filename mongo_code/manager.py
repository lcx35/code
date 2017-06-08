#from flask_script import Manager, Server
from app import app
import sys

sys.path.append("/data/www/code/")

#manager = Manager(app)
#manager.add_command("runserver", Server('0.0.0.0', port=5000))
#manager.add_command("runserver", Server('0.0.0.0', port=8080))



if __name__ == "__main__":
#	manager.run()
	app.run(host='0.0.0.0', debug=True, port=8080, threaded=True)
