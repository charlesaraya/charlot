import os
import shutil

def clear_dir(path):
    def clear_files(path):
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                print(f"Deleting file ...\t{filepath}")
                os.remove(filepath)
            else:
                clear_files(filepath)
        if os.path.isdir(path) and not os.listdir(path):
            print(f"Deleting dir ...\t{path}")
            os.rmdir(path)
            return 0
    clear_files(path)
    os.mkdir(path)
    return 0

def copy_dir(orig_path, dest_dir):
    for filename in os.listdir(orig_path):
        orig_filepath = os.path.join(orig_path, filename)
        dest_filepath = os.path.join(dest_dir, filename)
        if os.path.isfile(orig_filepath):
            print(f"Copy file ...\t{filename} to {dest_dir}")
            shutil.copy(orig_filepath, dest_filepath)
        else:
            print(f"Creating dir ...\t{filename} in {dest_dir}")
            os.mkdir(dest_filepath)
            copy_dir(orig_filepath, dest_filepath)

def copy_static(from_dir, to_dir):
    if not os.path.isdir(from_dir):
        raise ValueError(f"Target directory {from_dir} does not exist.")
    if os.path.isdir(to_dir):
        print(f"Deleting destination directory...")
        try:
            clear_dir(to_dir)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Destination directory {from_dir} does not exist.")
        print(f"Creating directory...")
        os.mkdir(to_dir)
    copy_dir(from_dir, to_dir)
    return 0


if __name__ == '__main__':
    import subprocess

    cwd = os.getcwd()
    from_dir = os.path.join(cwd, 'dummy_dir')
    to_dir = os.path.join(cwd, 'dest_dummy_dir')
    script_path = os.path.join(cwd, 'create_dummy_dir.sh')

    result = subprocess.run(
        ['bash', script_path, from_dir], 
        capture_output=True, 
        text=True
    )
    print(result.stdout)  # Print the standard output of the script
    print(result.stderr)  # Print the error output if any
    copy_static(from_dir, to_dir)
