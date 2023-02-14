# -*- coding: utf-8 -*-

"""
Identity.py

Created on 2023-02-03
Author: Loïs GALLAUD
This scripts contains the Identity class.
"""

#------------------------------------------------------------------------------#

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

#------------------------------------------------------------------------------#

class Identity:
    """
    This class represents the identity of user's computer on Internet.
    """
    def __init__(self):
        """
        Constructor of the Identity class.
        """
        # Driver manager initialization
        self.chrome_driver_manager = ChromeDriverManager()

        # Chrome options initialization
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_argument('--headless') # Launch in the background

        # Open the browser
        self.driver = webdriver.Chrome(self.chrome_driver_manager.install(), options = self.chrome_options) # Opens the browser

        # Get the user-agent
        self.driver.get("https://httpbin.org/user-agent")
        self.userAgent = self.driver.find_element(by = By.XPATH, value = '/html/body/pre').text

        # Get the IP adress
        self.driver.get("https://httpbin.org/ip")
        self.ipAdress = self.driver.find_element(by = By.XPATH, value = '/html/body/pre').text