import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    # Split the markdown string into individual lines
    lines = markdown.splitlines()
    
    for line in lines:
        # Strip whitespace from the edges of the line
        stripped_line = line.strip()
        
        # Check if the line starts with '#' followed by a space
        if stripped_line.startswith("# "):
            # Remove the '#' and strip any remaining whitespace from the title
            return stripped_line[2:].strip()
            
    # Raise an exception if no H1 header was found in the loop
    raise ValueError("No H1 header found in the provided markdown.")

def generate_page(from_path, template_path, dest_path):
    # 1. Print the tracking status message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # 2. Read the markdown source file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    # 3. Read the HTML template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # 4. Convert markdown content to an HTML string
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # 5. Extract the page title
    page_title = extract_title(markdown_content)
    
    # 6. Replace the placeholders in the template
    # This assumes your template uses exactly {{ Title }} and {{ Content }}
    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # 7. Create missing destination subdirectories if they do not exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Write the completed HTML file out to disk
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Loop through all files and folders in the current content directory level
    for item in os.listdir(dir_path_content):
        # Build full absolute/relative paths for the source item
        src_path = os.path.join(dir_path_content, item)
        
        # Determine if the item is a file or a nested folder
        if os.path.isfile(src_path):
            # Only process markdown files (.md)
            if item.endswith(".md"):
                # Swap the .md extension out for .html for the build output
                html_filename = item.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                # Reuse your existing single page layout compiler
                generate_page(src_path, template_path, dest_path)
        else:
            # If it's a directory, compute the matching destination folder path
            new_dest_dir = os.path.join(dest_dir_path, item)
            
            # Recursively descend into the subfolder to crawl its contents
            generate_pages_recursive(src_path, template_path, new_dest_dir)