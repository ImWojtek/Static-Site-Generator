from markdown_blocks import *
from copystatic import extract_title
import os
import shutil

def generate_page(from_path, template_path, to_path): #from_path -> md file or dir, template_path -> html template, to_path -> html file or dir
    print(f"Generating page from {from_path} to {to_path} using {template_path}")

    # read template once
    with open(template_path, "r") as f:
        template_raw = f.read()

    def render_and_write(src_path, out_path):
        with open(src_path, "r") as f:
            content = f.read()
        title = extract_title(content)
        content_html = markdown_to_html_node(content).to_html()
        rendered = template_raw.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

        out_dir = os.path.dirname(out_path) or "."
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(rendered)
        print(f"Wrote {out_path}")

    # If from_path is a directory, process each file inside it
    if os.path.isdir(from_path):
        entries = sorted(os.listdir(from_path))
        for entry in entries:
            src = os.path.join(from_path, entry)
            if not os.path.isfile(src):
                continue
            # determine output path
            if os.path.isdir(to_path) or to_path.endswith(os.sep):
                if not os.path.exists(to_path):
                    os.makedirs(to_path, exist_ok=True)
                out_file = os.path.splitext(entry)[0] + ".html"
                out = os.path.join(to_path, out_file)
            else:
                # to_path is a file path; if multiple inputs, create parent dir and write files inside it using same basename
                parent = os.path.dirname(to_path)
                if parent and os.path.exists(parent) and not os.path.isdir(to_path):
                    # treat provided to_path as directory target if it already exists as dir; else use parent dir
                    pass
                if not os.path.exists(to_path) or os.path.isfile(to_path):
                    # write each input to a sibling file named after the markdown
                    parent_dir = os.path.dirname(to_path) or "."
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir, exist_ok=True)
                    out = os.path.join(parent_dir, os.path.splitext(entry)[0] + ".html")
                else:
                    # fallback
                    out = os.path.join(to_path, os.path.splitext(entry)[0] + ".html")
            render_and_write(src, out)
    else:
        # single file input
        src = from_path
        if os.path.isdir(to_path) or to_path.endswith(os.sep):
            if not os.path.exists(to_path):
                os.makedirs(to_path, exist_ok=True)
            out_file = os.path.splitext(os.path.basename(src))[0] + ".html"
            out = os.path.join(to_path, out_file)
        else:
            out = to_path
        render_and_write(src, out)
