import os

FOLDER_PATH = r'C:\\Users\\anosh\\Documents\\GitHub\\project-Re-LAI-lite\\images\\numbers\\image_write\\enemy_damage\\done_images'

def listDir(dir):
    fileNames = os.listdir(dir)
    new_names = []
    for fileName in fileNames:
        fileName = fileName.replace('.jpg', '')
        fileName = int(fileName)
        new_names.append(fileName)
    new_names.sort()
    return print(new_names)

listDir(FOLDER_PATH)
