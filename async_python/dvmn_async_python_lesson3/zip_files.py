import subprocess


process = subprocess.Popen(
    ['zip', '-r', '-', 'files_to_zip'],
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)
process.communicate()
