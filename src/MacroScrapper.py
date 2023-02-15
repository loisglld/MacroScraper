# -*- coding: utf-8 -*-

"""
MacroScrapper.py

Created on 2023-02-03
Author: Loïs GALLAUD
This scripts contains the MarcoScrapper class.
"""

#------------------------------------------------------------------------------#

from Proxy import Proxy
from Driver import Driver
from WD import WorkingDirectory
from Logs import Logs
from selenium.webdriver.common.keys import Keys

import os
import codecs
from zipfile import ZipFile 
import shutil
import time

#------------------------------------------------------------------------------#

class MacroScrapper:
    version = "0.2.0"
    def __init__(self):
        """
        Constructor of the MacroScrapper class.
        """
        self.artist_name = input("IL EST IMPORTANT D'ECRIRE EXACTEMENT LE NOM DE L'ARTISTE\nEntrez le nom de l'artiste: ")
        
        self.WD = WorkingDirectory()
        self.logs = Logs()
        self.proxies = Proxy()
        self.driver = Driver(self.proxies.proxies[0], show=True)
        
        self.logs.log.info(f"The MacroScrapper {MacroScrapper.version} has been launched.")
        
    def start(self):
        """
        This function starts the scrapping.
        """
        self.logs.log.info("The scrapping has started.")
        self.logs.log.info("The artist name is: " + self.artist_name)
        
        self.WD.createArtistDir(self.artist_name)
        self.WD.createZipDir(self.artist_name)
        
        # Go to the bandcamp website
        self.driver.goTo(self.proxies.bandcamp_url)  
        
        # Click the entry box
        entrybox = self.driver.getElement('//*[@id="corphome-autocomplete-form"]/form/input[1]')
        # Send the artist name
        self.driver.seleniumSecuritySendKey(entrybox, self.artist_name)
        # Validate the entry
        self.driver.seleniumSecuritySendKey(entrybox, Keys.RETURN)
        self.driver.seleniumClick(self.driver.getElement('//*[@id="filter-b"]/span'))
        # Click on the first proposition
        self.driver.seleniumClick(self.driver.getElement('//*[@id="pgBd"]/div[1]/div[1]/div/ul/li[1]/div/div[2]/a'))
        # Get the artist name from the page
        self.artist_name = self.driver.getElement('//*[@id="band-name-location"]/span[1]').text      
        # Stock the albums in a text file
        self.stockAlbums()
        self.logs.log.info("The albums have been stocked.")
        for i in range(len(self.album_list)):
            album_name = self.album_list[i].strip()
            self.goToAlbumPage(i)
            self.WD.createAlbumDir(self.artist_name, album_name)
            self.downloadAlbum(album_name, i)
            self.logs.log.info(f"{album_name} has been downloaded.")
        
        self.logs.refreshLogs()
    
    def stockAlbums(self):
        """
        This function stocks the albums in the artist's working directory.
        """
        # Go to the discography
        self.driver.goTo(str(self.driver.getCurrentURL()) + '/music')
        # Get the name of all the albums
        album_names = self.driver.getElement('//*[@id="music-grid"]').text
        self.writeAlbumsNames(album_names)
        
    def writeAlbumsNames(self, album_names):
        """
        This function stocks the albums names in a text file.
        """
        try: # Si le fichier n'existe pas
            with codecs.open(self.WD.artistPath + "albums_names.txt", "x", "utf-8") as f:
                f.write(album_names)
                self.album_list = f.readlines()
                f.close()
        except: # Si le fichier est déjà existant
            with codecs.open(self.WD.artistPath + "albums_names.txt", "r", "utf-8") as f:
                self.album_list = f.readlines()
                f.close()
            
    def goToAlbumPage(self, i):
        # Get the entry box
        entrybox = self.driver.getElement('//*[@id="main-search-container"]/form/input[1]')
        # Send the album name
        self.driver.seleniumSecuritySendKey(entrybox, self.artist_name + ' ' + self.album_list[i])
        listbox_count = 1
        # Click on the first proposition
        self.driver.seleniumClick(self.driver.getElement(f'//*[@id="pgBd"]/div[1]/div[1]/div/ul/li[{listbox_count}]/div/div[2]/a'))
        
        # Verify if the album name is the same as the one in the text file
        listbox_count = 1
        while self.driver.getElement('//*[@id="name-section"]/h2').text != self.album_list[i].strip():
            entrybox = self.driver.getElement('//*[@id="main-search-container"]/form/input[1]')
            self.driver.seleniumSecuritySendKey(entrybox, self.artist_name + ' ' + self.album_list[i]) # Tape le nom de l'album dans l'netrybox
            self.driver.seleniumClick(self.driver.getElement(f'//*[@id="pgBd"]/div[1]/div[1]/div/ul/li[{listbox_count}]/div/div[2]/a')) # Clique sur la première entrée
            listbox_count += 1
            
    def downloadAlbum(self, album_name, i):
        # Click on the "Buy Now" button
        self.driver.seleniumClick(self.driver.getElement('//*[@id="trackInfoInner"]/ul/li[1]/div[3]/h4[1]/button'))
        # Get the price entry box
        entrybox_price = self.driver.getElement('//*[@id="userPrice"]')
        # Send the price (0)
        self.driver.seleniumSecuritySendKey(entrybox_price, '0')
        # Validate the entry
        self.driver.seleniumSecuritySendKey(entrybox_price, Keys.RETURN)
        # Click on the "Download on your laptop" button
        self.driver.seleniumClick(self.driver.getElement('//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[3]/div'))
        # Select mp3 320 kbps format
        self.driver.seleniumClick(self.driver.getElement('//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[4]/ul/li[2]/span[2]'))
        # Click on the "Download" button
        self.driver.seleniumClick(self.driver.getElement('//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/span/a'))
        
        self.unzipAlbum(album_name, i)
    
    def unzipAlbum(self, album_name, i):
        print("=================================================")
        print(f"Album {i+1}/{len(self.album_list)}")
        print('\nDownloading ' + album_name + '...')
        
        album_path = self.WD.downloadsPath + f'\\{self.artist_name} - {album_name}.zip'
        
        while not os.path.isfile(album_path):
            time.sleep(2)
        
        # Cut and paste the album in the artist's working directory
        new_album_path =self.WD.zipPath + f'\\{self.artist_name} - {album_name}.zip'
        shutil.copyfile(album_path, new_album_path)
        os.remove(album_path)
        
        with ZipFile(new_album_path, 'r') as zip: 
            zip.printdir()
            print('Extracting...')
            zip.extractall(self.WD.albumPath) 
            print('Done! \n')