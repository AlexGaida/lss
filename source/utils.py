"""
Utility module for the inner workings of the lss.py module.

Because we do not know what and where the sequential numbers will increment at,
so we will need to sort the list according to the names that do not change.
so we need to check every string number in the file name to verify and to collect sequencing number information.

We then store this sequence information inside a dictionary.
Then we concatenate the dictionary data to nicely print the information according to these rules:

if non sequential incrementing files:
    <length_of_files> <file_name>
else:
    <length_of_files> <file_string_format_name>  <n0 - (n+1) - n != n+1>

Example:
    1 elem.info
    46 sd_fx29.%04d.rgb 101-121 123-147
    1 strange.xml

Goals:
    The code must work exactly as instructed: finding the count, sequences and formatting name of the files given.
    Find a way to re-use code wherever possible. Be efficient in the use of all code.
    Reformat and document it well, in a way so it is clear for all readers.

Important Information:
    This tool does not check the validity of the files. Like corrupted files, empty image sequences, etc.
    This tool does not check if there are multiple copies of identical contents of the files.
    This tool only checks for sequence increments of 1.
    This tool will not display folders inside the directory.

Versions:
    1.0.0: Initial release.
    1.0.1: Concatenate files by dictionary key index.
"""
# import standard modules
from pprint import pprint

# import local modules
import path_utils
import string_utils
import file_utils

# define private variables
__version__ = "1.0.1"
__verbosity__ = 0
__debugging__ = False

# define global variables
__PATH_NAME__ = ""


def verbose(*args):
    """
    prints only when __verbosity__ is True.
    :param args: <tuple>, <list>, <str> to print.
    :return: <bool> True for success.
    """
    if __verbosity__:
        print(args)
    return True


def check_list(array_files=()):
    """
    return a boolean on the length of the array_files parameter.
    :param array_files: <list> array of files.
    :return: <bool> the length of the array files.
    """
    return bool(len(array_files))


def flatten_list(*args):
    """
    flatten a list
    :param args:
    :return:
    """
    new_list = []
    for arg_l in list(args):
        new_list += arg_l
    return new_list


def next_file_name_by_index(files_array=(), index=0):
    """
    return the file name by the next index.
    :param files_array: <list> file array list.
    :param index: <int> index position,
    :return: <str> the next file in list.
    """
    length_of_files = len(files_array) - 1
    if (index + 1) <= length_of_files:
        return files_array[index + 1]
    else:
        return files_array[index]


def prev_file_name_by_index(files_array=(), index=0):
    """
    return the file name by the previous index.
    :param files_array: <list> file array list.
    :param index: <int> index position,
    :return: <str> the next file in list.
    """
    if index == 0:
        return files_array[index]
    else:
        return files_array[index - 1]


def format_name(file_name):
    """
    get the unique key name specified by the file name given.
    :param file_name: <str> file_name in question.
    :return: <str> unique key name.
    """
    return string_utils.replace_number_format_in_string(file_name, sequence_format=True)


def check_increment(number_1, number_2, increment_idx=0):
    """
    check if the increment adds up.
    :return: <bool> True the incrementing number matches. <bool> False the incrementing number no match.
    """
    incr_num = int(number_1) + increment_idx
    return incr_num == int(number_2)


def extract_file_name_information(file_name=""):
    """
    extract the string data from the file name given.
    :param file_name: <str> the file name to check from.
    :return: <tuple> file name information
    """
    return_data = {}
    ext_name = string_utils.extract_extension(file_name=file_name)
    numbers_in_name = string_utils.extract_numbers(file_name)
    letters_in_name = string_utils.extract_letters(file_name)
    number_indices = string_utils.extract_numbers_indices(file_name)

    # data return
    return_data['ext_in_name'] = ext_name
    return_data['base_name'] = file_name
    return_data['letters_in_name'] = letters_in_name
    return_data['numbers_in_name'] = numbers_in_name
    return_data['indices_in_name'] = number_indices
    return return_data


