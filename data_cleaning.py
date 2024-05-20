"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project for the course `Développement d'Algorithmes pour des Applications Réticulaires`
~ of the Master's degree in Computer Science at Sorbonne University.
~
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


def clean(input_file_name='index_decoded.json', output_file_name='index_decoded_clean.json'):
    """
    Corrects the characters that failed to be decoded.

    Args:
        source_file_name (string): The name of input file containing the book titles to be clean.
    """

    output_file = open(output_file_name, 'w', encoding='utf-8')

    with open(input_file_name, 'r', encoding='utf-8') as input_file:
        
        line = input_file.readline()
        
        while line:
            if line.find('^') != -1 or line.find('΄') != -1 :
                line = line.replace('^e', 'ê')
                line = line.replace('a΄', 'á')
            line = line.replace("  ", ' ')
            line = line.replace('\\"', "'")
            line_without_last_character = line[:-1] 
            line_without_last_character.replace('\n', ' ')
            line = line_without_last_character + line[-1]
            output_file.write(line)
        
            line = input_file.readline()

    output_file.close()