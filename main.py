from flask import Flask
from waitress import serve

from blueprints.propunere_tehnica import propunere_tehnica_bp
from config.config import listening_host, listening_port
from services.integration.creatio_gateway_service import CreatioGatewayService
from services.integration.creatio_file_service import CreatioFileService

app = Flask(__name__)

gateway = CreatioGatewayService()
app.config['creatio_file_service'] = CreatioFileService(gateway)

app.register_blueprint(propunere_tehnica_bp)

if __name__ == '__main__':
    serve(app, host=listening_host, port=listening_port)
