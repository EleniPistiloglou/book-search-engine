dest = open('index_decoded_clean.json', 'w', encoding='utf-8')
with open("index_decoded.json", 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        if line.find('^') != -1 or line.find("΄") != -1 :
            print(line)
            line = line.replace('^e', 'ê')
            line = line.replace('a΄', 'á')
        line = line.replace("  ", " ")
        line = line.replace('\\"', "'")
        line1 = line[:-1] 
        line1.replace("\n", " ")
        line = line1 + line[-1]
        dest.write(line)
        line = f.readline()
dest.close()