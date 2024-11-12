import os


def rename_files(directory):
    try:
        files = os.listdir(directory)
        for i, file in enumerate(files, start=1):
            if os.path.isdir(os.path.join(directory, file)):
                continue
            extension = file.split('.')[-1]
            new_file = f"file{i}.{extension}"
            os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
        print("Files renamed successfully")
    except FileNotFoundError:
        print("Invalid directory path")
    except PermissionError:
        print("File could not be renamed. Insufficient permissions")
    except Exception as e:
        print(f"An error occurred: {e}")

rename_files("./wrong_directory")

rename_files("./ex2")
