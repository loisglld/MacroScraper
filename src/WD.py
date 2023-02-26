# -*- coding: utf-8 -*-

"""
WD.py

Created on 2023-02-04
Author: Loïs GALLAUD
This scripts contains the WorkingDirectory class.
"""

#------------------------------------------------------------------------------#

import os

#------------------------------------------------------------------------------#

class WorkingDirectory:
    """
    This class represents the working directory inside user's computer.
    It contains the different directory which will stock the albums, covers.
    
    Music   
    .
    |___ MacroScraper
        |___ Artist
            |___ Album1
            |___ Album2
            |___ ...
            |___ Zips
    """
    def __init__(self):
        """
        Constructor of the WorkingDirectory class.
        """
        self.path = os.path.join(os.environ['USERPROFILE'], "Music\\MacroScraper\\")
        self.downloadsPath = os.path.join(os.environ['USERPROFILE'], "Downloads\\")
        # Crée le dossier MacroScraper dans le dossier Musique de l'utilisateur
        if not os.path.exists(self.path): os.makedirs(self.path)

    def createArtistDir(self, artist):
        """
        Creates the artist's working directory.
        """
        self.artistPath =  self.path + artist + "\\"
        if not os.path.exists(self.artistPath): os.makedirs(self.artistPath)
        
    def createAlbumDir(self, album):
        """
        Creates the album's working directory.
        """
        self.albumPath = self.artistPath + "\\" + album + "\\"
        if not os.path.exists(self.albumPath): os.makedirs(self.albumPath)
        
    def createZipDir(self):
        """
        Creates the zip's working directory.
        """
        self.zipPath = self.artistPath + "\\Zips\\"
        if not os.path.exists(self.zipPath): os.makedirs(self.zipPath)
                
    def __str__(self):
        """
        Return the string representation of the WorkingDirectory class.
        """
        return "WorkingDirectory(" + self.path + ")"

    def __repr__(self):
        """
        Return the string representation of the WorkingDirectory class.
        """
        return "WorkingDirectory(" + self.path + ")"

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    wd = WorkingDirectory()