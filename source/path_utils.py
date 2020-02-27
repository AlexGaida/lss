"""
path_utils.py : a module dealing with path and directory names and file checks.

"""
# import standard modules
import os
import posixpath
import glob


def find_files(file_path="", file_name=""):
    """
    organize the found files by using the glob module.
    :return: <tuple> list of found items.
    """
    if not file_path:
        extract_base_name_from_path(file_name)
    file_full_names = glob.glob(file_path + '/{}'.format(file_name))
    return tuple([extract_base_name_from_path(f) for f in file_full_names])


def glob_search(string_name=""):
    """
    Please think of this like a path to a file with a glob.
    It could be in the current directory if no path is specified.
    it could also be an explicit path with a globbed name if it starts with a slash,
    or a relative path if does not start with a slash, but has slashes in the interior (eg foo/bar/bla.%04d.exr)
    :param string_name: <str> name to search.
    :return: <list> files by name.
    """
    return glob.glob(string_name)


def get_this_upper_path():
    """
    get the upper parent directory.
    :return: <str> directory name from directory path.
    """
    return posixpath.dirname(get_this_directory_path())


def get_current_path():
    """
    get the current working path.
    :return: <str> the current working directory path.
    """
    return os.getcwd()


def get_this_directory_path():
    """
    get the path of the current file directory.
    :return: <str> directory path name.
    """
    return posixpath.dirname(posixpath.basename(__file__).replace('\\', '/'))


def extract_base_name_from_path(file_name=""):
    """
    extract the base name from the filename. (no extension name.)
    if input a path --> /path/to/dir/file.exe, result is file.exe
    :param file_name: <str> the file path to extract the base name.
    :return: <str> base name.
    """
    return os.path.basename(file_name)


def join_file_path(*args):
    """
    returns a new file path string through string concatenation.
    :param args: <list> array of strings to concatenate into one path name.
    :return: <str> file path name.
    """
    return posixpath.join(*args)


def log_filename():
    """
    get the file name for the log file.
    :return: <str> log file name.
    """
    return posixpath.join(get_this_upper_path(), "logfile.log")


def get_directory_from_file_name(path_name=""):
    """
    return a directory path from the full filename path given.
    :param path_name: <str> the file path to check.
    :return: <str> path name, <str> dir name, <bool> False for failure.
    """
    if is_file(path_name):
        path_name = posixpath.normpath(path_name.replace('\\', '/'))
        return posixpath.dirname(path_name)
    elif is_dir(path_name):
        return path_name
    return False


def is_file(path_name=""):
    """
    check if the incoming filepath is a file name.
    :param path_name: <str> the file path to check.
    :return: <bool> True for success. <bool> False for failure.
    """
    return os.path.isfile(path_name)


def is_dir(path_name=""):
    """
    check if the incoming filepath is a directory name
    :param path_name: <str> the file path to check.
    :return: <bool> True for success. <bool> False for failure.
    """
    return os.path.isdir(path_name)


def has_extension(file_name=""):
    """
    find out if the file name contains an extension.
    :param file_name: <str> the file name string to check.
    :return: <bool> True for success. <bool> False for failure.
    """
    return bool(os.path.splitext(file_name)[1])


def list_files_from_dir(dir_name="", sort_key=None):
    """
    lists all the files in a given directory name.
    Does not list file directories.
    :param dir_name: <str> the file path to check.
    :param sort_key: <str> sort by this string.
    :return: <tuple> list of files inside the directory.
    """
    return tuple(
        sorted(
            filter(
                lambda x: has_extension(x), os.listdir(dir_name)
            ),
            key=sort_key
        )
    )


def list_files_from_filepath(path_name=""):
    """
    if a full file path was given, list all the files inside the directory the file name lives in.
    :param path_name: <str> the file path name to check.
    :return: <tuple> list of files.
    """
    return list_files_from_dir(
        get_directory_from_file_name(
            path_name)
    )


def check_path_name(path_name=""):
    """
    checks if the incoming string parameter is file name or a directory or neither.
    :param path_name: <str> the file path to check.
    :return: <str> path name identifier.
    """
    if is_file(path_name):
        return 'filename'
    if is_dir(path_name):
        return 'directory'
    else:
        return ''
