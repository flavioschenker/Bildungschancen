import logging

logger = logging.getLogger("bildungschance")
logger.setLevel(logging.INFO)
log_format = logging.Formatter(
    fmt="%(asctime)s (%(levelname)s): %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
log_print = logging.StreamHandler()
log_print.setFormatter(log_format)
logger.addHandler(log_print)
