import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_pages import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
content_path = "./content"
template_path = "./template.html"


def main():
    # CLI basepath (default "/")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # normalize: ensure leading and trailing slash
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"

    # Delete anything in the docs directory but keep the directory itself
    if os.path.exists(dir_path_public):
        if os.path.isfile(dir_path_public) or os.path.islink(dir_path_public):
            os.unlink(dir_path_public)
            os.makedirs(dir_path_public, exist_ok=True)
        else:
            print("Clearing docs directory contents...")
            for entry in os.listdir(dir_path_public):
                path = os.path.join(dir_path_public, entry)
                if os.path.islink(path) or os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
    else:
        os.makedirs(dir_path_public, exist_ok=True)

    # Copy all static files from static -> docs
    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Generate pages for every markdown file under content -> docs preserving structure
    print(f"Generating pages from {content_path} -> {dir_path_public} using {template_path} (basepath={basepath})")
    generate_pages_recursive(content_path, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()
