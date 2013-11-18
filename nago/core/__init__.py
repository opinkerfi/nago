
import time

# List of log entries since program start. Format should be:
# [{'timestamp':x, 'level': x, 'message'}]
_log_entries = []


def log(message, level="info"):
    """ Add a new log entry to the nago log.

    Arguments:
        level - Arbritrary string, levels should be syslog style (debug,log,info,warning,error)
        message - Arbritary string, the message that is to be logged.
    """
    now = time.time()
    entry = {}
    entry['level'] = level
    entry['message'] = message
    entry['timestamp'] = now
    _log_entries.append(entry)

    print("{level}: {message}".format(**locals()))
