from textnode import TextNode, TextType


def main():
    text_1 = TextNode("anchor text", TextType.LINK, "www.google.com")
    print(text_1)
main()