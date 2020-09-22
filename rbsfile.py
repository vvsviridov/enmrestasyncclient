def bs_list(filename):
    with open(filename, "r") as f:
        for line in f.readlines():
            yield line.strip()
