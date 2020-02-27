"""
unittest.py module is responsible for compiling test cases to run the tool against directories.

Goal:
    1. To make sure there are no errors are raised during the testing process.
    2. To make sure the tool has correct outputs.
    3. To write a log file to keep track of results.
"""

# import standard modules
import unittest

# import local modules
import path_utils
import utils
import file_utils

# define local variables
__directory_path__ = path_utils.get_this_upper_path()
utils.__debugging__ = True
utils.__verbosity__ = 1


class TestDirectories(unittest.TestCase):
    """
    Perform a battery of tests against the directories.
    """
    def test_sequence_00(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_00')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def test_sequence_01(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_01')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def test_sequence_02(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_02')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def test_sequence_03(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_03')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def test_sequence_04(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_04')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def test_sequence_06(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_06')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def raiseTest_sequence_invalid(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_99')
        self.assertRaises(IOError, utils.do_it(path_name=sequence_dir))


class TestFilenames(unittest.TestCase):
    """
    Perform a battery of tests against the files.
    """

    def test_filename_01(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_01', 'image-0023.png')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)

    def test_filename_06(self):
        sequence_dir = path_utils.join_file_path(__directory_path__, 'testdirectories', 'sequence_06', 'd.0003.png')
        self.assertEqual(utils.do_it(path_name=sequence_dir), True)


if __name__ == '__main__':
    file_utils.delete_logfile()
    unittest.main()

