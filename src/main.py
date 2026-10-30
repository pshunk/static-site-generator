import os
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from functions import markdown_to_html_node

SOURCE_DIRECTORY = "./static"
DESTINATION_DIRECTORY = "./public"
CONTENT_DIRECTORY = "./content"
TEMPLATE = "./template.html"

def main() -> None:
    copy_files()
    generate_pages_recursive(os.path.abspath(CONTENT_DIRECTORY), os.path.abspath(TEMPLATE), os.path.abspath(DESTINATION_DIRECTORY))
    return

def copy_files() -> None:
    abs_source_dir = os.path.abspath(SOURCE_DIRECTORY)
    abs_target_dir = os.path.abspath(DESTINATION_DIRECTORY)
    if not os.path.isdir(abs_source_dir):
        raise Exception("Error: source directory does not exist")
    if not os.path.isdir(abs_target_dir):
        raise Exception("Error: target directory does not exist")
    try:
        shutil.rmtree(abs_target_dir)
        shutil.copytree(abs_source_dir, abs_target_dir)
    except Exception as e:
        print (f"Error: {e}")

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Error: markdown does not have an h1 header")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        markdown_file = open(from_path)
        markdown: str = markdown_file.read()
        markdown_file.close()
        template_file = open(template_path)
        template: str = template_file.read()
        template_file.close()
        node: HTMLNode = markdown_to_html_node(markdown)
        html: str = node.to_html()
        title: str = extract_title(markdown)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, mode="x") as file:
            file.write(template)
    except Exception as e:
        print(f"Error: {e}")

def generate_pages_recursive(content_dir_path: str, template_path: str, dest_dir_path: str) -> None:
    for file in os.listdir(content_dir_path):
        filepath = os.path.join(content_dir_path, file)
        if os.path.isfile(filepath) and file.endswith(".md"):
            file = file[:-2] + "html"
            generate_page(filepath, template_path, os.path.join(dest_dir_path, file))
        elif os.path.isdir(filepath):
            generate_pages_recursive(filepath, template_path, os.path.join(dest_dir_path, file))

main()