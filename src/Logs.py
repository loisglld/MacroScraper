# -*- coding: utf-8 -*-

"""
Logs.py

Created on 2023-02-15
Author: Loïs GALLAUD
This scripts contains the Logs class.
"""

#------------------------------------------------------------------------------#

import logging
import os
import datetime

#------------------------------------------------------------------------------#
class Logs:
    """
    This class represents the logs of the application.
    """
    def __init__(self):
        """
        Constructor of the Logs class.
        """
        
        self.logLevel = logging.INFO # Configure log error level
        self.logName = "MacroLogs"
        self.logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" # Display format in the log
        self.logDateFormat = "%Y-%m-%d %I:%M:%S"
        self.logOutPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "\\logs\\" # Path of the log file
        self.logPath = os.path.join(self.logOutPath, self.logName + ".log")

        if not os.path.exists(self.logOutPath):
            os.makedirs(self.logOutPath)
            print("The logs folder has been created.")
        else: 
            print("The logs folder already exists.")

        # Delete the latest log file and create a new one to avoid conflict between the .log file
        try:
            os.remove(self.logPath)
        except OSError:
            pass
        
        self.log = logging.getLogger(self.logName)
        self.log.setLevel(self.logLevel)
        logging.basicConfig(filename=self.logPath, format=self.logFormat, datefmt=self.logDateFormat, level=self.logLevel)
    
    def refreshLogs(self):
        """
        Add to the log of the day the log of the passed session.
        """
        # Actualize the log file
        now = datetime.datetime.now() # Current date and hour
        logOfTheDayNamePath = os.path.join(self.logOutPath, now.strftime("%d-%m-%Y.log"))
        
        # Copy each line of the log file in the log of the day
        with open(logOfTheDayNamePath, "a", encoding="UTF-8") as logOfTheDay, open(self.logPath, "r", encoding="UTF-8") as logOfSession:
            for line in logOfSession:
                logOfTheDay.write(line)
                
            # Separate each session in the log of the day
            logOfTheDay.write("--------------------------------------------------------------\n")
            # Close files
            logOfTheDay.close()
            logOfSession.close()
            