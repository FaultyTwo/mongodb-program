## MongoDB Program
This branch of MongoDB program supports all kind of files, thanks to the power of LZMA compression, which reduces the size of bytes when uploading onto a MongoDB database and prone to less illegal bytes from file reading.

However. For legacy (suitable for quick machine learning), check the main branch instead (for now).

## Quick Guide
Specify the MongoDB server URL, then click "Connect" button.
If the server is found. A list of databases will be shown in the table.

For uploading files to a database. Click "Add files to the database", select the "database_folder" with following hierachy:

database_folder<br>
&emsp;|--> collection_1<br>
&emsp;&emsp;|--> img.png<br>
&emsp;&emsp;|--> img2.png<br>
&emsp;&emsp;...<br>
&emsp;|--> collection_2<br>
&emsp;&emsp;|--> doc1.docx<br>
&emsp;&emsp;|--> doc2.docx<br>
&emsp;&emsp;...<br>

To add files into a collection. Click "Add files to the collection", then select the collection folder with following hierachy:

collection<br>
&emsp;|--> doc1.docx<br>
&emsp;|--> img1.jpg<br>
&emsp;...<br>

When downloading. All files that used to be in subfolders will be put under their origin subfolder directory.

## Running the 'main.py'
Check `requirements.txt` for required libraries.

## Building a .EXE file
You can build a .EXE file from the source code using `pyinstaller` libraries, then type in the console:<br>
`pyinstaller --onefile main.py`

The file size should be reasonable since this branch doesn't longer require the numpy or scikit-image to function anymore.

## Future Features
- Implement right click context menu that allows for more functionality for better interfacing with MongoDB.
    - This includes "Add", "Delete", and "Move"
- [x] Allowing for any types of files to be uplaoded onto MongoDB
  - [x] Usually this problem was caused by illegal bytes when processing. This will be fixed.