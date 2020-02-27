"""
The lss command tool command interface.
"""
# import standard modules
import os
import argparse

# import local modules
import utils

# define global variables
PATH = os.getcwd()
VERBOSITY = 0


def argument_parse():
    """
    parse through incoming file names.
    :return: <tuple> incoming file name.
    """
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('filename', metavar='FILENAME', type=str, nargs="?",
                        help='glob file name search.')
    parser.add_argument('-p', dest='path', metavar="PATH", action="store",
                        help='Optionally specify a directory or a file path.')
    parser.add_argument('-v', dest='verbosity', metavar="VERBOSITY", action="store", default=0,
                        help='Specify verbosity. Options: 0, 1, 2.')
    return parser.parse_args()


def main():
    """
    the main function call.
    :return: <bool> True for success. <bool> False for failure.
    """
    args = argument_parse()
    utils.__verbosity__ = args.verbosity
    utils.do_it(glob_search=args.filename, path_name=args.path)
    return True

if __name__ == "__main__":
    main()
