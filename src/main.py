from textnode import TextNode, TextType

def main():
    # 1. Create a new TextNode object with dummy values
    dummy_node = TextNode(
        text="This is a bold text node", 
        text_type=TextType.BOLD, 
        url=None
    )
    
    # 2. Print the object to verify the __repr__ method
    print(dummy_node)

# 3. Call the main function when the script runs
if __name__ == "__main__":
    main()