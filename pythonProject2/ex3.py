import os
import sys


def calculate_total_size(directory):
    total_size = 0
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_size = os.stat(os.path.join(root, file)).st_size
                print(f"File: {file}, Size: {file_size} bytes")
                total_size += file_size

        print(f"Total size of all files in '{directory}': {total_size} bytes")
    except FileNotFoundError:
        print("Invalid directory path")
    except PermissionError:
        print("File access error")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python ex3.py <directory>")
    else:
        directory = sys.argv[1]
        calculate_total_size(directory)


main()
