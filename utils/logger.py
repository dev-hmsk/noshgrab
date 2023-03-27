#!/usr/bin/env
import logging
import time
import inspect
import logging.handlers
import traceback
import threading
import sys


############## USING LOGGER ################
''' To use pyLogger import logger like so:
    "from pyLogger import Log"
    Set Log level by adding this line:
    Log.setLoglvl('int level')
    Log to stdOut by changing stdOut to True:
    Log.setStdout(True)

    Log.CRITICAL(msg1, msg2)    --> >=50
    Log.ERROR(msg1, msg2)       --> >=40
    Log.WARNING(msg1, msg2)     --> >=30
    Log.INFO(msg1, msg2)        --> >=20
    Log.DATA(msg1, msg2)        --> >=15
    Log.DEBUG(msg1, msg2)       --> >=10
'''
############################################

class ThreadFilter(logging.Filter):
    def __init__(self, id):
        self.id = id

    def filter(self, record):
        return record.threadName == self.id

def datalog(self, message, *args, **kws):
    DEBUG_LEVELV_NUM = 15
    logging.addLevelName(DEBUG_LEVELV_NUM, 'DATALOG')
    
    if self.isEnabledFor(DEBUG_LEVELV_NUM):
        self._log(DEBUG_LEVELV_NUM, message, args, **kws)

class Log(object):

    _log_level = 60
    _trace_level = -3
    _single_trace = True
    _log_file = 'log.log'
    _data_log_file = 'log.log'
    
    logging.Logger.datalog = datalog
    _logger = logging.getLogger(__name__)
    _logger.propagate = False
    
    _data_logger = logging.getLogger('DATA')
    _data_logger.propagate = False
    _stdout = False

    _handler = logging.handlers.RotatingFileHandler(filename=_log_file, maxBytes=100000000, backupCount=2)
    _format = logging.Formatter('%(asctime)s \t[PID: %(process)s] [%(levelname)s] \t %(message)s')
    _error_format = logging.Formatter('%(asctime)s \t[PID: %(process)s] [%(levelname)s] \t %(message)s')
    _handler.setFormatter(_format)

    _data_handler = logging.handlers.RotatingFileHandler(filename=_data_log_file, maxBytes=100000000, backupCount=2)
    _data_handler.addFilter(ThreadFilter(threading.current_thread().name))
    _data_handler.setFormatter(_format)

    @classmethod
    def set_trace_level(cls, level, single_trace=False):
        cls._single_trace = single_trace
        if level ==  'full':
            cls._trace_level = 'full'
        elif level == 'last':
            cls._trace_level = -3
        else:
            cls._trace_level= 0 - level

    @classmethod
    def stdout(cls, bSet):
        if bSet:
            cls._stdout = True
            cls._handler = logging.StreamHandler(sys.stdout)
            cls._data_handler = logging.StreamHandler(sys.stdout)
        else:
            cls._stdout = False
            cls._handler = logging.handlers.RotatingFileHandler(filename=cls._log_file, maxBytes=100000000, backupCount=2)
            cls._data_handler = logging.handlers.RotatingFileHandler(filename=cls._data_log_file, maxBytes=100000000, backupCount=2)

        cls._handler.setFormatter(cls._format)
        cls._data_handler.setFormatter(cls._format)

    @staticmethod
    def format_trace(data):
        """Returns the current line number in our program."""
        data[2] = data[2].strip('  ').replace('in <module>', '').strip('\n')
        for i in range(len(data)):
            data[i] = data[i].strip(' ')
        return ': '.join(data)

    @classmethod
    def get_trace(cls, override=None):
        """Returns the current line number in our program."""
        trace_level = cls._trace_level
        if override:
            trace_level = 'full'
        frame = inspect.currentframe()
        stack_trace = traceback.format_stack(frame)
        nstack = []
        for trace in stack_trace:
            trace_data = trace.split(',')
            trace = cls.format_trace(trace_data)
            nstack.append(trace)
        if trace_level == 'full':
            return nstack[:-2]
        elif trace_level == 'None':
            return ''
        else:
            if cls._single_trace:
                return nstack[trace_level]
            else:
                return nstack[:trace_level]

    @classmethod
    def set_log_file(cls, _name):
        try:
            cls._handler = logging.handlers.RotatingFileHandler(filename=_name, maxBytes=100000000, backupCount=2)
            os.remove(cls._log_file)
            cls._log_file = _name
        except Exception as e:
            cls._handler = logging.handlers.RotatingFileHandler(filename=cls._log_file, maxBytes=100000000, backupCount=2)
            Log.WARNING('Error setting Log file: ', e)
        cls._handler.setFormatter(cls._format)

    @classmethod
    def set_data_log_file(cls, _name):
        try:
            cls._data_handler = logging.handlers.RotatingFileHandler(filename=_name, maxBytes=100000000, backupCount=2)
            os.remove(cls._data_log_file)
            cls._data_log_file = _name
        except Exception as e:
            cls._data_handler = logging.handlers.RotatingFileHandler(filename=cls._log_file, maxBytes=100000000, backupCount=2)
            Log.WARNING('Error setting Log file: ', e)
        cls._data_handler.setFormatter(cls._format)

    @classmethod
    def log_level(cls, _lvl):
        cls._log_level = _lvl
        cls._handler.setLevel(_lvl)
        cls._data_handler.setLevel(_lvl)
        cls._data_logger.setLevel(_lvl)
        cls._logger.setLevel(_lvl)

    @classmethod
    def INFO(cls, msg1, msg2=''):
        cls._handler.setFormatter(cls._format)
        cls._logger.addHandler(cls._handler)
        cls._logger.info('%s %s \t%s', msg1, msg2, cls.get_trace())
        cls._logger.removeHandler(cls._handler)

    @classmethod
    def DEBUG(cls, msg1, msg2=''):
        cls._handler.setFormatter(cls._format)
        cls._logger.addHandler(cls._handler)
        cls._logger.debug('%s %s \t%s', msg1, msg2, cls.get_trace(True))
        cls._logger.removeHandler(cls._handler)

    @classmethod
    def ERROR(cls, msg1, msg2=''):
        cls._handler.setFormatter(cls._error_format)
        cls._logger.addHandler(cls._handler)
        cls._logger.error('%s %s \t%s', msg1, msg2, cls.get_trace())
        cls._logger.removeHandler(cls._handler)

    @classmethod
    def WARNING(cls, msg1, msg2=''):
        cls._handler.setFormatter(cls._error_format)
        cls._logger.addHandler(cls._handler)
        cls._logger.warning('%s %s \t%s', msg1, msg2, cls.get_trace())
        cls._logger.removeHandler(cls._handler)

    @classmethod
    def CRITICAL(cls, msg1, msg2=''):
        cls._handler.setFormatter(cls._format)
        cls._logger.addHandler(cls._handler)
        cls._logger.critical('%s %s \t%s', msg1, msg2, cls.get_trace())
        cls._logger.removeHandler(cls._handler)

    @classmethod
    def DATA(cls, msg1, msg2=''):
        cls._data_handler.setFormatter(cls._format)
        cls._data_logger.addHandler(cls._data_handler)
        cls._data_logger.datalog('%s %s', msg1, msg2)
        cls._data_logger.removeHandler(cls._data_handler)
