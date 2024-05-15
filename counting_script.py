"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
~ in Computer Science at Sorbonne University.
~
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


def count_documents(input_file_name='index.json'):
    """
    Counts the number of json objects contained in a list.

    Args: 
        input_file_name (string): The name of the file containing the list of objects.
    """

    nbr_of_docs = 0

    with open(input_file_name, 'r') as f:
        line = f.readline()
        while line:
            if line[0] == '{':
                nbr_of_docs += 1
            line = f.readline()

    print(input_file_name + " contains " + nbr_of_docs + " documents.")