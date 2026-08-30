import os
import shutil

def clean_and_copy_directory(src, dst):
    # Step 1: Clean the destination directory if it exists
    if os.path.exists(dst):
        print(f"Cleaning destination directory: {dst}")
        shutil.rmtree(dst)
    
    # Recreate the root destination directory
    os.mkdir(dst)
    
    # Step 2: Start the recursive copy process
    recursive_copy(src, dst)

def recursive_copy(src, dst):
    # Loop through everything inside the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Log the file copy action as requested
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # If it is a directory, make the new directory in dst
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            # Recursively copy its contents
            recursive_copy(src_path, dst_path)

