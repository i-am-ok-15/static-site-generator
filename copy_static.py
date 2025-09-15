import os
import shutil

destination = "./public copy/"
origin = "./static/"

def clean_destination_files(path):

    os.listdir(path=path)
    shutil.rmtree(path)

    os.mkdir(path=path)
    os.listdir(path=path)

clean_destination_files(destination)

def list_origin_files(path, destination):

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_origin_files(full_path, destination)
        else:
            shutil.copy(full_path, destination)


list_origin_files(origin, destination)