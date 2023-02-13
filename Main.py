# -*- coding: utf-8 -*-

"""
Main.py

Created on 2023-02-03
Author: Loïs GALLAUD

This program is a scrapper for Bandcamp. 
It allows you to download all the albums of a band.
"""

#------------------------------------------------------------------------------#

from MacroScrapper import MacroScrapper

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    # Ignore the DeprecationWarning
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Create the MarcoScrapper
    macroScrapper = MacroScrapper()
    macroScrapper.start()

    # End of the program
    print("End of the program.")