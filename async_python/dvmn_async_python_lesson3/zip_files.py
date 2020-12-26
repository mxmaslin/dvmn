import os
from os.path import basename
from zipfile import ZipFile


with ZipFile('zipped.zip', 'w') as zip_obj:
   for folder_name, subfolders, filenames in os.walk('files_to_zip'):
       for filename in filenames:
           file_path = os.path.join(folder_name, filename)
           zip_obj.write(file_path, basename(file_path))
