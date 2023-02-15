# -*- coding: utf-8 -*-

"""
Proxy.py

Created on 2023-02-03
Author: Loïs GALLAUD
This scripts contains the Proxy class.
"""

#------------------------------------------------------------------------------#

from Driver import Driver
from Identity import Identity

import requests
import pandas as pd

#------------------------------------------------------------------------------#

class Proxy:
    """
    This class represents the Proxy the MacroScrapper will use to navigate on bandcamp.
    """
    def __init__(self):
        """
        Constructor of the Proxy class.
        """
        self.computerIdentity = Identity()
        self.computerIP = self.computerIdentity.ipAdress
        self.computerUserAgent = self.computerIdentity.userAgent

        self.bandcamp_url = "https://bandcamp.com/"
        self.url = "https://free-proxy-list.net/"
        self.proxies = self.is_proxies_safe(self.get_good_proxies(1))

    def proxiesInit(self):
        """
        Initialize the list of proxies. 
        """

        # Get the proxies into a DataFrame
        proxy = requests.get(self.url)
        proxy_list = pd.read_html(proxy.text)[0]
        # Add the url column
        proxy_list["url"] = "http://" + proxy_list["IP Address"] + ":" + proxy_list["Port"].astype(str)

        return proxy_list[proxy_list["Https"] == "yes"]

    def get_good_proxies(self, amount_of_proxies):
        """
        Try to get a good proxy by launching in the background the bandcamp url.
        If the web page returns a 200 status code, the proxy is good.

        If the proxy is good, it will be added to the list of good proxies.
        
        Args:
            amount_of_proxies (int): amount of proxies the user wants to test.

        Returns:
            list: list of proxies which work on the given website.
        """

        good_proxies = set() # Initialise un dictionnaire vide avec que des clefs

        for proxy_url in self.proxiesInit()["url"]:
            proxy = {"http": proxy_url, "https": proxy_url,}
            try:
                requests.get(self.bandcamp_url, proxies=proxy, timeout=1)
                good_proxies.add(proxy_url)
                print(f"PROXY {proxy_url} OK.")
            except Exception:
                print(f"PROXY {proxy_url} KO.")
                pass

            # Stop looking for proxies if there is enough proxies
            if len(good_proxies) >= amount_of_proxies:
                break

        if not len(good_proxies):
            print("Program stopped because there is no good proxy.\nEnd of the program.")
            exit()
            
        return good_proxies

    def is_proxies_safe(self, proxies):
        """
        Verify if the proxies are safe by launching in the background the bandcamp url.
        If the web page returns a different IP adress and a different user-agent which
        correspond to python's request, the proxy is safe.

        Args:
            proxies (list): list of proxies which work on the given website.

        Returns:
            list: list of proxies which have been double checked (IP adress and user-agent) and are safe.
        """
        verified_proxies = []
        proxies = list(proxies)
        print(proxies)
        #print("==============================\n\nStarting verification of proxies\n\n==============================\n")
    
        for proxy in proxies:
            #print(f"PROXY : {index_good_proxy+1}/{N}\n==============================\n")
            driver = Driver(proxy)
            if self.is_IP_OK(driver):
                verified_proxies.append(proxy)
                print(f'{proxy} a été ajouté à la liste des proxy sûrs.\n')
            else:
                print("Le proxy n'est pas sûr.\n")
        
        if not len(verified_proxies):
            print("Program stopped because there is no safe proxy.\nEnd of the program.")
            exit()
        return verified_proxies

    def is_IP_OK(self, driver:Driver):
        """
        Verify if the IP adress is safe by launching in the background the bandcamp url.

        Args:
            driver (selenium.webdriver.chrome.webdriver.WebDriver): chrome's driver.

        Returns:
            bool: True if the IP adress covers user's IP adress, False otherwise.
        """
        try:
            # Get the IP adress of the user
            assert driver.getIPAdress() != self.computerIP
            print("IP is safe.")
        except:
            print("IP isn't safe..\nOn to the next proxy.\n")
            return False
        return True

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    proxy = Proxy()
    print(proxy.getProxies())