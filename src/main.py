import sys
import os

from copy_static import copy_static
from generate_page import generate_page

def main():
    cwd = os.getcwd()
    static_path = os.path.join(cwd, 'static')
    public_path = os.path.join(cwd, 'public')
    copy_static(static_path, public_path)

    dir_path_content = 'content/index.md'
    template_path = 'template.html'
    dest_dir_path = 'public/index.html'

    generate_page(dir_path_content, template_path, dest_dir_path)

main()
