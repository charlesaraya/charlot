#!/bin/bash

DIR_PATH="$1"

# Check if the directory exists
if [ -d $DIR_PATH ]; then
  echo "Directory exists. Deleting..."
  rm -rf $DIR_PATH
  echo "Directory deleted."
else
  echo "Directory does not exist."
fi

# Create a root dummy directory
mkdir -p $DIR_PATH

# Create dummy files in the root directory
touch $DIR_PATH/file1.txt
touch $DIR_PATH/file2.txt
touch $DIR_PATH/file3.txt

# Create subdirectories
mkdir -p $DIR_PATH/subdir1
mkdir -p $DIR_PATH/subdir2
mkdir -p $DIR_PATH/subdir2/subsubdir
mkdir -p $DIR_PATH/subdir3_empty

# Create dummy files inside subdirectories
touch $DIR_PATH/subdir1/file2.txt
touch $DIR_PATH/subdir1/file1.txt # alter name order for testing purposes
touch $DIR_PATH/subdir2/file2.txt
touch $DIR_PATH/subdir2/subsubdir/file1.txt

# Verify the directory structure
echo "Directory structure created:"
tree $DIR_PATH
