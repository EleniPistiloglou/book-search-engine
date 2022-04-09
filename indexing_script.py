"""
This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
in Computer Science at Sorbonne University.

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~ Script for index creation ~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~
~ Author: Eleni Pistiloglou
~
~ Search instructions: A book from the index can later be retrieved from the Gutenberg website 
~                      by concatenating the book's id to the address https://www.gutenberg.org/ebooks/ .
~                      The page containing the book in plain text format is 
~                      https://www.gutenberg.org/cache/epub/`book_id`/pg`book_id`.txt . 
~
~
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """

import json


rf = open("index.json", 'w', encoding="utf-8")  # destination file

with open("unprocessed_index.txt", 'r', encoding="utf-8") as f:  # source file retrieved from https://www.gutenberg.org/dirs/GUTINDEX.2021
    line = f.readline()

    while line:
        if line[0]=='~' or line[0]=='#' or line[0:5]=="TITLE" or len(line)<2:
            line = f.readline()

        else:
            object = dict()
            language = "English"  # default language
            id = line[-6:-1]
            print(id)
            object["id"] = id

            line = line[:-6].split(", by ") # splitting title from authors
            while len(line)==1:
                line = line[0] + f.readline()
                line = line.split("by ")
            title = line[0].replace("  ", "")
            if title[-1]=="\n" : title = title[:-1]
            if title[-1]==" " : title = title[:-1]
            if title[-1]=="," : title = title[:-1]
            print(title)
            object["title"] = title

            authors = line[1].replace("  ", "")
            if authors[-1] == "\n" : authors = authors[:-1]
            if authors[-1] == " " : authors = authors[:-1]
            print(authors)
            object["authors"] = authors

            line = f.readline()
            if line[2:10] == "Subtitle":
                subtitle = line[12:]
                while line[-2]!="]" :
                    line = f.readline()
                    subtitle += line
                subtitle = subtitle.replace('\n', '')[:-1]
                if subtitle[-1]==" " : subtitle = subtitle[:-1]
                if subtitle[-1]=="," : subtitle = subtitle[:-1]
                print(subtitle)
                object["subtitle"] = subtitle
                line = f.readline()
            if line[3:13] == "llustrator":
                line = f.readline()
            if line[2:10] == "Language":
                language = line[12:-2]
                print(language)
                line = f.readline()

            elif len(line)>1:
                # the authors take two rows
                authors += line
                authors = authors.replace("  ", "")
                if authors[-1] == "\n" : authors = authors[:-1]
                print(authors)
                object["authors"] = authors
                line = f.readline()

                if line[2:10] == "Subtitle":
                    subtitle = line[12:]
                    while line[-2]!="]" :
                        line = f.readline()
                        subtitle += line
                    subtitle = subtitle.replace('\n', '')[:-1]
                    if subtitle[-1]==" " : subtitle = subtitle[:-1]
                    if subtitle[-1]=="," : subtitle = subtitle[:-1]
                    print(subtitle)
                    object["subtitle"] = subtitle
                    line = f.readline()
                if line[3:13] == "llustrator":
                    line = f.readline()
                if line[2:10] == "Language":
                    language = line[12:-2]
                    print(language)
                    line = f.readline()

            object["language"] = language 
            rf.write(json.dumps(object, indent=4))
            rf.write(', \n')

        print()

rf.close()
