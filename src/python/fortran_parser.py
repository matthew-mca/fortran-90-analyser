def parse_file(file_path):
    with open(file_path, "r") as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()
