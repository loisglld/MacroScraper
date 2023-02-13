# -*- coding: utf-8 -*-

"""
Logs.py

Created on 2023-02-03
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
        Initialise les logs de l'application.
        
        Crée un fichier MacroLogs.log dans lequel se trouvera un
        historique des actions réalisées lors de la session.
        """     
        
        self.logLlevel = logging.DEBUG # Configure log error level
        self.logName = "MacroLogs"
        self.logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" # Display format in the log
        self.logDateFormat = "%Y-%m-%d %I:%M:%S"
        self.logOutPath = "../logs/"
        self.logPath = os.path.join(self.logOutPath, self.logName + ".log")

        # Delete the latest log file and create a new one to avoid conflict between the .log file
        try:
            os.remove(self.logPath)
        except OSError as e:
            print(e)
        
        self.log = logging.getLogger(self.logName)
        self.log.setLevel(self.logLlevel)
        logging.basicConfig(filename=self.logPath, format=self.logFormat, datefmt=self.logDateFormat, level=self.logLlevel)
    
    def refreshLog(self):
        # Actualize the log file
        now = datetime.now()  # Current date and hour
        logFileName = "MacroLogs" + ".log"
        logFNPath = os.path.join(self.logOutPath, logFileName)
        logOfTheDayNamePath = os.path.join(self.logFolderPath, now.strftime("%d-%m-%Y.log"))
        
        # Copy each line of the log file in the log of the day
        with open(logOfTheDayNamePath, "a", encoding="UTF-8") as logOfTheDay, open(logFNPath, "r", encoding="UTF-8") as logOfSession:
            for line in logOfSession:
                logOfTheDay.write(line)
                
            # Separate each session in the log of the day
            logOfTheDay.write("--------------------------------------------------------------\n")
            # Close files
            logOfTheDay.close()
            logOfSession.close()