def compare_two_file_names(file_1, file_2, diff=False, same=False,
                           names=False, indices=False, ext=False,
                           length=False, numbers=False):
    """
    compares against two files.
    :param file_1: <str> the source file.
    :param file_2: <str> the comparing file.
    :param diff: <bool> the difference between the files names.
    :param same: <bool> the union between the two file names.
    :param names: <bool> compare file names. if the names match, return True.
    :param indices: <bool> compare file indices.
    :param numbers: <bool> compare file indices.
    :param ext: <bool> compare file extenstion names.
    :param length: <bool> compare file lengths.
    :return: <tuple> the difference.
    """
    file_1_name_data = extract_file_name_information(file_1)
    file_2_name_data = extract_file_name_information(file_2)
    file_1_ext = file_1_name_data["ext_in_name"]
    file_1_indices = file_1_name_data["indices_in_name"]
    file_1_numbers = file_1_name_data["numbers_in_name"]
    file_1_letters = file_1_name_data["letters_in_name"]

    file_2_ext = file_2_name_data["ext_in_name"]
    file_2_indices = file_2_name_data["indices_in_name"]
    file_2_numbers = file_2_name_data["numbers_in_name"]
    file_2_letters = file_2_name_data["letters_in_name"]

    if length:
        return len(file_1) == len(file_2)

    elif ext:
        return file_1_ext == file_2_ext

    elif names:
        return not bool(flatten_list(set(file_1_letters).symmetric_difference(set(file_2_letters))))

    elif indices:
        return file_1_indices == file_2_indices

    elif diff:
        file_numbers = set(file_1_numbers).symmetric_difference(set(file_2_numbers))
        file_letters = set(file_1_letters).symmetric_difference(set(file_2_letters))
        return flatten_list(file_numbers, file_letters)

    elif numbers:
        nums = flatten_list(set(file_2_numbers) - set(file_1_numbers))
        if not nums:
            nums = flatten_list(set(file_1_numbers) - set(file_2_numbers))
        return nums

    elif same:
        file_numbers = set(file_1_numbers) & set(file_2_numbers)
        file_letters = set(file_1_letters) & set(file_2_letters)
        return flatten_list(file_numbers, file_letters)
    return None


def name_strip(file_name, cur_file_indices, num_position):
    """
    strip the key name by the indices given.
    :param file_name: <str> file name.
    :param cur_file_indices: <tuple> number indices array. ((1, 3), (5, 6), (8, 9))
    :param num_position: <tuple> index position of the indices (0,)
    :return: <str> stripped file name.
    """
    return string_utils.strip_name_by_indices(
        string_name=file_name, number_indices=cur_file_indices, num_position=num_position)


def check_file_exists(file_name=""):
    """
    check if this file exists.
    :return: <bool> True for success. <bool> False for failure.
    """
    return path_utils.is_file(path_utils.join_file_path(get_directory_name(), file_name))


