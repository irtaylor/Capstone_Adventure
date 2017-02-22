#!/usr/bin/env python

# List of prepositions that will be parsed from user input
PREPOSITIONS = {'to', 'at', 'about', 'on', 'onto', 'above', 'into', 'around'}

# List of vowels that will determine article
VOWELS = {'a', 'e', 'i', 'o', 'u'}

# List of conjunctions that will be parsed from user input
CONJUNCTIONS = {'and'}

# List of proper nouns
PROPER_NOUNS = { 'jerry', 'rick', 'morty', 'beth', 'summer', 'tiny rick' }

# TODO: expand to also strip out articles of incoming strings
def check_for_prepositions(string):
    """
    Given a string input, strips the first preposition and returns the new string.
    :param string: String representing the user's input
    :return: A string that removes the first preposition from the given input
    """
    # If the first word in the string is a preposition
    if string.split()[0] in PREPOSITIONS:
        # Remove it
        string = string.split(' ')[1:]
        string = " ".join(string)
    return string

def check_if_vowel(string):
    """"
    Checks if first word starts with a vowel; this is to assist determining
    which article to use
    """
    if any ((vowel in VOWELS) for vowel in string[0]):
    #if string.startswith(for any in VOWELS):
        return True
    else:
        return False
        
def format_string_plurality(key, description):
    """
    Verify if string is plural or not to prepend the correct article,
    depending on whether the object being examined is an item or a feature
    Features use both fields, proper nouns and items only use the key, currently
    """
    if key in PROPER_NOUNS:
        return key
    if (description == None):
        if key.endswith('s') is True:
            return add_article(key, True)
        else:
            return add_article(key, False)
    if key.endswith('s'):
        return add_article(description, True)
    else:
        return add_article(description, False)


def add_article(string, plural):
    """
    Prepends appropriate article to a feature or item
    """
    # TODO: Fix pluraity with nouns which do not end with 's' and singular nouns that end with 's'
    if (plural == True) or (string.lower() == "money"):
        string = "some " + string
    else:
        if check_if_vowel(string) is True:
            string = "an " + string
        else if 
        else:
            string = "a " + string
    return string