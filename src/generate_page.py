import textnode as tn
import os

def create_dir_path(path):
    dirs = path.split('/')
    new_dir = ''
    for dir in dirs:
        if dir and dir != '.':
            new_dir += dir
            if not os.path.isdir(new_dir):
                os.mkdir(new_dir)
            new_dir += '/'

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as from_file:
        markdown = from_file.read()

    title = tn.extract_title(markdown)
    content = tn.markdown_to_html_node(markdown)

    placeholders = [
        ('{{ Title }}', title),
        ('{{ Content }}', content),
    ]
    with open(template_path, 'r') as template_file:
            generated_file = ''
            for line in template_file:
                generated_line = line
                for placeholder in placeholders:
                    generated_line = generated_line.replace(placeholder[0], placeholder[1])
                generated_file += generated_line

    dir_path = os.path.dirname(dest_path)
    dest_path = dest_path[1:] if dest_path.startswith('/') else dest_path # default to relative paths
    if os.path.isfile(dest_path):
        mode = 'w'
    else:
        mode = 'x'
        create_dir_path(dir_path)
    with open(dest_path, mode) as dest_file:
         dest_file.write(generated_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isdir(dir_path_content):
        if (files := os.listdir(dir_path_content)):
            for file in files:
                filepath = os.path.join(dir_path_content, file)
                dest_filepath = os.path.join(dest_dir_path, file)
                if os.path.isfile(filepath):
                    dest_filepath, _ = os.path.splitext(dest_filepath)
                    generate_page(filepath, template_path, dest_filepath + '.html')
                elif os.path.isdir(filepath):
                    generate_pages_recursive(filepath, template_path, dest_filepath)
