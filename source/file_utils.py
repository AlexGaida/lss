"""
file_utils.py modules for all file handling related objects.
"""

# import standard modules
import os

# import local modules
import path_utils


def delete_logfile():
    """
    deletes the log file.
    :return: <bool> True for success.
    """
    log_file = path_utils.log_filename()
    if path_utils.is_file(log_file):
        return os.remove(log_file)
    return True


def open_logfile_obj():
    """
    opens a file log object.
    :return: <fileObj>
    """
    f_obj = open(path_utils.log_filename(), 'a+')
    return f_obj


def close_logfile_obj(f_obj=None):
    """
    closes the file log object.
    :param f_obj: <fileObj> file object variable.
    :return: <fileObj>
    """
    f_obj.close()
    return f_obj


def write_logfile_obj(f_obj, string_line=""):
    """
    write the strings to a file.
    :param f_obj: <fileObj> file object variable.
    :param string_line: <str> the string line to write to the file.
    :return: <bool> True for success.
    """
    f_obj.write(string_line)
    return True


class LogFile:
    """
    a handy class object to deal with files opening, writing and closing.
    """
    def __init__(self):
        self.file_obj = open_logfile_obj()

    def write_file(self, string_line=""):
        """
        write the line to the file object.
        :param string_line: <str> the message to write.
        :return: <None>
        """
        write_logfile_obj(self.file_obj, string_line)

    def close_file(self):
        """
        close the opened file object.
        :return: <None>
        """
        close_logfile_obj(self.file_obj)

    @staticmethod
    def delete_file():
        """
        deletes the log file.
        :return: <None>
        """
        delete_logfile()

    @property
    def is_active(self):
        """
        returns True if the file is not closed. False is the file is closed.
        :return: <bool>
        """
        return not self.file_obj.closed

    @property
    def is_closed(self):
        """
        returns True if the file is closed. False if the file is not closed.
        :return: <bool>
        """
        return self.file_obj.closed

    def __del__(self):
        self.close_file()
        # print("[LogFile] :: is closed: {}".format(self.is_closed))
