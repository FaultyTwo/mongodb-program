import pathlib, lzma

def path_walk(path:str):
    dataset = pathlib.Path(path)
    valid = list()

    for x in list(dataset.rglob("*")):
        if x.is_file(): # if a path is a file path
            valid.append(x)
    
    return valid

def file_encode(path:str):
    # it's not a wise idea to put the entire binary into mongodb
    # either we have to compress it first or else
    with open(path, "rb") as f:
        compressed_data = lzma.compress(f.read())
        return compressed_data
    
def file_decode(path:str,data):
    with open(path, "wb") as f:
        depressed_data = lzma.decompress(data)
        f.write(depressed_data)