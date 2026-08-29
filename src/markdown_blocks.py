from enum import Enum

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
