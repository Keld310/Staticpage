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