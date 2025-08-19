from itertools import takewhile
from os import makedirs
from random import shuffle

from globals import *

"""Functions that are needed in almost every file.
   They have nothing in common but it's organized"""

def mix(array) -> list:
    """Returns a shuffled list without changing the original"""
    temp = array[:]
    shuffle(temp)
    return temp


def check_valid_input(*entries, include=None, exclude=()) -> bool:
    """Makes an entry red if invalid, else default grey
    :param exclude: input is valid if it doesn't contain values from here
    :param include: input is valid if it only contains values from here
    :returns: True if **all** inputs are valid, else False
    """
    is_valid = True
    for entry in entries:
        text = entry.get().strip()
        if text and text == ''.join(takewhile(lambda x: x not in exclude and (include is None or x in include), text)):
            entry.configure(fg_color="#353638", border_color='#555560')
        else:
            entry.configure(fg_color="darkred", border_color='red')
            entry.focus_set()
            is_valid = False
    return is_valid


def validate_testfile(test_path: str) -> None:
    """Removes empty lines and trailing spaces from file. Sorts the words alphabetically
        If user has manually written words in a (very) wrong format - we erase them."""
    text = get_text_from_file(test_path)
    for i in range(len(text) - 1, -1, -1):
        word_pair = text[i].split(' - ')
        if len(word_pair) != 2:
            text.pop(i)
            continue
        word_pair = [j.strip().capitalize() for j in word_pair]
        text[i] = f"{word_pair[0]} - {word_pair[1]}\n"

    with open(test_path, 'w', encoding=ENCODING) as file:
        for line in sorted(text):
            file.write(line)


def get_text_from_file(file_path: str) -> list[str]:
    text = open(file_path, 'r', encoding=ENCODING).readlines()
    return text


def check_oper_folder():
    makedirs(OPER_FOLDER, exist_ok=True)  # makes a folder if there wasn't already one
