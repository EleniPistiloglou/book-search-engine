"""
This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
in Computer Science at Sorbonne University.

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~ Script for document counting ~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~
~ Author: Eleni Pistiloglou
~
~
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """

c=0
with  open("index.json", 'r') as f:
    line = f.readline()
    while line:
        if line[0] == '{':
            c += 1
        line = f.readline()

print(c)

# result : 2832