
from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, 
                            QLabel, QWidget, QLineEdit, QHBoxLayout,
                            QGridLayout, QPushButton, QListWidget,
                            QFileDialog, QMenu, QMessageBox)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer
from pymongo import MongoClient
from helper_func import *
from dialogs import *

import sys, os

# GUI Design Guideline:
# - First, we need the user to add their mongodb server address
# After the server is connected, we allow user to search, add, remove .etc

# TODO: Mute all of print out complaints
# TODO: Proper threading when uploading and downloading, so your program doesn't freeze and die
# like when you alt-tab TF2 when starting up

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MongoDB Dataset Program")
        self.main = MainWidgets()
        self.setCentralWidget(self.main)

class MainWidgets(QWidget):
    def __init__(self):
        super().__init__()
        # this constructor is a mess
        # signal stuffs
        self.mongo_sv = QLineEdit()
        self.mongo_sv_btn = QPushButton("Connect")
        self.mongo_sv_btn.clicked.connect(self.__mongo)

        self.mongo_search = QLineEdit()
        self.mongo_search.editingFinished.connect(self.__entry_query)
        self.mongo_search.setEnabled(False)

        self.data_view = QListWidget()
        #self.data_view.addItem("CRACK!!???")
        self.data_view.itemClicked.connect(self.__data_click)
        self.data_view.setEnabled(False)
        self.data_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.data_view.customContextMenuRequested.connect(self.__data_context_menu)
        self.data_view.setEnabled(False)

        self.col_view = QListWidget()
        self.col_view.itemClicked.connect(self.__col_click)
        self.col_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.col_view.customContextMenuRequested.connect(self.__col_context_menu)
        self.col_view.setEnabled(False)

        self.entry_view = QListWidget()
        self.entry_view.itemClicked.connect(self.__entry_click)
        self.entry_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.entry_view.customContextMenuRequested.connect(self.__entry_context_menu)
        self.entry_view.setEnabled(False)

        self.mongo_status = QLabel("Status: Not Connected")
        self.mongo_status.setStyleSheet("color: red")
        
        # no signal stuffs
        mongo_sv_txt = QLabel("Please specify the server url:")

        # Need to group both of this together
        sv_lay = QHBoxLayout() #
        sv_lay.addWidget(self.mongo_sv) # text input
        sv_lay.addWidget(self.mongo_sv_btn) # search button

        # potato_lay = Mani Layout for the main window
        potato_lay = QGridLayout()
        potato_lay.addWidget(mongo_sv_txt,0,0) # text
        potato_lay.addLayout(sv_lay,1,0) # server search
        potato_lay.addWidget(self.mongo_search,1,2) # query and search
        potato_lay.addWidget(self.mongo_status,2,0) # mongo status text
        potato_lay.addWidget(self.data_view,3,0) # database table
        potato_lay.addWidget(self.col_view,3,1) # collections table
        potato_lay.addWidget(self.entry_view,3,2) # collections table
    
        self.lay = QVBoxLayout(self) # this is our parent
        self.lay.addLayout(potato_lay)
        self.lay.setSpacing(5)
        
        self.col = None # cache the col variable

        self.setLayout(self.lay)

    def __data_context_menu(self,pos):
        item = self.data_view.itemAt(pos) # check if there's an item or not
        menu = QMenu(self)
        # item action
        if item is not None:
            self.database = self.cilent[item.text()]
            action_download = menu.addAction("Download")
            action_download.triggered.connect(self.__download)
            action_upload = menu.addAction("Upload")
            action_upload.triggered.connect(self.__upload)
            action_delete = menu.addAction("Delete")
            action_delete.triggered.connect(self.__delete_database)
            seperator = QAction(self)
            seperator.setSeparator(True)
            menu.addAction(seperator)

        # global action
        action_new = menu.addAction("New")
        action_new.triggered.connect(self.__new_database)
        menu.exec(self.data_view.mapToGlobal(pos))

    def __new_database(self):
        dialog = NewDatabaseDialog(self)
        dialog.return_value.connect(self.__new_database_exec)
        dialog.exec()

    def __new_database_exec(self, value):
        print(value)
        self.database = self.cilent[value] # does this even work?
        self.col = self.database["collection"]
        self.col.insert_one({"name": "test","subpath":-1,"content":"literally nothing"})
        # re and fresh
        self.database = None
        self.data_view.clear()
        self.data_view.addItems(self.cilent.list_database_names())
        self.col = None
        self.col_view.clear() # refresh
        self.entry = None
        self.entry_view.clear() # refresh
        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")

    def __delete_database(self):
        # "Are you sure you want to drop this?" windows
        name = self.database.name
        confirmation = QMessageBox.question(self, "Delete database", "Are you SURE you want to delete this database?\n(You can't undo this process!)")
        if confirmation == QMessageBox.StandardButton.Yes:
            self.cilent.drop_database(self.database)
            self.database = None
            self.data_view.clear()
            self.data_view.addItems(self.cilent.list_database_names())
            self.col = None
            self.col_view.clear() # refresh
            self.col_view.setEnabled(False)
            self.entry = None # refresh entry too
            self.entry_view.clear()
            self.entry_view.setEnabled(False)
        else:
            return
        self.mongo_status.setText(f"Status: Dropped \"{name}\"")
        self.mongo_status.setStyleSheet("color: green")

    def __col_context_menu(self,pos):
        item = self.col_view.itemAt(pos) # check if there's an item or not
        menu = QMenu(self)
        # item action
        if item is not None:
            self.col = self.database[item.text()]
            action_download = menu.addAction("Download")
            action_download.triggered.connect(self.__download_col)
            action_upload = menu.addAction("Upload")
            action_upload.triggered.connect(self.__upload_col)
            action_delete = menu.addAction("Delete")
            action_delete.triggered.connect(self.__delete_col)
            seperator = QAction(self)
            seperator.setSeparator(True)
            menu.addAction(seperator)

        # entry refresh menu
        if self.col_view.count() > 0:
            action_new = menu.addAction("Refresh")
            action_new.triggered.connect(self.__refresh_col)

        # global action
        action_new = menu.addAction("New")
        action_new.triggered.connect(self.__new_col)
        menu.exec(self.col_view.mapToGlobal(pos))
    def __refresh_col(self):
        self.entry_view.clear()
        self.entry_view.addItems(self.col.find().distinct("name"))
        self.mongo_status.setText(f"Status: Refreshed")
        self.mongo_status.setStyleSheet("color: green")

    def __delete_col(self):
        # "Are you sure you want to drop this?" windows
        name = self.col.name
        confirmation = QMessageBox.question(self, "Delete collection", "Are you sure you want to delete this collection?")
        if confirmation == QMessageBox.StandardButton.Yes:
            self.col.drop()
            self.col = None
            self.col_view.clear() # refresh
            self.col_view.addItems(self.database.list_collection_names())
            self.entry = None # refresh entry too
            self.entry_view.clear()
            self.mongo_search.clear()
            self.mongo_search.setEnabled(False)
        else:
            return
        self.mongo_status.setText(f"Status: Dropped \"{name}\"")
        self.mongo_status.setStyleSheet("color: green")
    
    def __entry_context_menu(self,pos):
        item = self.entry_view.itemAt(pos) # check if there's an item or not
        menu = QMenu(self)
        # item action
        if item is not None:
            self.entry = self.col[item.text()]
            action_download = menu.addAction("Download")
            action_download.triggered.connect(self.__download_entry)
            action_delete = menu.addAction("Delete")
            action_delete.triggered.connect(self.__delete_entry)
            seperator = QAction(self)
            seperator.setSeparator(True)
            menu.addAction(seperator)

        # global action
        menu.exec(self.entry_view.mapToGlobal(pos))

    def __delete_entry(self):
        # "Are you sure you want to drop this?" windows
        name = self.entry.name.split(".")[1:]
        name = ".".join(name)
        confirmation = QMessageBox.question(self, "Delete entry", "Are you sure you want to delete this entry?")
        if confirmation == QMessageBox.StandardButton.Yes:
            # of course ".name" method also includes its collection name too
            self.col.delete_one({"name": name})
            self.entry = None
            self.entry_view.clear()
            self.entry_view.addItems(self.col.find().distinct("name"))
        else:
            return
        self.mongo_status.setText(f"Status: Dropped an entry")
        self.mongo_status.setStyleSheet("color: green")
    
    def __data_click(self, item):
        # display col items when database is clicked
        self.col_view.clear()
        self.entry_view.clear()

        self.database = self.cilent[item.text()]
        self.col_view.addItems(self.database.list_collection_names())
        self.mongo_search.setEnabled(False)
        self.entry_view.setEnabled(False)
        self.col_view.setEnabled(True)

        self.col = None # Prevent phantom collections
        self.entry = None # Prevent phantom entry
    
    def __col_click(self, item):
        # specify what collections user wants to add to
        self.col = self.database[item.text()]
        print(item.text())
        self.entry_view.clear()
        self.entry_view.addItems(self.col.find().distinct("name"))
        self.mongo_search.setEnabled(True)
        self.entry_view.setEnabled(True)
        self.entry = None
    
    def __entry_click(self, item):
        self.entry = self.col[item.text()]
        print(self.entry)

    def __entry_query(self):
        if len(self.mongo_search.text()) == 0:
           self.mongo_search.clearFocus()
           self.entry_view.clear()
           self.entry_view.addItems(self.col.find().distinct("name"))
           return # really? nothing?
        # querying
        search_results = self.entry_view.findItems(self.mongo_search.text(),Qt.MatchFlag.MatchContains)
        search_strings = [item.text() for item in search_results] # get names
        self.entry_view.clear()
        self.entry_view.addItems(self.col.find({"name": {"$in": search_strings}}).distinct("name"))
        self.mongo_search.clearFocus()

    def __mongo(self):
        self.data_view.clear()
        self.col_view.clear()
        self.entry_view.clear()
        self.col = None
        self.entry = None
        self.data_view.setEnabled(True)
        self.col_view.setEnabled(False)
        self.entry_view.setEnabled(False)
        self.mongo_search.setEnabled(False)
        # This is going to be pain in the ass to design
        # Need some clear gui design before designing .. this entire things
        try:
            #print("Looking for the server ...")
            #self.mongo_status.setStyleSheet("color: yellow")
            #self.mongo_status.setText("Status: Connecting ...")
            self.cilent = MongoClient(str(self.mongo_sv.text()),serverSelectionTimeoutMS=3000)
            #print(str(self.mongo_sv.text()))
            sv_check = self.cilent.list_database_names() # check if cilent can connect or not
        except:
            #print("Couldn't find the server.. returning ..")
            self.mongo_status.setText("Status: Fetch Failed!")
            self.mongo_status.setStyleSheet("color: red")
            return
        else:
            #print("Found! Hurray!")
            self.mongo_status.setText("Status: Fetched")
            self.mongo_status.setStyleSheet("color: green")

        #print(self.cilent.list_database_names())
        self.data_view.addItems(self.cilent.list_database_names())
        
    def __new_col(self):
        dialog = NewCollectionDialog(self)
        dialog.return_value.connect(self.__new_col_exec)
        dialog.exec()

    def __new_col_exec(self, value):
        self.database.create_collection(value)
        self.col = None
        self.col_view.clear() # refresh
        self.col_view.addItems(self.database.list_collection_names())
        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")

    def __upload_col(self):
        # Upload for collection
        self.fol = QFileDialog.getExistingDirectory(self,"Specify your data directory")
        if(len(self.fol) == 0): # almost forgot about the cancel culture
            print("no, gtfo")
            return
        print(self.fol)
        print(self.col)

        push = path_walk(self.fol) # get all dir
        main_path = pathlib.Path(self.fol)
        print(len(main_path.parts),main_path.parts)

        for y in push:
            subpath = y.parts[y.parts.index(main_path.parts[-1])+1:len(y.parts) - 1] # get subfolders inside a folder
            data_dict = {
                "name": str(y.parts[-1]),
                "subpath": '/'.join(subpath) if len(subpath) > 0 else -1,
                "content": file_encode(y)
            }
            #print(data_dict)
            self.col.insert_one(data_dict) # let's test the code first
        
        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")

        # refresh. better turn this into a method
        self.entry_view.clear()
        self.entry_view.addItems(self.col.find().distinct("name"))

    # don't forget to create contexts for databases too!

    def __upload(self):
        self.fol = QFileDialog.getExistingDirectory(self,"Specify your data directory")
        if(len(self.fol) == 0): # almost forgot about the cancel culture
            print("no, gtfo")
            return

        print(self.fol)

        push = path_walk(self.fol) # get all dir
        main_path = pathlib.Path(self.fol)
        print(len(main_path.parts),main_path.parts)
        col_list = list()

        for x in push:
            col_list.append(x.parts[len(main_path.parts)]) # get each main dir, should be next from the folder paths
        
        col_list = [*set(col_list)] # get rid of dupes you idiot
        print(col_list)

        for x in col_list: # get col list
            col_temp = self.database[str(x)]
            for y in push: # get each elements
                if x == y.parts[len(main_path.parts)]: # check if folder name is the same or not
                    subpath = y.parts[y.parts.index(main_path.parts[-1])+1:len(y.parts) - 1] # get subfolders inside a folder
                    data_dict = {
                        "name": str(y.parts[-1]),
                        "subpath": '/'.join(subpath) if len(subpath) > 0 else -1,
                        "content": file_encode(y)
                    }
                    col_temp.insert_one(data_dict)

        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")

        self.col_view.clear() # refresh
        self.col_view.addItems(self.database.list_collection_names())

    def __download_col(self):
        self.fol = QFileDialog.getExistingDirectory(self,"Specify your data directory")
        if(len(self.fol) == 0): # almost forgot about the cancel culture
            print("no, gtfo")
            return

        for y in self.col.find():
            # first, check whether a subfolder exist or not
            #subpath = self.fol + "/" + y['subpath'] if type(y['subpath']) is str else -1
            subpath = "/".join([self.fol, y['subpath']]) if type(y['subpath']) is str else -1
            if subpath != -1:
                if not os.path.exists(subpath):
                    os.makedirs(subpath)
            #fullsub = self.fol + "/" + y['subpath'] + "/" + y['name'] if y['subpath'] != -1 else self.fol + "/"  + y['name']
            fullsub = "/".join([self.fol,y['subpath'],y['name']]) if y['subpath'] != -1 else "/".join([self.fol,y['name']])
            file_decode(fullsub, y['content'])
        
        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")

    def __download_entry(self):
        self.fol = QFileDialog.getExistingDirectory(self,"Specify your data directory")
        if(len(self.fol) == 0): # almost forgot about the cancel culture
            print("no, gtfo")
            return

        # great. self.entry.name concatenate collection name for its return
        # alright. let's process it first so self.col can find it
        txt = '.'.join(str.split(self.entry.name,'.')[-2:]) # get the name of the file

        for y in self.col.find({"name":txt}):
            #fullsub = self.fol + "/" + y['subpath'] + "/" + y['name'] if y['subpath'] != -1 else self.fol + "/"  + y['name']
            fullsub = "/".join([self.fol,y['name']])
            file_decode(fullsub, y['content'])
        
        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")

    def __download(self):
        self.fol = QFileDialog.getExistingDirectory(self,"Specify your data directory")
        if(len(self.fol) == 0): # almost forgot about the cancel culture
            print("no, gtfo")
            return
        # uh.. how are we going to do this?
        # create a folder using list_collection_names as a name
        # -> dump the data from each collections -> repeat till done
        col_names = self.database.list_collection_names()
        print(self.fol, type(self.fol))

        for x in col_names:
            col_temp = self.database[str(x)]
            download_path = self.fol + '/' + x + '/'
            # rewrite this to checks for existing directory you dork
            if not os.path.exists(download_path):
                os.mkdir(download_path)

            for y in col_temp.find():
                #subpath = self.fol + "/" + x + "/" + y['subpath'] if type(y['subpath']) is str else -1
                subpath = "/".join([self.fol,x,y['subpath']]) if type(y['subpath']) is str else -1
                if subpath != -1:
                    if not os.path.exists(subpath):
                        os.makedirs(subpath)
                fullsub = "/".join([self.fol,x,y['subpath'],y['name']]) if y['subpath'] != -1 else "/".join([self.fol,x,y['name']])
                file_decode(fullsub, y['content'])

        self.mongo_status.setText("Status: Done")
        self.mongo_status.setStyleSheet("color: green")
    
    def test(self):
        print("Hello there")
        if self.col == None:
            print("Collection hasn't been pressed yet")
        else:
            print(self.col)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
    del window # prevent memory leak