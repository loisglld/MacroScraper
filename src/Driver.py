# -*- coding: utf-8 -*-

"""
Driver.py

Created on 2023-02-03
Author: Loïs GALLAUD
This scripts contains the Driver class.
"""

#------------------------------------------------------------------------------#

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

import time
import random
import logging

#------------------------------------------------------------------------------#

class Driver:
    """
    This class represents a driver.
    This driver will naviguate through the pages of the bandcamp website with a given IP adress.
    """
    def __init__(self, proxy=None, show=False):
        """
        Constructor of the Driver class.
        """
        
        # Driver manager initialization
        self.chrome_driver_manager = ChromeDriverManager()

        # Chrome options initialization
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument('--log-level=3') # Clean Logs from webdriver_manager info messages
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        if proxy:
            self.chrome_options.add_argument(f'--proxy-server={proxy}')
        if not show:
            self.chrome_options.add_argument('--headless')

        # Open the browser
        self.driver = webdriver.Chrome(self.chrome_driver_manager.install(), options=self.chrome_options)
        #print("Driver initialized.")

    def getUserAgent(self):
        """
        Returns the user-agent of the user.
        """
        self.driver.get("https://httpbin.org/user-agent")
        return self.driver.find_element(by = By.XPATH, value = '/html/body/pre').text

    def getIPAdress(self):
        """
        Returns the IP adress of the user.
        """
        self.driver.get("https://httpbin.org/ip")
        return self.driver.find_element(by = By.XPATH, value = '/html/body/pre').text

    def goTo(self, url):
        """
        Goes to the given URL.
        """
        self.driver.get(url)

    def click(self, element):
        """
        Clicks on the element with the given xpath.
        
        Args (selenium.webdriver.remote.webelement.WebElement): to click on
        """
        time.sleep(random.random()/10**2)
        element.click()
    
    def getElement(self, xpath):
        """
        Returns the element with the given xpath.
        
        Args (str): xpath of the element to return
        
        Returns (selenium.webdriver.remote.webelement.WebElement): element with the given xpath
        """
        WebDriverWait(self.driver, 40).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath)

    def seleniumClick(self, element):
        """
        Waits for a random span of time and clicks on the given element.
        If the element is not clickable, the function will try again 3 times.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement): element to click on
        """
        randomSleep()
        order_tries = 0
        while order_tries < 3:
            try:
                element.click()
                return
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                order_tries += 1
                print(f"{e.__class__.__name__} - Nouvelle tentative...")
        # print("La page a mis trop de temps à répondre.\nFermeture du programme...")
        driver.quit()
        exit()

    def seleniumSecuritySendKey(self, entrybox, send_keys_arg):
        """
        Send keys to the given entrybox.

        Args:
            entrybox (selenium.webdriver.remote.webelement.WebElement): _description_
            send_keys_arg: _description_
        """
        randomSleep()
        order_tries = 0
        no_error = False
        while not no_error:
            try:
                entrybox.send_keys(send_keys_arg)
                no_error = True
            except TimeoutException:
                print("TIMEOUT ERROR:\nNouvelle tentative...")
                order_tries += 1
                
            if order_tries >= 3:
                print("\nLa page a mis trop de temps à répondre.\n\nFermeture du programme...")
                driver.quit()
                exit()

    def getCurrentURL(self):
        """
        Returns the current URL.
        """
        return self.driver.current_url

def randomSleep():
    """
    Sleeps for a random span of time.
    """
    time.sleep(random.random()/10**2)

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    driver = Driver(show=True)
    driver.goTo("https://bandcamp.com")
    print(type(driver.getElement('//*[@id="header-wrapper"]/div[1]/div[1]/div[1]/h2/a')))
    