from flask_app import app
from flask_app.controllers import users, shows


if __name__=='__main__':
    app.run(debug=bool(os.environ.get("DEBUG_STATUS")))