"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project for the course `Développement d'Algorithmes pour des Applications Réticulaires`
~ of the Master's degree in Computer Science at Sorbonne University.
~ 
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """

# COLLECT THE UNICODE CHARACTERS

from base64 import encode

def collect_characters(input_file='index.json') -> set[str]:
    codes = set()
    with open(input_file) as f:
        line = f.readline()
        while line:
            position = line.find('\\u')
            if position != -1:
                str = line[position : position+6]
                codes.add(str)
            line = f.readline()
    return codes

# BUILD A DICTIONARY

dictionary = dict()
dictionary['\\u00eb'] = 'ë'
dictionary['\\u00df'] = 'ß'
dictionary['\\u0151'] = 'ő'
dictionary['\\u00f1'] = 'ñ'
dictionary['\\u011d'] = 'ĝ'
dictionary['\\u02b9'] = "'"
dictionary['\\u00e5'] = 'å'
dictionary['\\u00c3'] = 'Ã'
dictionary['\\u0302a'] = 'â' # accent circonflexe
dictionary['\\u0302e'] = 'ê'
dictionary['\\u0302o'] = 'ô'
dictionary['\\u0302u'] = 'û'
dictionary['\\u0302i'] = 'î'
dictionary['\\u0302'] = '^'
dictionary['\\u0302a'] = 'Â'
dictionary['\\u0302e'] = 'Ê'
dictionary['\\u0302o'] = 'Ô'
dictionary['\\u0302u'] = 'Û'
dictionary['\\u0302i'] = 'Î'
dictionary['\\u00ec'] = 'ì'
dictionary['\\u201c'] = '"'
dictionary['\\u201d'] = '"'
dictionary['\\u00e4'] = 'ä'
dictionary['\\u00c4'] = 'Ä'
dictionary['\\u00e6'] = 'æ'
dictionary['\\u00fc'] = 'ü'
dictionary['\\u00f3'] = 'ó'
dictionary['\\u00cd'] = 'Í'
dictionary['\\u00fa'] = 'ú'
dictionary['\\u00ef'] = 'ï'
dictionary['\\u00e0'] = 'à'
dictionary['\\u00c9'] = 'É'
dictionary['\\u00f6'] = 'ö'
dictionary['\\u00f8'] = 'ø'
dictionary['\\u00c1'] = 'Á'
dictionary['\\u0153'] = 'œ'
dictionary['\\u00f4'] = 'ô'
dictionary['\\u00f9'] = 'ù'
dictionary['\\u00c8'] = 'È'
dictionary['\\u00e9'] = 'é'
dictionary['\\ufffd'] = ' '
dictionary['\\u00c5'] = 'Å'
dictionary['\\u2013'] = '-'
dictionary['\\u00c0'] = 'À'
dictionary['\\u0301a'] = 'á' #acute accent
dictionary['\\u0301e'] = 'é'
dictionary['\\u0301o'] = 'ó'
dictionary['\\u0301u'] = 'ú'
dictionary['\\u0301i'] = 'í'
dictionary['\\u0301y'] = 'ý'
dictionary['\\u0301E'] = 'É'
dictionary['\\u0301'] = '΄'
dictionary['\\u016d'] = 'ŭ'
dictionary['\\u021a'] = 'Ț'
dictionary['\\u2014'] = '--'
dictionary['\\u00e1'] = 'á'
dictionary['\\u2019'] = "'"
dictionary['\\u00e8'] = 'è'
dictionary['\\u00ed'] = 'í'
dictionary['\\u00e2'] = 'â'
dictionary['\\u0152'] = 'Œ'
dictionary['\\u00ea'] = 'ê'
dictionary['\\u00e7'] = 'ç'
dictionary['\\u00bd'] = '½'
dictionary['\\u2019'] = "'"
dictionary['\\u00ee'] = 'î'
dictionary['\\u00ad'] = '-'
dictionary['\\u0306'] = ''
dictionary['\\u00d6'] = 'Ö'

def replace_characters(input_file='index.json', output_file='index_decoded.json'):
    """
    Encodes a file in utf-8.

    Args:
        input_file (string): The name of the input file.
        output_file (string): The name of the output file.
    """
    input = open(input_file, 'r', encoding='utf-8')
    with open(output_file, 'w', encoding='utf-8') as output:
        line = input.readline()
        while line:
            position = line.find('\\u')
            while position != -1:
                s = line[position : position+6]
                if s in ['\\u0301', '\\u0302'] and line[position : position+7] in dictionary.keys():
                    s = line[position : position+7]
                line = line.replace(s, dictionary[s])
                position = line.find('\\u')
            output.write(line)
            line = input.readline()
    input.close()