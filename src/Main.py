# -*- coding: utf-8 -*-

"""
Main.py

Created on 2023-02-03
Author: Loïs GALLAUD

This program is a Scraper for Bandcamp. 
It allows you to download all the albums of a band.
"""

#------------------------------------------------------------------------------#

from MacroScraper import MacroScraper
from Logs import Logs

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    # Ignore the DeprecationWarning
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Initialize the logs
    logs = Logs()
    
    # Create the MarcoScraper
    macroScraper = MacroScraper(logs)
    macroScraper.start()

    # End of the program
    print("End of the program.")