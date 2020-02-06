import os
import core

class Game(dict):
    def __init__(self, name, id, folder, parts):
        self.name = name
        self.id = id
        self.folder = folder
        self.parts = parts

    
