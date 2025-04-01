from textnode import TextNode, TextType
def main():
    tn = TextNode("*Bold*", TextType.LINK, "https://www.charlot.dev")
    print(tn)

main()
