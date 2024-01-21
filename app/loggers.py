import logging
import os


def set_up_loggers():
    stream_log = logging.StreamHandler()

    access_logger = logging.getLogger("access")
    access_logger.setLevel(logging.INFO)
    access_file_handler = logging.FileHandler(
        os.path.join(os.getcwd(), "logs", "access.log")
    )
    access_logger.addHandler(access_file_handler)
    access_logger.addHandler(stream_log)

    basic_log_file = logging.FileHandler(
        os.path.join(os.getcwd(), "logs", "root_basic.log")
    )
    logging.basicConfig(
        handlers=(basic_log_file, stream_log),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

