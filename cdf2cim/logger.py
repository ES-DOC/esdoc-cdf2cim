# -*- coding: utf-8 -*-
"""
.. module:: utils.logger.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Logging utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime as dt



# Set of logging levels.
LOG_LEVEL_DEBUG = 'DUBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'
LOG_LEVEL_FATAL = 'FATAL'
LOG_LEVEL_SECURITY = 'SECURITY'

# Module logging name.
_MODULE = "CDF2CIM"

# Text to display when passed a null message.
_NULL_MSG = "-------------------------------------------------------------------------------"


def log(msg=None, level=LOG_LEVEL_INFO):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str module: Module emitting log message (e.g. MQ).
    :param str level: Message level (e.g. INFO).

    """
    print(_get_formatted_message(msg, level))


def log_warning(msg):
    """Logs a warning event.

    :param str msg: A log message.
    :param str level: Message level (e.g. INFO).

    """
    log(msg, LOG_LEVEL_WARNING)


def log_error(err):
    """Logs a runtime error.

    :param Exception err: Error to be written to log.
    :param str module: Module emitting log message (e.g. DB).

    """
    msg = "!! RUNTIME ERROR !! :: "
    if issubclass(BaseException, err.__class__):
        msg += "{} :: ".format(err.__class__)
    msg += "{}".format(err)
    log(msg, LOG_LEVEL_ERROR)


def _get_formatted_message(msg, level):
    """Returns a message formatted for logging.

    """
    if msg is None:
        return _NULL_MSG

    return "{} [{}] :: ES-DOC > {} :: {}".format(
        unicode(dt.datetime.utcnow())[0:19],
        level,
        _MODULE,
        unicode(msg).strip()
        )
