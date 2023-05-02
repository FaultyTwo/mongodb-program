import pathlib

def path_walk(path:str):
    dataset = pathlib.Path(path)
    wanted = ['.docx','.png','.jpg','.jpeg','.doc'] # targeted file extension
    valid = list()

    for x in list(dataset.rglob("*")):
        if x.is_file(): # if a path is a file path
            spr_1 = x.suffix
            if spr_1 in wanted: # if that file is wanted
                valid.append(x)
    
    return valid