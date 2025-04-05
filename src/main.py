from copy_static import copy_static
import sys
import os

def main():
    cwd = os.getcwd()
    static_path = os.path.join(cwd, 'static')
    public_path = os.path.join(cwd, 'public')
    copy_static(static_path, public_path)

main()
