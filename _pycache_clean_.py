# function to clean up all the pycache folders when dragging over to the rashperry
import os
import re

def find_all_dirs():
    """Finds all the __pycache__ subdirectories recursively and returns a list of them, in a relative path format"""
    pycache_dirs = []
    pycache_regex = re.compile(r".*__pycache__")
    venv_regex = re.compile(r".*venv")
    git_regex = re.compile(r".*\.git")
    for root, dirs, files in os.walk("."):
        is_ignore = venv_regex.match(root) or git_regex.match(root)
        if is_ignore:
            continue
        for dir in dirs:
            is_dir_ignore = venv_regex.match(dir) or git_regex.match(dir)
            if is_dir_ignore:
                break
            if pycache_regex.match(dir):
                pycache_dirs.append(os.path.join(root,dir))
    return pycache_dirs


def main():
    pycache_dirs = find_all_dirs()

    print(f"Found {len(pycache_dirs)} __pycache__ directories")
    for dir in pycache_dirs:
        print(f"Removing {dir}")
    response = input("Would you like to remove all the directories? (y/n): ")
    if response == "y":
        for dir in pycache_dirs:
            print(f"Removing {dir}")
            os.system(f"rm -rf {dir}")
        print("All directories removed")

if __name__ == "__main__":
    main()