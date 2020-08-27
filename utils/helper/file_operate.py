import os

def mkdir(path):
    # ȥ?????????ߵĿո?
    path=path.strip()
    # ȥ??β?? \????
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
        
    return path


'''
@path  
@file_name 
@data 
'''
def save_file(file_name, data,path=None):
    if data == None:
        return
    if path:
        mkdir(path)
        if(not path.endswith("/")):
            path=path+"/"
    else:
        path=""
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()

def del_file(file_name,path=None):
    if path:
        mkdir(path)
        if(not path.endswith("/")):
            path=path+"/"
    else:
        path=""
    if(os.path.exists(path+file_name)):
        os.remove(path+file_name)
       