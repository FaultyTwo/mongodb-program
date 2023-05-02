## MongoDB Dataset Program
- So far. Support following formats.
  - Images: ".jpeg", ".jpg", ".png"
  - Word Documents: ".docx", ".doc"
    - Other formats that aren't in the following, aren't supported yet. So by default, they are ignored when uploading.
- Files are normally processed when uploading and downloading for ready to be used with deep learning tasks.

## Quick Guide
Specify the MongoDB server URL, then click "Connect" button.
If the server is found. A list of databases will be shown in the table.

For importing files to a database. Click "Add files to the database", select the "database_folder" with following hierachy:
database_folder<br>
    |--> collection_1<br>
        |--> img.png<br>
        |--> img2.png<br>
        ...<br>
    |--> collection_2<br>
        |--> doc1.docx<br>
        |--> doc2.docx<br>
        ...<br>

Any subfolders inside collections will be lumped with files in collections.

To add files into a collection. Click "Add files to the collection", then select the collection folder with following hierachy:
collection<br>
    |--> doc1.docx<br>
    |--> img1.jpg<br>
    ...<br>

Any subfolders inside a collection will be lumped with files in that collection.

To download a database. Select the database then click 'Download a database' and specify the location.<br>
To download a collection. Select the collection then click 'Download a collection' and specify the location.

## Running the 'main.py'
Check `requirements.txt` for required libraries.

## Building a .EXE file
You can build a .EXE file from the source code using `pyinstaller` libraries, then type in the console:
`pyinstaller --onefile main.py`

## Future Features
- Implement right click context menu that allows for more functionality for better interfacing with MongoDB.
    - This includes "Add", "Delete", and "Move"
- Allowing for any types of files to be uplaoded onto MongoDB
  - Usually this problem was caused by illegal bytes when processing. This will be fixed.