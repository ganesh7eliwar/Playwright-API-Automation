import inspect, logging


class Loggen:
    @staticmethod
    # def log_generator():
    #     log_name = inspect.stack()[1][3]
    #     logger = logging.getLogger(log_name)
    #     log_file = logging.FileHandler(f'./logs/simple_grocery_store_logs.log', encoding="utf-8")
    #     log_format = logging.Formatter(
    #         "%(asctime)s | %(levelname)s | %(funcName)s | %(lineno)s | %(message)s")
    #     log_file.setFormatter(log_format)
    #     logger.addHandler(log_file)
    #     logger.setLevel(logging.INFO)
    #     return logger

    # def log_generator():
    #     log_name = inspect.stack()[1][3]
    #     logger = logging.getLogger(log_name)
    #     log_file = logging.FileHandler(f'./logs/simple_grocery_store_logs.log', encoding="utf-8")
    #     log_format = logging.Formatter(
    #         "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(lineno)s | %(message)s")
    #     log_file.setFormatter(log_format)
    #     logger.addHandler(log_file)
    #     logger.setLevel(logging.DEBUG)
    #     return logger

    def log_generator():
        log_name = inspect.stack()[1][3]
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.INFO)

        # ⭐ IMPORTANT: Prevent adding handlers multiple times
        if not logger.handlers:
            log_file = logging.FileHandler(f'./logs/simple_grocery_store_logs.log', encoding="utf-8")
            log_format = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(funcName)s | %(lineno)s | %(message)s"
            )
            log_file.setFormatter(log_format)
            logger.addHandler(log_file)

        return logger
