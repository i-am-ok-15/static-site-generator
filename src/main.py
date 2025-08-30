from textnode import TextNode


def main():
    text_1 = TextNode("anchor text", "text type", "some url")
    print(f"TextNode({text_1.text}, {text_1.text_type}, {text_1.url})")
main()