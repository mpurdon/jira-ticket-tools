import argparse
import os

from jira import JIRA


class BC:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


LEVEL_SUCCESS = 2.9
LEVEL_DEBUG = 3
LEVEL_WARN = 2
LEVEL_INFO = 1
LEVEL_ERROR = 0


def debug_print(message, level=LEVEL_DEBUG):
    return print(f'{message}')

    # if level > args.verbosity:
    #     return None
    #
    # if level == LEVEL_DEBUG:
    #     return print(f'{message}')
    #
    # if level == LEVEL_SUCCESS and LEVEL_DEBUG == args.verbosity:
    #     return print(f'{BC.OKGREEN}{message}{BC.ENDC}')
    #
    # if level == LEVEL_WARN:
    #     return print(f'{BC.WARNING}{message}{BC.ENDC}')
    #
    # if level == LEVEL_INFO:
    #     return print(f'{BC.OKBLUE}{message}{BC.ENDC}')
    #
    # if level == LEVEL_ERROR:
    #     return print(f'{BC.ERROR}{message}{BC.ENDC}')


JIRA_OPTIONS = {
    'server': os.getenv('jira_base_url', 'https://athletesperformance.atlassian.net'),
}


def get_argparser(description=None):
    """
    Construct an argument parser with common options

    """
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('-v', '--verbose',
                           dest='verbosity',
                           action='count',
                           default=0,
                           help='increases log verbosity for each occurrence.')
    argparser.add_argument('user',
                           help='The JIRA username to log in as')
    argparser.add_argument('--password',
                           default=None,
                           help='The JIRA password to log in with')

    return argparser


def connect(args, **kwargs):
    """
    Connect to the JIRA server

    """
    options = JIRA_OPTIONS
    options.update(**kwargs)

    attempt = 1
    while attempt < 3:
        password = args.password or input('Password:')
        options['auth'] = (args.user, password)
        try:
            return JIRA(**options)
        except RecursionError:
            print('Invalid password, try again.')

        attempt += 1

    debug_print('Could not connect to JIRA', level=LEVEL_ERROR)
    return None
