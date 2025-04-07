import sys
import os

from copy_static import copy_static
from generate_page import generate_pages_recursive

def main():
    basepath = sys.argv[1] if (len(sys.argv) == 2) else ''
    static_path = os.path.join(basepath, 'static')
    public_path = os.path.join(basepath, 'public')
    content_path = os.path.join(basepath, 'content')
    template_path = os.path.join(basepath, 'template.html')

    copy_static(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path, basepath)

main()
