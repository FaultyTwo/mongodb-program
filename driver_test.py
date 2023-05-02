# TEST FILE
# IGNORE

import format_handler, format_handler_sci
from path_walk import *

import cv2
from skimage.io import imsave

# D:\Python\Machine Learning ENV\DummyInterview\example_codes
# D:\Python\Machine Learning ENV\DummyInterview\project_data\data_noaudio\รูปภาพภาคสนาม\แคมป์คนงาน กทม.-บางแค

a = path_walk("D:\Python\Machine Learning ENV\DummyInterview\project_data\data_noaudio\รูปภาพภาคสนาม\แคมป์คนงาน กทม.-บางแค")

why = "\\".join(a[1].parts)
print(why)

#en = format_handler.image_encode(why,12.31)
en_sci = format_handler_sci.image_encode(why)

#print(format_handler.image_decode(en))
print(format_handler_sci.image_decode(en_sci))

imsave("poop.jpg",arr=format_handler_sci.image_decode(en_sci)) # use scikit imsave to save image, or else color will be L O S S