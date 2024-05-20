"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project for the course `Développement d'Algorithmes pour des Applications Réticulaires`
~ of the Master's degree in Computer Science at Sorbonne University.
~
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """

import json


def create_index(input_file_name='unprocessed_index.txt', output_file_name='index.json'):
    """
    Converts a text file containing the Gutenberg index retrieved from https://www.gutenberg.org/dirs/GUTINDEX.2021
    into json format and stores it in a file.

    A book from the index can later be retrieved from the Gutenberg website 
    by concatenating the book's id to the address https://www.gutenberg.org/ebooks/ .
    The page containing the book in plain text format is 
    https://www.gutenberg.org/cache/epub/`book_id`/pg`book_id`.txt . 
    
    Args:
        input_file_name (string): The text file containing the gutenberg index.
        output_file_name (string): The name of the output file.
    """
    
    output_file = open(output_file_name, 'w', encoding='utf-8')

    with open(input_file_name, 'r', encoding='utf-8') as input_file:

        line = input_file.readline()

        while line:

            if line[0] == '~' or line[0] == '#' or line[0:5] == 'TITLE' or len(line) < 2:
                line = input_file.readline()

            else:
                object = dict()

                language = 'English'  # default language
                id = line[-6:-1]
                object['id'] = id

                line = line[:-6].split(', by ') # splitting title from authors
                while len(line) == 1:
                    # the title can comprise multiple lines
                    line = line[0] + input_file.readline()
                    line = line.split('by ')

                title = line[0].replace('  ', '')
                if title[-1] == '\n' : title = title[:-1]
                if title[-1] == ' ' : title = title[:-1]
                if title[-1] == ',' : title = title[:-1]
                object['title'] = title

                authors = line[1].replace('  ', '')
                if authors[-1] == '\n' : authors = authors[:-1]
                if authors[-1] == ' ' : authors = authors[:-1]
                object['authors'] = authors

                line = input_file.readline()
                if line[2:10] == 'Subtitle':
                    subtitle = line[12:]
                    while line[-2] != ']':
                        # the subtitle can comprise multiple lines
                        line = input_file.readline()
                        subtitle += line
                    subtitle = subtitle.replace('\n', '')[:-1]
                    if subtitle[-1] == ' ' : subtitle = subtitle[:-1]
                    if subtitle[-1] == ',' : subtitle = subtitle[:-1]
                    object['subtitle'] = subtitle

                    line = input_file.readline()

                if line[3:13] == 'Illustrator':
                    # skip illustrator
                    line = input_file.readline()

                if line[2:10] == 'Language':
                    language = line[12:-2]
                    line = input_file.readline()

                elif len(line) > 1:
                    # the authors take two rows
                    authors += line
                    authors = authors.replace("  ", '')
                    if authors[-1] == '\n' : authors = authors[:-1]
                    object['authors'] = authors
                    line = input_file.readline()

                    if line[2:10] == 'Subtitle':
                        subtitle = line[12:]
                        while line[-2] != ']':
                            line = input_file.readline()
                            subtitle += line
                        subtitle = subtitle.replace('\n', '')[:-1]
                        if subtitle[-1] == ' ' : subtitle = subtitle[:-1]
                        if subtitle[-1] == ',' : subtitle = subtitle[:-1]
                        object['subtitle'] = subtitle
                        line = input_file.readline()

                    if line[3:13] == 'Illustrator':
                        line = input_file.readline()

                    if line[2:10] == 'Language':
                        language = line[12:-2]
                        line = input_file.readline()

                object['language'] = language 
                output_file.write(json.dumps(object, indent=4))
                output_file.write(', \n')

    output_file.close()
