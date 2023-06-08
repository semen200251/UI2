import os
import shutil


def check_folder_writable(folder_path):
    return os.access(folder_path, os.W_OK)


def check_folder_readable(file_paths):
    for file_path in file_paths:
        if not os.access(file_path, os.R_OK):
            return False
    return True


def transfer_files(file_paths, destination_folder):
    for file_path in file_paths:
        if file_path is not None:
            try:
                file_name = os.path.basename(file_path)
                destination_file = os.path.join(destination_folder, file_name)
                shutil.copyfile(file_path, destination_file)
                print(f"Файл {file_name} успешно загружен в папку {destination_folder}.")
            except Exception as e:
                return e
    return True

