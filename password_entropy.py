# Author: Ian Docherty
# Description: The below functions take a password and evaluate it based on its
#              calculated information entropy. For randomly generated passwords,
#              the information bit entropy is calculated using the formula:
#              H = log2(N^L), where L is the password length and N is the number
#              of possible symbols to choose from. The bit entropy is one method
#              used to describe how many possible permutations a brute force attack
#              would need to explore to guess all possible passwords.

import math


# Possible characters options for PasswordVault generated passwords
UPPERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "1234567890"
SPECIALS = '@%+!$?~'


def get_entropy(password):
    """
    Calculates the information entropy in bits using the given information. An
    assumption is made that, if the password contains any one of the characters
    in the UPPERS, NUMBERS, and SPECIALS global variables, then any character in
    the given password has an equal probability of being any of the approved
    symbols. Approved symbols are lowercase letters and any symbol in the above
    global variables.
    :return: The bit value representing the password entropy
    """

    # Determine number of possible unique symbols present in the given password
    number_of_symbols = 26  # Base password only has 26 lowercase chars allowed

    # Check if any uppercase, numbers, or special chars exist in given password
    uppercase_found = False
    number_found = False
    special_found = False
    for char in password:

        if char in UPPERS and not uppercase_found:
            number_of_symbols += len(UPPERS)
            uppercase_found = True

        if char in NUMBERS and not number_found:
            number_of_symbols += len(NUMBERS)
            number_found = True

        if char in SPECIALS and not special_found:
            number_of_symbols += len(SPECIALS)

    bit_entropy = math.log((number_of_symbols ** len(password)), 2)
    return bit_entropy


def get_password_strength(bit_entropy):
    """
    Given an entropy bit value, returns a string describing the strength of
    the password used to generate the entropy value
    :param bit_entropy: The information entropy of a specific password
    :return: One of the following strings: Very Weak, Weak, Moderately Strong, Strong, Very Strong
    """
    if bit_entropy < 28:
        return "Very Weak"
    elif 28 <= bit_entropy <= 35:
        return "Weak"
    elif 36 <= bit_entropy <= 59:
        return "Moderately Strong"
    elif 60 <= bit_entropy <= 127:
        return "Strong"
    else:
        return "Very Strong"
