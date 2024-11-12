# Write a Python script that counts the number of files with each extension in a given directory. The script should:
# Accept a directory path as a command line argument (using sys.argv).
# Use the os module to list all files in the directory.
# Count the number of files for each extension (e.g., .txt, .py, .jpg) and print out the counts.
# Include error handling for scenarios such as the directory not being found, no read permissions, or the directory being empty.

import os
import sys


def count_files_by_extension(directory):
    try:
        files = os.listdir(directory)
        if len(files) == 0:
            raise Exception("Directory is empty")
        extension_count = {}
        for file in files:
            if os.path.isdir(os.path.join(directory, file)):
                continue
            extension = file.split('.')[-1]
            extension_count[extension] = extension_count.get(extension, 0) + 1

        for extension, count in extension_count.items():
            print(f"Extension: {extension}, Count: {count}")
    except FileNotFoundError:
        print("Invalid directory path")
    except PermissionError:
        print("File access error")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python ex4.py <directory>")
    else:
        directory = sys.argv[1]
        count_files_by_extension(directory)


main()
