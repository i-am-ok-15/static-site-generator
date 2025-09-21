from config import CONTENT, TEMPLATE
from converters import markdown_to_html_node

def extract_title(markdown):
    markdown_elements = markdown.split("\n")

    for element in markdown_elements:
        if element.startswith("# "):
            return element.strip("# ")

def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    markdown = open(from_path, "r").read()

    template = open(template_path, "r").read()

    html_nodes = markdown_to_html_node(markdown)

    html_string = html_nodes.to_html()

    title = extract_title(markdown)

    new_template = template.replace(r"{{ Title }}", title)
    new_template = new_template.replace(r"{{ Content }}", html_string)

    with open(dest_path, "w") as generated_page:
        generated_page.write(new_template)