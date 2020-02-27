"""
string_utils.py: dealing with string operations, slicing string objects.
"""
# import standard modules
import re
import os

# define local variables
re_digits = re.compile("\d+")           # get all digits
re_letters = re.compile("[A-Za-z]+")    # get all letters
re_split = re.compile(r"([0-9]+)")      # split everything by numbers
re_zeroes = re.compile("^0+")           # find all leading zeroes


def concatenate_data(*args):
    """
    concatenated any incoming data into one string, regardless of data type.
    :return: <str> concatenated data.
    """
    concat_str = ""
    for arg in args:
        if isinstance(arg, (list, tuple)):
            concat_str += '_'.join(arg)
        elif isinstance(arg, (str, unicode)):
            concat_str += '_' + arg
        elif isinstance(arg, (int, float)):
            concat_str += '_' + str(arg)
        else:
            concat_str += '_' + arg
    return concat_str


def replace_number_format_in_string(file_name="", sequence_format=False, regex_format=False):
    """
    replaces all numbers in the string by a string format.
    :param file_name: <str> the string to change into any numbers into string formats.
    :param sequence_format: <bool> if true, the numbers will be replaced by C style printf format.
    :param regex_format: <bool> if True, the numbers will be replaced by regex-style [0-9] format
    :return: <str> formatted string.
    """
    numbers_in_name = extract_numbers(file_name)
    if sequence_format:
        formatted_numbers = map(sequence_string, numbers_in_name)
    if regex_format:
        formatted_numbers = map(regex_number_string, numbers_in_name)
    split_name = split_numbered_strings(file_name)
    # replace all the numbers into a string format
    new_file_name = ""
    num_count = 0
    for s_pl in split_name:
        # check if the string is an integer and replace it with the selected format string.
        try:
            int(s_pl)
            new_file_name += formatted_numbers[num_count]
            num_count += 1
        except ValueError:
            new_file_name += s_pl
    return new_file_name


def split_numbered_strings(name=""):
    """
    split all numbers and names.
    :param name: <str> the name to perform splitting operation.
    :return: <tuple> split items.
    """
    return re_split.split(name)


def extract_extension(file_name=""):
    """
    extract the extension name from the filename.
    :param file_name: <str> the file path to extract the extension name.
    :return: <str> extension name.
    """
    return os.path.splitext(file_name)[-1]


def split_file_extension(file_name=""):
    """
    extract the base name from the filename. (no extension name.)
    :param file_name: <str> the file path to extract the base name.
    :return:
    """
    return os.path.splitext(file_name)[0]


def extract_numbers(file_name=""):
    """
    extracts all numbers from the filename.
    :param file_name: the file name to iterate the regex from.
    :return: <tuple> the numbers as string objects from the file name.
    """
    return tuple(re_digits.findall(file_name))


def extract_letters(file_name=""):
    """
    extracts all numbers from the filename.
    :param file_name: the file name to iterate the regex from.
    :return: <tuple> the numbers as string objects from the file name.
    """
    return tuple(re_letters.findall(file_name))


def extract_numbers_indices(file_name=""):
    """
    find not only the numbers, but their respective indices too.
    :param file_name: the file name to iterate the regex from.
    :return: <tuple> the numbers as string objects from the file name.
    """
    return tuple([(m.start(0), m.end(0)) for m in re_digits.finditer(file_name)])


def replace_str_by_index(text, start_position=0, end_position=1, replacement=''):
    """
    replace a string object by the index number for slicing.
    :param text: <str> original text.
    :param start_position: <int> start index to replace string from.
    :param end_position: <int> end index to replace string from.
    :param replacement: <str> replacement text.
    :return: <str> modified string.
    """
    return '{}{}{}'.format(text[:start_position], replacement, text[end_position:])


def regex_number_string(snumber=""):
    """
    replace the incomig string numbers with the regex style numbers.
    :param snumber: <str> the incoming numbers to change.
    :return: <str> [0-9] regex style formatting.
    """
    return "[0-9]" * len(snumber)


def sequence_string(snumber=""):
    """
    count the length of the incoming zeroes from the string number in question.
    :param snumber: <str> the incoming numbers to change.
    :return: <str> printf formatting.
    """
    all_zeroes = re_zeroes.findall(snumber)
    length_of_digits = len(snumber)
    number_of_zeroes = 0

    if all_zeroes:
        number_of_zeroes = len(all_zeroes[0])

    if number_of_zeroes:
        return "%0{}d".format(length_of_digits)

    else:
        return "%d"


def verify_sequence_string(strnum="", number=0):
    """
    reconstruct string formatting.
    :param strnum: <str> the string object to check.
    :param number: <int> the number to check.
    :return: <str> numbers.
    """
    return sequence_string(strnum) % number


def increment_number(number_string="", increment_int=1):
    """
    increment the string number by the incrementing integer.
    :param number_string: <str> the number string to increment from.
    :param increment_int: <int> increment by this number.
    :return: <str> incremented number.
    """
    padding_num = len(number_string)
    return str(int(number_string) + increment_int).zfill(padding_num)


def sequence_string_format_replace(base_name="", numbers_in_name=(), number_indices=(), num_position=()):
    """
    return a new base name from the parameter instructions given.
    :param base_name: <str> the base name to change.
    :param numbers_in_name: <tuple>, <list> array of numbers found in the base name.
    :param number_indices: <tuple>, <list> array of where the sequencing number is found in the base name.
    :param num_position: <tuple>, <list> single array item to determine where the format should be placed.
    :return: <str> new formatted string name.
    """
    if not num_position:
        raise IndexError("[FileSequenceStringReplace] :: num_position parameter is empty!")

    position = num_position[0]
    index_of_number = number_indices[position]

    formatted_number_string = sequence_string(numbers_in_name[position])
    return replace_str_by_index(base_name, index_of_number[0], index_of_number[1], formatted_number_string)


def strip_name_by_indices(string_name="", number_indices=(), num_position=()):
    """
    strip the name by the indices.
    :param string_name: <str>
    :param number_indices: <tuple>
    :param num_position: <tuple>
    :return: <str> replaced string.
    """
    position = num_position[0]
    index_of_number = number_indices[position]
    return replace_str_by_index(string_name, index_of_number[0], index_of_number[1], "")
