
from copystatic import clean_and_copy_directory
from gencontent import generate_pages_recursive

def main():
    
    source_dir = "static"
    destination_dir = "public"
    
    print("Starting the build process...")
    
    
    clean_and_copy_directory(source_dir, destination_dir)
    
    print("All files successfully copied!")

    print("Generating index page...")
    
    generate_pages_recursive(
        dir_path_content="content",      # Path to your source markdown file
        template_path="template.html",     # Path to your HTML template layout
        dest_dir_path="public"      # Target location to serve at localhost root
    )
    print("Build complete!")




if __name__ == "__main__":
    main()