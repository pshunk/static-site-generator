import os
import shutil
from textnode import TextNode, TextType

SOURCE_DIRECTORY = "./static"
DESTINATION_DIRECTORY = "./public"

def main() -> None:
    print("copying files")
    copy_files()
    return

def copy_files() -> None:
    abs_source_dir = os.path.abspath(SOURCE_DIRECTORY)
    abs_target_dir = os.path.abspath(DESTINATION_DIRECTORY)
    if not os.path.isdir(abs_source_dir):
        raise Exception("Error: source directory does not exist")
    if not os.path.isdir(abs_target_dir):
        raise Exception("Error: target directory does not exist")
    shutil.rmtree(abs_target_dir)
    os.mkdir(abs_target_dir)
        

main()