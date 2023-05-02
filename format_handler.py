# OBSOLETED
# Functions for handling each type of files before being sent into mongodb

import os, cv2, sys
import numpy as np
from docx import Document

def image_encode(path:str, scale_percent:float = 50):
    img = cv2.imread(path)
    dim = (int(img.shape[1] * (scale_percent / 100)),
        int(img.shape[0] * (scale_percent / 100)))
    # rescale the image, the lower, the smaller

    resized = cv2.resize(img,dim,interpolation=cv2.INTER_AREA) # resize the image
    resized_encode = cv2.imencode(".jpg",resized)[1] # get ndarray only
    resized_bytes = resized_encode.tobytes() # to bytes

    return resized_bytes

def image_decode(data):
    resized_decode = np.frombuffer(data,dtype=np.uint8) # create ndarray for decoding the image
    output = cv2.imdecode(resized_decode, cv2.IMREAD_COLOR) # get rescaled image
    return output

def docx_encode(path:str):
    with open(path,'rb') as f:
        data = Document(f)
    
    doc_str = ""
    for x in data.paragraphs:
        #print(x.text)
        doc_str += x.text + " "
    
    return doc_str

# in the future. for universal file supports.
# either we store the data in this format
# {
#   "name":"eman"
#   "format": ".pdf"
#   "data": "bindata" # using "tobytes" methods
# }
# with this. we won't need to rely on checking file format anymore
# however. since this is clearly for processing data for ml.
# we would still need an extra processing to make sure they are suitable for ml
# but our current method. it should good enough to handle standard data using in ml