from tinycrawler.utils import Logger


def test_logger():
    path = "logs/testing_logger.log"
    logger = Logger(path)
    logger.info("Imma be testing info.")
    logger.warning("Imma be testing warning.")
    logger.error("Imma be testing error.")
