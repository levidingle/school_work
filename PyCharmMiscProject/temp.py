import shutil
import tempfile
import time
# Creates a temporary folder in C:\Users\inglevg\AppData\Local\Temp
tempdir = tempfile.mkdtemp()
print(tempdir)
# This sets it to delete after 10 seconds
time.sleep(10)
shutil.rmtree(tempdir)

