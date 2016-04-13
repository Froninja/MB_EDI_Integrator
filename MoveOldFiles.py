import shutil, os
from datetime import date
os.chdir('C:\\')

dir = "P:\\EDI\\MAPDATA\\"
newfolder = 'P:\\\EDI\\MAPDATA\\Archive\\'
newfolder += date.today().strftime("%m-%d-%Y")

if not os.path.exists(newfolder):
    os.makedirs(newfolder)

for file in os.listdir(dir):
    if file[-3:] == 'txt':
        shutil.move(dir + file, newfolder)