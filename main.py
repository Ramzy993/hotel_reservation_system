from src.web_app.app import start_app
from src.common.logger import LogHandler


if __name__ == '__main__':
    LogHandler().logger.info("Welcome to Hotel Reservation System ....")
    start_app()
