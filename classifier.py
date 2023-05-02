import cv2
import sqlite3
import database_operations as do

class classifier():

    def __init__(self, img_path):
        
        self.__db = do('big_boy.sqlite')
        self.__img_path = img_path

    def find_all(self):
        self.__db.make_table('rois', ['id INTEGER PRIMARY KEY', ''])
        

        pictures = self.__db.statement('SELECT * FROM images')