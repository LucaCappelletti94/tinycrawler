from tinycrawler.utils import Logger


def logger_setup()->Logger:
    path = "logs/testing_logger.log"
    return Logger(path)


def test_logger():
    logger = logger_setup()
    logger.info("Imma be testing info.")
    logger.warning("Imma be testing warning.")
    logger.error("Imma be testing error.")
    logger.critical("Imma be testing error.")
