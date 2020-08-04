import logging

logformatter = logging.Formatter(
    "-> [%(levelname)s] %(name)s::%(funcName)s() : %(message)s"
)
# unfortunately have to set the base logger format because pyABF sets it.
# That's why stuff is commented below
logging.basicConfig(
    level=logging.CRITICAL,
    format="-> [%(levelname)s] %(name)s::%(funcName)s() : %(message)s",
)


def make_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # console_log_handler = logging.StreamHandler()
    # console_log_handler.setLevel(logging.DEBUG)
    # console_log_handler.setFormatter(logformatter)
    # logger.addHandler(console_log_handler)
    curr_logs = [i for i in logging.Logger.manager.loggerDict.keys()]
    if "pyabf" in curr_logs:
        logging.getLogger("pyabf").setLevel(logging.CRITICAL)
    else:
        pass
    return logger
