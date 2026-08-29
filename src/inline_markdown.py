import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        parts = old_node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: delimiter '{delimiter}' was not closed in text: '{old_node.text}'")
            
        for i in range(len(parts)):
            if parts[i] == "":
                continue
                
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
                
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r'(?<!!)\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        images = extract_markdown_images(current_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
            
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            sections = current_text.split(image_markdown, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            current_text = sections[1]
            
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        links = extract_markdown_links(current_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for anchor_text, link_url in links:
            link_markdown = f"[{anchor_text}]({link_url})"
            sections = current_text.split(link_markdown, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))
            current_text = sections[1]
            
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    # Start by tracking the entire input string as a plain TEXT block
    nodes = [TextNode(text, TextType.TEXT)]
    
    # 1. Split by multi-character syntax first (Bold)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # 2. Split by single-character typography (Italic & Code)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # 3. Pull out the image and link blocks last
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes


# --- Combined Test/Example Verification Execution Block ---
if __name__ == "__main__":
    # Define a complex sample node to verify parsing
    sample_node = TextNode(
        "This is text with a link [to Boot.dev](https://boot.dev) and an image ![of a bird](bird.png)",
        TextType.TEXT
    )
    
    print("--- Testing Image and Link Node Splitter Pipeline ---")
    nodes_after_images = split_nodes_image([sample_node])
    final_split_nodes = split_nodes_link(nodes_after_images)
    
    for node in final_split_nodes:
        print(node)