class PatternFinder:
    """
    find the patterns from the parameters given.
    """
    def __init__(self, files=(), file_name="", directory_name=""):
        """
        conditional initialization.
        if files are given, then scan through all files as-is.
        if file_name is given, then find all occurrences of this filename.
        if directory_name is given, then the list will be resorted, and then scanned afterwards.
        :param files: <list>, <tuple> loop through all these files and try to find patterns.
        :param file_name: <str> look only for this file_name in the current directory.
        :param directory_name: <str> sorts all files, then match patterns by scanning one ahead and one behind.
        """
        self.INCREMENT = 1
        self.LENGTH_OF_ALL_FILES = 0

        # the metadata information used for printing the final results
        self.FILES_METADATA = {}
        self.LOG_FILE = None

        if file_name:
            # glob search this file name
            files = self.get_files(file_name=file_name)

        elif not file_name and directory_name:
            # get a semi-sorted list from the directory given.
            files = self.get_files(directory_name=directory_name)

        self.LENGTH_OF_ALL_FILES = len(files)

        # sort and group that list nice-like according to the length of the file name
        sorted_files_dict = self.resort_files_by_key_name_pattern(files)
        # find breaks in the incrementation in between files
        updated_files_dict = self.get_relevant_files_info(sorted_files_dict)
        self.update_files_metadata(updated_files_dict)

    @staticmethod
    def _get_incrementing_indices(num_position=(), number_indices=()):
        """
        returns the incrementing number.
        :param num_position:
        :param number_indices:
        :return:
        """
        if len(num_position) > 1:
            raise IndexError("[FindIncrementingIndices] :: num_position parameter must only contain a single integer.")
        position = num_position[0]
        return number_indices[position]

    @staticmethod
    def get_increment_position(array_1, array_2):
        """
        match the number array and extract the difference of numbers.
        :param array_1: <tuple> an array of numbers to check
        :param array_2: <tuple> an array of numbers to check against array 1/
        :return: <str> the difference number
        """
        match_num = map(lambda x, y: x == y, array_1, array_2)
        return tuple([n for n in range(len(array_2)) if match_num[n] is False])

    def display_information(self, file_write=False):
        """
        displays the collection of FILES_METADATA dictionary class variable to the command prompt.
        :param file_write: <bool> saves it to the local file log.
        :return: <bool> True for success.
        """
        increment_tally = ""

        if file_write:
            self.LOG_FILE = file_utils.LogFile()
            self.LOG_FILE.write_file(string_line=get_path_name_variable() + '\n')
            self.LOG_FILE.write_file(string_line='{}\n'.format(self.length_of_all_files))

        if self.FILES_METADATA:
            if __verbosity__:
                print(
                    "\n"
                    "---------------------------------"
                    "\n"
                )

            print("\n")
            for key_name in self.FILES_METADATA:
                if 'files' in self.FILES_METADATA[key_name]:
                    pprint(self.FILES_METADATA[key_name]["files"])
                metadata_info = self.FILES_METADATA[key_name]["metadata"]
                sequence_count = metadata_info["count"]
                format_name = metadata_info["format_name"]
                if "increment_tally" in metadata_info:
                    increment_tally = ' '.join(
                        map(lambda x: '{}-{}'.format(x[0], x[1]), metadata_info["increment_tally"]))

                message = '{} {}\t{}'.format(sequence_count, format_name, increment_tally)
                print(message)

                if file_write:
                    self.LOG_FILE.write_file(string_line=message + '\n')

            if file_write:
                self.LOG_FILE.write_file(string_line='\n')

            print("\n")

            if __verbosity__:
                print("Length of all Files {}\n".format(self.length_of_all_files))
                print(
                    "\n"
                    "---------------------------------"
                    "\n"
                )
        else:
            message = (
                "\n"
                "There is nothing here."
                "\n"
            )

            print(message)

            if file_write:
                self.LOG_FILE.write_file(string_line=message + '\n')

        if file_write:
            self.LOG_FILE.close_file()

        return True

    def key_name(self, file_name="", files=(), index=0, strip=False, replace=False, fformat=False):
        """
        returns a nice key name.
        :param file_name: <str> file name.
        :param files: <str> file list to run the indexing against.
        :param strip: <bool> strips the name of the incrementing number.
        :param replace: <bool> replaces the name of the incrementing number with format
        :param: fformat <bool> replaces the name with the %d and %0d formatting
        :param index: <idx> the index to check within the file list.
        :return: <str> file name.
        """
        increment_data = self.find_incrementing_number_by_list_index(files, index)

        if increment_data:
            num_position = increment_data["num_position"]
            numbers_in_name = increment_data["numbers_in_name"]
            number_indeces = increment_data["file_indices"]
            if strip:
                return name_strip(file_name, number_indeces, num_position)
            if replace:
                return string_utils.sequence_string_format_replace(
                    file_name, numbers_in_name=numbers_in_name, number_indices=number_indeces, num_position=num_position
                )
            if fformat:
                return format_name(file_name)
        else:
            return file_name

    def resort_files_by_key_name_pattern(self, files=[]):
        """
        resorts the list so it nicely starts and ends with the file increments.
        I do not know how else to sort the list according to the various positions of incrementation of numbers in files.
        So We re-organize the list by finding the patterns in the file name.
        :param files: <list> the files to sort.
        Example:
            'V3-0002_comp_0001.jpg',
            'V3-0002_comp_<n+1>.jpg',
            'V3-0002_comp_0200.jpg',

            'V3-0002_comp_01.jpg',
            'V3-0002_comp_<n+1>.jpg',
            'V3-0002_comp_64.jpg'
        :return: <dict> properly sorted files. with metadata information.
        """
        key_number_list = map(lambda f_name: self.get_file_name_all_numbers(f_name), files)
        key_indices_list = map(lambda f_name: self.get_file_name_all_indices(f_name), files)
        idx = 0
        data = {}

        single_files = []

        # this files array object is not sorted, so let's find some semblance of order
        # we'll sort everything in compare_files_and_resort_dictionary function
        # files will be organized based on the current, previous and the next index of the files array.
        for key_indices, key_numbers, file_name in zip(key_indices_list, key_number_list, files):
            length_of_file = len(file_name)
            en_pos = None

            # finds relevant incrementing file data
            increment_data = self.find_incrementing_number_by_list_index(files, idx)

            idx += 1
            if increment_data:
                num_position = increment_data["num_position"]
                en_pos = key_indices[num_position[0]][1]
                key_name = string_utils.strip_name_by_indices(
                    string_name=file_name, number_indices=key_indices, num_position=num_position)
            else:
                key_name = file_name
                single_files.append(file_name)

            if key_name not in data:
                data[key_name] = {'files': [], 'metadata': {'sort_key': [],
                                                            'file_len': []}}

            if increment_data:
                if en_pos not in data[key_name]["metadata"]['sort_key']:
                    data[key_name]["metadata"]['sort_key'].append(en_pos)

                if length_of_file not in data[key_name]["metadata"]['file_len']:
                    data[key_name]["metadata"]['file_len'].append(length_of_file)

            if file_name not in data[key_name]["files"]:
                if file_name not in data[key_name]["files"]:
                    data[key_name]["files"].append(file_name)
        # end loop

        # create a beautifully sorted nested dictionary files.
        return self.compare_files_and_resort_dictionary(data, single_files)

    @staticmethod
    def compare_files_and_resort_dictionary(data, single_files=()):
        """
        compare files against the array in dictionary and sorts them.
        because a beautifully sorted list is totally awesome
        :param data: <dict> data dictionary.
        :param single_files: <tuple> single files with no sequencing metadata information.
        :return: <dict> a beautiful, beautiful dictionary of properly sorted lists.
        """
        # re-make the lists according to their respective lengths
        for k_name, v in data.items():
            file_length_dict = {}
            # if this organizer does not have a sorting key, skip it
            file_lengths = v['metadata']['file_len']

            for f_name in v['files']:
                if not file_lengths:
                    length_key = 0
                else:
                    length_key = file_lengths.index(len(f_name))
                if length_key not in file_length_dict:
                    file_length_dict[length_key] = []
                file_length_dict[length_key].append(f_name)

            # delete the old files list
            del(data[k_name]['files'])
            # update the new file dict
            data[k_name]['files'] = file_length_dict

        # append the single files into their respective groups
        if single_files:
            for single_file in single_files:
                for k_name, v_data in data.items():
                    for len_idx, v_files in v_data['files'].items():
                        if len(v_files) != 1:
                            name_comp = compare_two_file_names(single_file, v_files[0], names=True)
                            if not name_comp:
                                continue

                            index_comp = compare_two_file_names(single_file, v_files[0], indices=True)
                            if not index_comp:
                                continue

                            diff_comp = compare_two_file_names(single_file, v_files[0], diff=True)
                            if not len(diff_comp) <= 2:
                                continue

                            if single_file not in v_data['files'][len_idx]:
                                v_data['files'][len_idx].insert(0, single_file)
                                del(data[single_file])

        # now sort all files by the metadata sort_key
        for k_name, v in data.items():
            file_lengths = v['metadata']['file_len']
            # file_sorts = v['metadata']['sort_key']
            if not file_lengths:
                continue
            for len_id in range(len(file_lengths)):
                v['files'][len_id].sort()
        return data

    def get_files(self, directory_name="", file_name=""):
        """
        get the files to loop over and check for patterns down the line.
        :return: <tuple> file names. <tuple> empty for failure.
        """
        files = ()
        if directory_name:
            files = path_utils.list_files_from_dir(directory_name)
            self.LENGTH_OF_ALL_FILES = len(files)

        if file_name:
            # find by using glob module
            base_name = path_utils.extract_base_name_from_path(file_name)
            dir_name = path_utils.get_directory_from_file_name(file_name)
            if not dir_name:
                dir_name = get_directory_name()
            file_format = string_utils.replace_number_format_in_string(base_name, regex_format=True)
            # use glob to find files.
            files = path_utils.find_files(dir_name, file_format)
        return files

    @property
    def length_of_all_files(self):
        """
        returns the length of all files.
        :return:
        """
        return self.LENGTH_OF_ALL_FILES

    def _find_prinf_format_in_files(self, files):
        """
        find the printf formatting in the files given.
        :param files: <list> scan through these files
        :return: <str> format name.
        """
        cur_file_name = files[-1]
        length_of_files = len(files)
        if length_of_files == 1:
            return cur_file_name
        prev_file_name = files[-2]
        cur_file_name_data = extract_file_name_information(cur_file_name)
        prev_file_name_data = extract_file_name_information(prev_file_name)
        cur_numbers_in_name = cur_file_name_data["numbers_in_name"]
        prev_numbers_in_name = prev_file_name_data["numbers_in_name"]
        num_position = self.get_increment_position(cur_numbers_in_name, prev_numbers_in_name)
        return self.get_formatted_name(cur_file_name, num_position)

    def _find_ranges_in_files(self, files):
        """
        find the incrementing patterns in this list.
        This function is for nicely sorted lists only.

        :param files: <list> search through these files
        :return: <dict>, file_indices, numbers_in_name, num_position, incrementing_number. <dict>, empty for no match.
        """
        return_data = []
        length_of_files = len(files)
        start_increment_num = ""
        reset_start_num = True

        if length_of_files == 1:
            return ""

        for idx, f_name in enumerate(files):
            prev_file_name = prev_file_name_by_index(files, idx)
            current_file_name = files[idx]
            next_file_name = next_file_name_by_index(files, idx)

            # find information on current file name
            cur_file_name_data = extract_file_name_information(current_file_name)
            cur_numbers_in_name = cur_file_name_data["numbers_in_name"]

            prev_file_name_data = extract_file_name_information(prev_file_name)
            prev_numbers_in_name = prev_file_name_data["numbers_in_name"]

            # find information on current file name
            next_file_name_data = extract_file_name_information(next_file_name)
            next_numbers_in_name = next_file_name_data["numbers_in_name"]

            # if reach the end of the line
            if idx == length_of_files - 1:
                incr_number = compare_two_file_names(current_file_name, prev_file_name, numbers=True)
                num_position = self.get_increment_position(cur_numbers_in_name, prev_numbers_in_name)
            else:
                incr_number = compare_two_file_names(current_file_name, next_file_name, numbers=True)
                num_position = self.get_increment_position(cur_numbers_in_name, next_numbers_in_name)

            # get current increment number
            cur_incrementing_number = cur_numbers_in_name[num_position[0]]

            # get the beginning of the increment
            if reset_start_num:
                start_increment_num = cur_incrementing_number
                reset_start_num = False

            # identify incrementing pattern
            check_incr = check_increment(cur_incrementing_number, incr_number[0], increment_idx=self.INCREMENT)
            if not check_incr:
                return_data.append((start_increment_num, cur_incrementing_number))
                reset_start_num = True
        return return_data

    def find_incrementing_number_by_list_index(self, files, idx):
        """
        find the incrementing number in an unsorted list index
        Sometimes this gets fucked because the original file array is not sorted right.

        Example:
            ['V3-0002_comp_0156.jpg',
            'image-0041.png'
            'V3-0002_comp_01.jpg'
            'V3-0002_comp_0002.jpg',
            'emptyfile.bmp',
            'V3-0002_comp_03.jpg',
            'V3-0002_comp_63.jpg',]
            Hard to scan correctly when this garbage gets through.
        :param idx: <int> to look in the files list.
        :return: <dict>, file_indices, numbers_in_name, num_position, incrementing_number. <dict>, empty for no match.
        """
        return_data = {}
        prev_file_name = prev_file_name_by_index(files, idx)
        current_file_name = files[idx]
        next_file_name = next_file_name_by_index(files, idx)

        cur_file_name_data = extract_file_name_information(current_file_name)
        cur_numbers_in_name = cur_file_name_data["numbers_in_name"]
        cur_file_indices = cur_file_name_data["indices_in_name"]

        next_file_name_data = extract_file_name_information(next_file_name)
        next_numbers_in_name = next_file_name_data["numbers_in_name"]

        prev_file_name_data = extract_file_name_information(prev_file_name)
        prev_numbers_in_name = prev_file_name_data["numbers_in_name"]

        # proceed only if the current file name has numbers
        if cur_numbers_in_name:
            num_position = ()

            # if reached at the end of the line
            if idx == self.length_of_all_files - 1 and cur_numbers_in_name == next_numbers_in_name:
                num_position = self.get_increment_position(cur_numbers_in_name, prev_numbers_in_name)

            # else if the length of the current numbers compares against the length of the next number in list
            elif len(cur_numbers_in_name) == len(next_numbers_in_name):
                num_position = self.get_increment_position(cur_numbers_in_name, next_numbers_in_name)

            # else if check if the previous numbers compares against the current numbers
            elif cur_numbers_in_name == prev_numbers_in_name:
                num_position = self.get_increment_position(cur_numbers_in_name, prev_numbers_in_name)

            # else if reached the end of the increment of the file, so compare against the previous number
            elif len(cur_numbers_in_name) == len(prev_numbers_in_name):
                num_position = self.get_increment_position(cur_numbers_in_name, prev_numbers_in_name)

            # else designate as invalid sequentially numbered file,
            # however, if an invalid numbered file is at the beginning of the list, this will pass through
            else:
                return False

            # so we need to declare this num_position variable check
            if not num_position:
                return False

            # hoo boy so there is more than one incrementing number, so let's validate some names
            if len(num_position) > 1:
                # compare against both the previous and the next file name to find that one magic number
                prev_position = self.get_increment_position(cur_numbers_in_name, prev_numbers_in_name)
                next_position = self.get_increment_position(cur_numbers_in_name, next_numbers_in_name)
                if len(prev_position) == 1:
                    num_position = prev_position
                elif len(next_position) == 1:
                    num_position = next_position

            prev_key_name = name_strip(prev_file_name, cur_file_indices, num_position)
            cur_key_name = name_strip(current_file_name, cur_file_indices, num_position)
            next_key_name = name_strip(next_file_name, cur_file_indices, num_position)

            if cur_key_name == next_key_name and len(cur_numbers_in_name) == len(next_numbers_in_name):
                # get data from next_key
                cur_incrementing_number = cur_numbers_in_name[num_position[0]]
                return_data['file_indices'] = cur_file_indices
                return_data['numbers_in_name'] = cur_numbers_in_name
                return_data['prev_file_name'] = prev_file_name
                return_data['next_file_name'] = next_file_name

                return_data['num_position'] = num_position
                return_data['incrementing_number'] = cur_incrementing_number
                return return_data

            elif cur_key_name == prev_key_name and len(cur_numbers_in_name) == len(prev_numbers_in_name):
                # get data from previous key
                cur_incrementing_number = cur_numbers_in_name[num_position[0]]
                return_data['file_indices'] = cur_file_indices
                return_data['numbers_in_name'] = cur_numbers_in_name
                return_data['prev_file_name'] = prev_file_name
                return_data['next_file_name'] = current_file_name

                return_data['num_position'] = num_position
                return_data['incrementing_number'] = cur_incrementing_number
                return return_data
        # else designate the file in question as not incrementable
        return False

    @staticmethod
    def get_formatted_name(file_name, num_position):
        """
        return a formatted name.
        :param file_name: <str> the string name in question.
        :param num_position: <tuple> change the string at this position.
        :return: <str> the formatted name.
        """
        if not num_position:
            return file_name

        file_name_data = extract_file_name_information(file_name)
        numbers_in_name = file_name_data["numbers_in_name"]
        number_indices = file_name_data["indices_in_name"]

        return string_utils.sequence_string_format_replace(
            file_name, numbers_in_name, number_indices, num_position)

    @staticmethod
    def get_file_name_all_numbers(file_name):
        """
        get the key name based on the static number and letters of the file in question.
        :param file_name: <str> the file name in question.
        :return: <str> key name.
        """
        cur_file_name_data = extract_file_name_information(file_name)
        cur_numbers = cur_file_name_data["numbers_in_name"]
        return cur_numbers

    @staticmethod
    def get_file_name_all_indices(file_name):
        """
        get the key name based on the static number and letters of the file in question.
        :param file_name: <str> the file name in question.
        :return: <str> key name.
        """
        cur_file_name_data = extract_file_name_information(file_name)
        cur_indices = cur_file_name_data["indices_in_name"]
        return cur_indices

    def _get_incrementing_number_from_filename(self, file_name="", number_position=()):
        """
        return the incrementing number based on the number position.
        :param file_name: <str> file name to extract the numbers from.
        :param number_position: <tuple> singe integer unit to extract the number from.
        :return: <str> numbers.
        """
        file_name_data = extract_file_name_information(file_name)
        numbers_in_name = file_name_data["numbers_in_name"]
        return self._find_incrementing_number_from_numbers(numbers_in_name, number_position)

    @staticmethod
    def _find_incrementing_number_from_numbers(numbers_in_name, num_position):
        """
        finds the incrementing number. We do not know which number is incremented unless we check for imaginary files.
        :param numbers_in_name: <tuple> all numbers in file name.
        :param num_position: <tuple> single number of incrementing position.
        :return: <str> the incrementing number. <bool> False for failure.
        """
        if not num_position:
            return False
        position = num_position[0]
        return numbers_in_name[position]

    def update_files_metadata(self, data={}):
        """
        update the class metadata
        :param data: <dict> information to update the files metadata with.
        :return: <bool> True for success.
        """
        if __verbosity__ > 1:
            self.FILES_METADATA.update(data)

        else:
            for k_name, v_data in data.items():
                if k_name not in self.FILES_METADATA:
                    self.FILES_METADATA[k_name] = {}
                self.FILES_METADATA[k_name]["metadata"] = v_data['metadata']
        return True

    def get_relevant_files_info(self, sorted_files_dict={}):
        """
        finds incrementing patterns in the files
        :param sorted_files_dict: <list> the files to find increment patterns in.
        :return: <data> increment patterns.
        """
        for k_name, v_data in sorted_files_dict.items():
            files = []
            # dictionary items are not sorted, so we sort the integer keys here.
            file_indices = sorted(v_data['files'])
            for f_index in file_indices:
                files.extend(v_data['files'][f_index])

            # find the formatted name in files
            printf_format = self._find_prinf_format_in_files(files)
            sorted_files_dict[k_name]["metadata"].update({"format_name": printf_format})

            # find pattern in ranges in files
            ranges = self._find_ranges_in_files(files)
            sorted_files_dict[k_name]["metadata"].update({"increment_tally": ranges})
            sorted_files_dict[k_name]["metadata"].update({"count": len(files)})
        return sorted_files_dict


