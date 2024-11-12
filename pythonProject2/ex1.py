
import os
import sys


def read_extension_files(directory, extension):
    try:
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                continue
            if file.endswith(f'.{extension}'):
                with open(os.path.join(directory, file), 'r') as f:
                    print(f"File: {file}")
                    print(f.read())
    except FileNotFoundError:
        print("Invalid directory path")
    except PermissionError:
        print("File access error")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python ex1.py <directory> <extension>")
    else:
        directory = sys.argv[1]
        extension = sys.argv[2]
        read_extension_files(directory, extension)


main()
