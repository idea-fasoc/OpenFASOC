from os import path, rename, environ , listdir, remove, chmod

def delete_files_in_directory(directory_path):
   try:
     files = listdir(directory_path)
     for file in files:
       file_path = path.join(directory_path, file)
       if path.isfile(file_path):
         try:
            chmod(file_path, 0o777)
            remove(file_path)
         except PermissionError:
               print(f"PermissionError: Operation not permitted for {file_path}")
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

