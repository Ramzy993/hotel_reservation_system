from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from src.common.config_manager import ConfigManager
from src.common.logger import LogHandler
from src.db_manager.db_driver import DBDriver
from src.web_app.api.v1.auth import auth_blueprint
from src.web_app.api.v1.rooms import room_blueprint
from src.web_app.api.v1.reservation import reservation_blueprint
from src.web_app.api.v1.users import user_blueprint

flask_app = Flask(import_name=__name__)

# TODO: better use flask restful

HOST = ConfigManager().get_str('FLASK_APP', 'host', fallback='localhost')
PORT = ConfigManager().get_int('FLASK_APP', 'port', fallback=8008)
DEBUG = ConfigManager().get_bool('FLASK_APP', 'debug', fallback=False)

SWAGGER_URL = '/swagger'
SWAGGER_FILE = "/static/swagger.json"
# TODO: find a way to separate swagger.json to multiple files

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_FILE,
    config={
        'app_name': "HRS API"
    }
)

logger = LogHandler().logger


def create_app():

    with flask_app.app_context():
        flask_app.config['SECRET_KEY'] = ConfigManager().get_str('FLASK_APP', 'app_secret')
        flask_app.config['ENV'] = ConfigManager().get_str('FLASK_APP', 'env')

        logger.info("Flask App created.")

    DBDriver()
    JWTManager(flask_app)

    flask_app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # API V1 Registration
    api_v1_base_url = '/api/v1'
    flask_app.register_blueprint(auth_blueprint, url_prefix=api_v1_base_url)
    flask_app.register_blueprint(room_blueprint, url_prefix=api_v1_base_url)
    flask_app.register_blueprint(reservation_blueprint, url_prefix=api_v1_base_url)
    flask_app.register_blueprint(user_blueprint, url_prefix=api_v1_base_url)


def start_app():

    create_app()

    flask_app.run(host='0.0.0.0', port=PORT, debug=DEBUG, use_reloader=True)
    logger.info(f"App is running on host name: {HOST}, port: {PORT}, with debug mode: {DEBUG}")


@flask_app.route('/health', methods=['GET'])
def health():
    return {'status': 'SUCCESS'}
