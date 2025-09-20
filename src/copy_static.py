import os
import shutil

def clean_destination_files(path):

    os.listdir(path=path)
    shutil.rmtree(path)

    os.mkdir(path=path)
    os.listdir(path=path)


def generate_public_directory(origin, destination):

    clean_destination_files(destination)

    elements = os.listdir(origin)

    for entry in elements:
        entry_path = os.path.join(origin, entry)
        if os.path.isdir(entry_path):
            destination_path = os.path.join(destination, entry)
            os.mkdir(destination_path)
            generate_public_directory(entry_path, destination_path)
        else:
            shutil.copy(entry_path, destination)
