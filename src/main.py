from textnode import TextNode, TextType
from copy_static import generate_public_directory
from config import PUBLIC_DIR, STATIC_DIR, CONTENT, TEMPLATE
from generators import generate_page

def main():
    text_1 = TextNode("anchor text", TextType.LINK, "www.google.com")
    print(text_1)
    generate_public_directory(STATIC_DIR, PUBLIC_DIR)
    generate_page(CONTENT, TEMPLATE, "public/index.html")

main()