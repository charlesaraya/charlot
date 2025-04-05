import unittest
import subprocess
import os

from copy_static import copy_static

class TestCopyStatic(unittest.TestCase):

    def assertEqualFilenames(self, from_dir, to_dir):
        """Tests if files and dirs are equal in both dirs"""
        # sort to avoid failing when from_files and to_files have same files but in diff order
        from_files = sorted(os.listdir(from_dir))
        to_files = sorted(os.listdir(to_dir))
        for from_filename, to_filename in zip(from_files, to_files):
            from_filepath = os.path.join(from_dir, from_filename)
            to_filepath = os.path.join(to_dir, to_filename)
            self.assertEqual(from_filename, to_filename)
            if os.path.isdir(from_filepath) and os.path.isdir(to_filepath):
                self.assertEqualFilenames(from_filepath, to_filepath)

    def test_copy_static(self):
        cwd = os.getcwd()
        from_dir = os.path.join(cwd, 'test/dummy_dir')
        to_dir = os.path.join(cwd, 'test/test_dummy_dir')

        # Create a dummy directory with files, subdirs with files and an empty dir
        script_path = os.path.join(cwd, 'src/test_create_dummy_dir.sh')
        result = subprocess.run(
            ['bash', script_path, from_dir], 
            capture_output=True, 
            text=True
        )
        print(result.stdout)  # Print the standard output of the script
        print(result.stderr)  # Print the error output if any


        copy_static(from_dir, to_dir)
        self.assertEqualFilenames(from_dir, to_dir)


if __name__ == '__main__':
    unittest.main()