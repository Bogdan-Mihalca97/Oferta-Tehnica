"""
Centralized configuration loader.
Reads config/config.json once at import time and exposes values as module-level variables.
"""
import os
import json

_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

with open(_config_path, 'r', encoding='utf-8') as _f:
    _cfg = json.load(_f)

anthropic_api_key = _cfg["anthropicApiKey"]
creatio_base_url = _cfg["creatioBaseUrl"]
creatio_auth_secret = _cfg["creatioAuthSecret"]
listening_host = _cfg["listeningHost"]
listening_port = _cfg["listeningPort"]
