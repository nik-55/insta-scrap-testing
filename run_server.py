"""
This file starts the server and open a database connection.
"""

from flask import Flask
from dotenv import load_dotenv
from os import getenv as os_getenv
from server.database.db import create_tables
from server.views.auth import auth
from server.views.posts import posts

# Configure the environment variables
load_dotenv(override=True)
SECRET_KEY = os_getenv("SECRET_KEY")

# Initialize the app
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello, this is Club Noticeboard Backend"


# Register the routes that are declared in other files
app.register_blueprint(auth)
app.register_blueprint(posts)

if __name__ == "__main__":
    # Create a database if it does not exist
    create_tables()
    # Start the server
    app.run()
