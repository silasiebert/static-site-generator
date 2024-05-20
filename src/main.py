from os.path import isfile
from textnode import TextNode
import os
import shutil


def main():
    dummy = TextNode("This is a textnode", "bold", "www.boot.dev")
    print(dummy)
    copy_directory("./static", "./public")


def copy_directory(source_directory, target_directory):
    shutil.rmtree(target_directory)
    os.mkdir(target_directory)
    # Validate paths
    if not os.path.exists(source_directory):
        raise Exception("Invalid source directory")
    if not os.path.exists(target_directory):
        raise Exception("Invalid target directory")
    # List files in source dir
    source_files = os.listdir(source_directory)
    for entry in source_files:
        current_path = os.path.join(source_directory, entry)
        target_path = os.path.join(target_directory, entry)
        print(f"Current directory: {current_path}")
        if os.path.isfile(current_path):
            # copy to target dir
            print(f"I'm a file: {current_path}")
            shutil.copy(current_path, target_path)
        else:
            os.mkdir(target_path)
            copy_directory(current_path, target_path)


main()
