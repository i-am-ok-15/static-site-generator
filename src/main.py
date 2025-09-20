from textnode import TextNode, TextType
from copy_static import generate_public_directory
from config import PUBLIC_DIR, STATIC_DIR

def main():
    text_1 = TextNode("anchor text", TextType.LINK, "www.google.com")
    print(text_1)
    generate_public_directory(STATIC_DIR, PUBLIC_DIR)

main()