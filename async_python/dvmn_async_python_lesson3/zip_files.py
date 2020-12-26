import subprocess


process = subprocess.Popen(
    ['zip', '-r', 'zipped.zip', 'files_to_zip'],
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)
process.communicate()