from config.config import base_url
from services.integration.creatio_gateway_service import CreatioGatewayService


class CreatioService:
    def __init__(self, creatio_connection):
        self.connection: CreatioGatewayService = creatio_connection
