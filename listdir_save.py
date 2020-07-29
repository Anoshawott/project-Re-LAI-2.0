import pickle
import os

FOLDER_PATH = r'C:\\Users\\anosh\\Documents\\GitHub\\project-Re-LAI-lite\\images\\numbers\\image_write\\enemy_damage\\done_images'
fileNames = os.listdir(FOLDER_PATH)

class list_search:
    def list_def(self):
        new_names = {}
        for fileName in fileNames:
            fileName = fileName.replace('.jpg', '')
            fileName = int(fileName)
            new_names[fileName]=0
        new_names = sorted(new_names)

        pickle_out = open('imgNames.pickle', 'wb')
        pickle.dump(new_names, pickle_out)
        pickle_out.close()
        return
    
    def list_save(self, data=None):
        pickle_out = open('imgNames.pickle', 'wb')
        pickle.dump(data, pickle_out)
        pickle_out.close()
        return