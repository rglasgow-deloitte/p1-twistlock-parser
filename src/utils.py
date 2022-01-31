import os
def read_files(directory):
    """
    This function will read the files in the directory.
    """
    files = []
    for file in os.listdir(directory):
        files.append(file)
    return files