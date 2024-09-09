cat = subprocess.Popen(["hadoop", "fs", "-cat", "/path/to/myfile"], stdout=subprocess.PIPE)
for line in cat.stdout:
    print line
