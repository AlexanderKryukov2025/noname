from inspect import currentframe
from os.path import basename

from loguru import logger

LOG_LEVEL = 'INFO'


def autolog(message, level=LOG_LEVEL):
    """Autolog in format [time][level][module][function:line] : <message>

    :param message: message for logging
    :param level: log level
    """
    level = dict(
        trace='TRACE',
        debug='DEBUG',
        info='INFO',
        success='SUCCESS',
        warning='WARNING',
        error='ERROR',
        critical='CRITICAL'
    ).get(level.lower(), None)

    if not level:
        raise Exception('Set log level: trace, debug, info, success, warn, error, critical.')

    func = currentframe().f_back.f_code
    msg_format = '[{module}][{function}:{line}] : {msg}'
    logger.log(level, msg_format.format(module=basename(func.co_filename),
                                        function=func.co_name,
                                        line=func.co_firstlineno,
                                        msg=message))
