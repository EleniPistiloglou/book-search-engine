# OK
with open("logs\\sample_log_file.txt",'w') as f:
    for i in range(3):
        f.write(str(i) + "\n")