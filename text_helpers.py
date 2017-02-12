#!/usr/bin/env python

TEXT_PATH = "data/text/"

def get_text(file_name):
    file_path = TEXT_PATH + file_name
    with open(file_path, "r") as inFile:
        text = inFile.read().splitlines()
        for line in text:
            print line
        print

def get_intro():
    get_text("intro.txt")

def get_ending(ending_type):
    """
        Takes in the name of the desired ending (e.g. "plumbus" or "death"),
        and runs the corresponding ending.
    """
    ending_file_name = "ending_" + ending_type + ".txt"
    get_text(ending_file_name)
