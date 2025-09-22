import os
from config import CONTENT, TEMPLATE
from converters import markdown_to_html_node

def extract_title(markdown):
    markdown_elements = markdown.split("\n")

    for element in markdown_elements:
        if element.startswith("# "):
            return element.strip("# ")

def generate_page(from_path, template_path, dest_path, basepath):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()

    html_nodes = markdown_to_html_node(markdown)
    html_string = html_nodes.to_html()

    title = extract_title(markdown)

    new_template = template.replace(r"{{ Title }}", title)
    new_template = new_template.replace(r"{{ Content }}", html_string)
    new_template = new_template.replace("href\"/", f"href=\"{basepath}")
    new_template = new_template.replace("src\"/", f"src=\"{basepath}")

    with open(dest_path, "w") as generated_page:
        generated_page.write(new_template)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):

    elements = os.listdir(dir_path_content)

    for entry in elements:
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            destination_path = os.path.join(dest_dir_path, entry)
            os.mkdir(destination_path)
            generate_pages_recursively(entry_path, template_path, destination_path, basepath)
        else:
            if entry.endswith(".md"):
                html_entry = entry.rstrip(".md")
                html_entry = f"{html_entry}.html"
                content_path = os.path.join(dir_path_content, entry)
                destination_path = os.path.join(dest_dir_path, html_entry)
                generate_page(content_path, template_path, destination_path, basepath)
