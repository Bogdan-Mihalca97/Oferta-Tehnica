from flask import Flask
from waitress import serve

from blueprints.propunere_tehnica import propunere_tehnica_bp
from config.config import listening_host, listening_port

app = Flask(__name__)
app.register_blueprint(propunere_tehnica_bp)

if __name__ == '__main__':
    serve(app, host=listening_host, port=listening_port)
