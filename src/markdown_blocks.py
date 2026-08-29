from enum import Enum
from htmlnode import ParentNode
# Ensure your other functions and enums are imported correctly
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    # 1. Split the entire document by double newlines to find chunks
    raw_blocks = markdown.split("\n\n")
    cleaned_blocks: list[str] = []
    
    for block in raw_blocks:
        # 2. Strip leading and trailing whitespace from the block
        stripped_block = block.strip()
        
        # 3. Only keep blocks that are not empty strings
        if stripped_block != "":
            cleaned_blocks.append(stripped_block)
            
    return cleaned_blocks


def block_to_block_type(block: str) -> BlockType:
    # 1. Check for Heading syntax (1 to 6 '#' followed by a space)
    if (
        block.startswith("# ") 
        or block.startswith("## ") 
        or block.startswith("### ") 
        or block.startswith("#### ") 
        or block.startswith("##### ") 
        or block.startswith("###### ")
    ):
        return BlockType.HEADING

    # 2. Check for Code Block syntax (Starts and ends with exactly 3 backticks)
    if block.startswith("```") and block.endswith("```") and len(block) >= 6:
        return BlockType.CODE

    # Split the block into individual lines to check multiline conditions
    lines = block.split("\n")
   
    # 3. Check for Quote Block syntax (Every line must start with '>')
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # 4. Check for Unordered List syntax (Every line must start with '* ' or '- ')
    is_unordered_list = True
    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # 5. Check for Ordered List syntax (Every line must increment starting sequentially at '1. ')
    is_ordered_list = True
    for i in range(len(lines)):
        expected_prefix = f"{i + 1}. "
        if not lines[i].startswith(expected_prefix):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # 6. Default fallback condition
    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown: str) -> ParentNode:
    # 1. Break the raw document string into individual distinct blocks
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    # 2. Iterate through each block to categorize and compile them
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                # Paragraphs are wrapped in <p> tags
                # Join lines if the paragraph spans multiple lines
                cleaned_text = " ".join([line.strip() for line in block.split("\n")])
                children = text_to_children(cleaned_text)
                block_nodes.append(ParentNode(tag="p", children=children))

            case BlockType.HEADING:
                # Headings require counting the leading hashes
                lines = block.split("\n")
                # Assume a single-line block for a heading, calculate hash length
                level = len(block) - len(block.lstrip("#"))
                heading_text = block[level:].strip()
                children = text_to_children(heading_text)
                block_nodes.append(ParentNode(tag=f"h{level}", children=children))

            case BlockType.CODE:
                # Special Case: No inline processing. Text remains a raw literal string.
                # Strip out the wrapper ``` signs from start and end
                lines = block.split("\n")
                if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
                    code_text = "\n".join(lines[1:-1])
                else:
                    code_text = block.strip("`").strip("\n")

                code_text_node = TextNode(code_text, TextType.CODE)
                code_html_node = text_node_to_html_node(code_text_node)

                block_nodes.append(ParentNode(tag="pre", children=[code_html_node]))
                
                
            case BlockType.QUOTE:
                # Quote blocks remove the leading '>' character and spaces from each line
                cleaned_lines = []
                for line in block.split("\n"):
                    cleaned_lines.append(line.lstrip("> ").strip())
                quote_text = " ".join(cleaned_lines)
                children = text_to_children(quote_text)
                block_nodes.append(ParentNode(tag="blockquote", children=children))

            case BlockType.UNORDERED_LIST:
                # Map every list element line into an <li> parent node
                li_nodes = []
                for line in block.split("\n"):
                    # Strip the starting '* ' or '- ' marker
                    item_text = line[2:].strip()
                    li_nodes.append(ParentNode(tag="li", children=text_to_children(item_text)))
                block_nodes.append(ParentNode(tag="ul", children=li_nodes))

            case BlockType.ORDERED_LIST:
                # Map every ordered list element line into an <li> parent node
                li_nodes = []
                for line in block.split("\n"):
                    # Strip the dynamic numerical prefix (e.g. '1. ', '12. ')
                    prefix_end = line.find(". ") + 2
                    item_text = line[prefix_end:].strip()
                    li_nodes.append(ParentNode(tag="li", children=text_to_children(item_text)))
                block_nodes.append(ParentNode(tag="ol", children=li_nodes))

            case _:
                raise ValueError(f"Invalid block type context detected: {block_type}")

    # 3. Encapsulate all elements under a parent <div> container node and return
    return ParentNode(tag="div", children=block_nodes)