def update_path_name_variable(path_name=""):
    """
    updates the __PATH_NAME__ global variable.
    :param path_name: <str>
    :return: <bool> True for success.
    """
    global __PATH_NAME__
    __PATH_NAME__ = path_name
    return True


def get_path_name_variable():
    """
    returns the global path name variable
    :return: <str> path name.
    """
    global __PATH_NAME__
    return __PATH_NAME__


def get_directory_name():
    """
    get the directory name from the path name global variable.
    :return: <str> the directory name.
    """
    return path_utils.get_directory_from_file_name(get_path_name_variable())


def do_it(glob_search="", path_name=""):
    """
    Perform the directory parse.
    :param path_name: <str> path name to parse from.
    :param glob_search: <str> search string into the glob function.
    :return: <bool> True for success. <bool> False for failure.
    """
    current_path = path_utils.get_current_path()

    if not glob_search and not path_name:
        # if the lss arguments are empty, the path name is the current directory
        update_path_name_variable(current_path)
        # glob_search = current_path + '\*'
        path_name = current_path

    if path_name:
        update_path_name_variable(path_name)
        path_check = path_utils.check_path_name(path_name)
        verbose("[DoIt] :: PathName: {}, {}".format(path_name, path_check))
        if not path_check:
            raise IOError("[DoIt] :: Incorrect path given. path_name: {}".format(path_name))
        if path_check == 'directory':
            pf = PatternFinder(directory_name=path_name)
            pf.display_information(file_write=__debugging__)
            return True

        if path_check == 'filename':
            pf = PatternFinder(file_name=path_name)
            pf.display_information(file_write=__debugging__)
            return True

    else:
        if not glob_search:
            glob_search = current_path

        files = path_utils.glob_search(glob_search)
        files = map(path_utils.extract_base_name_from_path, files)
        pf = PatternFinder(files=files)
        pf.display_information(file_write=__debugging__)
        return True
    return False
