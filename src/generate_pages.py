import os

from markdown_blocks import markdown_to_html_node
from copystatic import extract_title


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively walk dir_path_content. For every .md file generate a corresponding
    .html file under dest_dir_path preserving directory structure, using template_path.
    """
    # read template once
    with open(template_path, "r") as f:
        template_raw = f.read()

    for root, _, files in os.walk(dir_path_content):
        for filename in sorted(files):
            if not filename.endswith(".md"):
                continue

            src_path = os.path.join(root, filename)
            # relative path inside content dir, then replace .md -> .html
            rel_path = os.path.relpath(src_path, dir_path_content)
            rel_html = os.path.splitext(rel_path)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, rel_html)

            # ensure destination directory exists
            dest_dir = os.path.dirname(dest_path) or "."
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            # render
            with open(src_path, "r") as rf:
                content = rf.read()
            title = extract_title(content)
            content_html = markdown_to_html_node(content).to_html()
            rendered = (
                template_raw.replace("{{ Title }}", title)
                .replace("{{ Content }}", content_html)
            )

            # write output
            with open(dest_path, "w") as wf:
                wf.write(rendered)
            print(f"Wrote {dest_path}")