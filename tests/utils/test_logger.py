from tinycrawler.utils import Logger


def setup()->Logger:
    path = "logs/testing_logger.log"
    return Logger(path)


def test_logger():
    logger = setup()
    logger.info("Imma be testing info.")
    logger.warning("Imma be testing warning.")
    logger.error("Imma be testing error.")
    logger.critical("Imma be testing error.")
