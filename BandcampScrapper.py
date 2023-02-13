# -*- coding: utf-8 -*-

"""
MacroScrapper.py

Created on 2023-02-03
Author: Loïs GALLAUD

This programme is a scrapper for Bandcamp. 
It allows you to download all the albums of a band.
"""

#------------------------------------------------------------------------------#

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from zipfile import ZipFile 

import requests
import pandas as pd

import random
from time import sleep
from pathlib import Path

from warnings import filterwarnings
import codecs
import shutil
import os

#------------------------------------------------------------------------------#

def parent_dir(dir:str):
    dir_list = list(dir)
    while dir_list[-1] != '\\':
        dir_list.pop()
    return "".join(dir_list)

def clickWithSelenium(xpath:str, method=By.XPATH):
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((method, xpath)))
    random_sleep()
    driver.find_element(method, value=xpath).click()
    
def seleniumSecurity(xpath:str, seleniumOrder=clickWithSelenium, method=By.XPATH):
    order_tries = 0
    no_error = False
    while not no_error:
        try:
            seleniumOrder(xpath, method)
            no_error = True
        except NoSuchElementException:
            print("NO SUCH ELEMENT ERROR:\nNouvelle tentative...")
            order_tries += 1
        except TimeoutException:
            print("TIMEOUT ERROR:\nNouvelle tentative...")
            order_tries += 1
        except ElementClickInterceptedException:
            print("CLICKINTERCEPTION ERROR:\nNouvelle tentative...")
            order_tries += 1
            
        if order_tries >= 3:
            print("\nLa page Spotify a mis trop de temps à répondre.\n\nFermeture du programme...")
            driver.quit()
            exit()
            
def seleniumSecuritySendKey(entrybox, send_keys_arg):
    order_tries = 0
    no_error = False
    while not no_error:
        try:
            entrybox.send_keys(send_keys_arg)
            no_error = True
        except TimeoutException:
            print("TIMEOUT ERROR:\nTStarting a new tentative...")
            order_tries += 1
            
        if order_tries >= 3:
            driver.quit()
            exit()

def create_folder(name):
    folder_name = f"\\{name}"
    no_error = False
    while not no_error:
        try:
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + f"\\Music" + folder_name) # Crée le dossier
            no_error = True
        except:
            print(f"\nUne erreur est survenue: le dossier existe déjà !")
            shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + f"\\Music" + folder_name)
            print(f'Suppression du mauvais dossier...')
            print(f"Création du nouveau dossier...")
    return folder_name

def proxiesInit():
	print("Récupération du proxy...")

	get_proxy = requests.get("https://free-proxy-list.net") # Va sur le site de proxies gratuits

	proxy_list = pd.read_html(get_proxy.text)[0]
	proxy_list["url"] = "http://" + proxy_list["IP Address"] + ":" + proxy_list["Port"].astype(str)

	return proxy_list[proxy_list["Https"] == "yes"] # On copie ici avec pd.DataFrame pour pouvoir ajouter proprement une colonne ensuite

def get_good_proxies(url_to_try):
    good_proxies = set()

    for proxy_url in proxiesInit()["url"]:
        proxies = {"http": proxy_url, "https": proxy_url,}
        try:
            requests.get(url_to_try, proxies=proxies, timeout=1)
            good_proxies.add(proxy_url)
            print(f"PROXY {proxy_url} OK.")
        except Exception:
            pass

        if len(good_proxies) >= 1:
            break

    if len(good_proxies) == 0:
        print("Le programme n'a pas trouvé de proxy qui fonctionne.\nFin du programme.")
        exit()
        
    return good_proxies

def is_IP_OK(driver):
	try:
		driver.get("https://httpbin.org/ip")
		good_proxy_IP = driver.find_element(by = By.XPATH, value = '/html/body/pre').text
		assert good_proxy_IP != '''{
		"origin": "92.92.29.202"
		}'''
		print("L'IP utilisateur couverte.")
	except:
		print("L'adresse IP n'a pas été changée..\nPasse au proxy suivant.\n")
		return False
	return True

def is_useragent_OK(driver):
	try:
		driver.get("https://httpbin.org/user-agent")
		good_proxy_useragent = driver.find_element(by = By.XPATH, value = '/html/body/pre').text
		assert good_proxy_useragent != '''{
		"user-agent": "python-requests/2.26.0"
		}'''
		print("L'user-agent utilisateur est couvert.")
	except:
		print("Le user-agent n'a pas été changé..\nPasse au proxy suivant.\n")
		return False
	return True

def is_proxies_OK(good_proxies):
    verified_proxies = []
    print("==============================\n\nLancement de la procédure de vérification des proxy...\n")
 
    for index_good_proxy in range(len(good_proxies)):
        print(f"PROXY : {index_good_proxy+1}/{len(good_proxies)}\n------------------------------")
        # Initialisation du driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--proxy-server=%s' % list(good_proxies)[index_good_proxy]) # Intègre la bonne adresse IP
        chrome_options.add_argument("--headless") # Ouvre en arrière-plan la fenêtre
        driver_init = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options) # Ouvre la page web

        if index_good_proxy == 1: # Problème d'écriture dans le shell réglée par cette ligne de code
            print('') # Pour la lisibilité de la console

        if is_IP_OK(driver_init) == True and is_useragent_OK(driver_init) == True:
            verified_proxies.append(list(good_proxies)[index_good_proxy])
            print(f'{list(good_proxies)[index_good_proxy]} a été ajouté à la liste des proxy sûrs.\n')
        else:
            print("Le programme n'a pas trouvé de proxy qui fonctionne.\nFin du programme.")
            exit()
    return verified_proxies

def random_sleep():
	return random.random()/10**2

#----------------------------------------------------------------------------------------------------------------------------------# Initialisation

print("Début du programme.")

filterwarnings("ignore", category=DeprecationWarning) # Nettoie le terminal des erreurs de versions éventuelles
downloads_path = Path(str(Path.home() / "Downloads"))

url_to_try = "https://bandcamp.com" # Vérifie que les proxy fonctionnent sur le site bandcamp
verified_proxies = is_proxies_OK(get_good_proxies(url_to_try)) # Vérifie que l'utilisateur soit bien caché derrière l'IP et l'user-agent de tous les proxy utilisables

opt = Options()
ua = UserAgent()
userAgent = ua.random
opt.add_argument(f'user-agent={userAgent}')
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
print("Chargement du nouveau UserAgent...")

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_experimental_option('excludeSwitches', ['enable-logging']) # Enlève les "listening on ..." de la console
chrome_opt.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_opt.add_experimental_option('useAutomationExtension', False)
chrome_opt.add_argument("--disable-blink-features=AutomationControlled")
print("Passage à travers les Captcha...")

chrome_opt.add_argument('--proxy-server=%s' % verified_proxies[0]) # Intègre la bonne adresse IP
print("Chargement de la nouvelle adresse IP...")

chrome_opt.add_experimental_option("detach", True) # Laisse la page Chrome ouverte
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_opt, chrome_options = opt) # Ouvre la page web
print("\nLancement de la page web...")

os.system('cls') 

#----------------------------------------------------------------------------------------------------------------------------------# Execution

driver.get(f"https://bandcamp.com")
entrybox = driver.find_element(by = By.XPATH, value = '//*[@id="corphome-autocomplete-form"]/form/input[1]') # Clique sur l'entrybox
artist_name = input("IL EST IMPORTANT D'ECRIRE EXACTEMENT LE NOM DE L'ARTISTE\nEntrez le nom de l'artiste: ")
seleniumSecuritySendKey(entrybox, artist_name) # Ecrit l'input utilisateur
seleniumSecuritySendKey(entrybox, Keys.RETURN) # Valide
seleniumSecurity('//*[@id="filter-b"]/span') # Clique sur artiste et label
seleniumSecurity('//*[@id="pgBd"]/div[1]/div[1]/div/ul/li[1]/div/div[2]/a') # Clique sur la première proposition
artist_name = driver.find_element(by = By.XPATH, value = '//*[@id="band-name-location"]/span[1]').text # Récupère le véritable nom de l'artiste, histoire d'être sûr
driver.get(str(driver.current_url) + '/music') # Va dans la discographie de l'artiste
albums_names = driver.find_element(by = By.XPATH, value = '//*[@id="music-grid"]').text # Récupère le nom de tous les albums de l'artiste présents sur Bandcamp

# Ecrit le nom de tous les albums das un fichier texte
try: # Si le fichier n'existe pas
    with codecs.open(f"Text\\{artist_name}.txt", "x", "utf-8") as f:
        f.write(albums_names)
        album_list = f.readlines()
        f.close()
except: # Si le fichier est déjà existant
    with codecs.open(f"Text\\{artist_name}.txt", "r", "utf-8") as f:
        album_list = f.readlines()
        f.close()

unable_to_dl_albums = []
folder_name_for_artist = create_folder(artist_name)
folder_name_for_zip = create_folder(f"\\{artist_name}\\zip")
listbox_count = 1  

for i in range(len(album_list)):
    entrybox = driver.find_element(by = By.XPATH, value = '//*[@id="main-search-container"]/form/input[1]') # Trouve l'entrybox
    
    seleniumSecuritySendKey(entrybox, artist_name + ' ' + album_list[i]) # Tape le nom de l'album dans l'entrybox
    seleniumSecurity(f'//*[@id="pgBd"]/div[1]/div[1]/div/ul/li[{listbox_count}]/div/div[2]/a') # Clique sur la première entrée
    
    # Vérifie que c'est le bon album qui va se télécharger
    listbox_count = 1
    while driver.find_element(by = By.XPATH, value = '//*[@id="name-section"]/h2').text != album_list[i].strip():
        entrybox = driver.find_element(by = By.XPATH, value = '//*[@id="main-search-container"]/form/input[1]')
        seleniumSecuritySendKey(entrybox, artist_name + ' ' + album_list[i]) # Tape le nom de l'album dans l'netrybox
        seleniumSecurity(f'//*[@id="pgBd"]/div[1]/div[1]/div/ul/li[{listbox_count}]/div/div[2]/a') # Clique sur la première entrée
        listbox_count += 1
        
    # Vérifie que l'album est bien gratuit et donc téléchargeable
    if driver.find_element(by = By.XPATH, value = '//*[@id="trackInfoInner"]/ul/li[1]/div[3]/h4[1]/span').text != "proposez un prix":
        unable_to_dl_albums.append(album_list[i].strip())
        print(f"\nL'album {album_list[i].strip()} n'a pas pu être téléchargé car il recquiert d'être acheté...\n")
        continue

    folder_name_for_extracted = create_folder(f"\\{artist_name}\\{album_list[i].strip()}")
    seleniumSecurity('//*[@id="trackInfoInner"]/ul/li[1]/div[3]/h4[1]/button') # Clique sur acheter l'album
    entrybox_price = driver.find_element(by = By.XPATH, value = '//*[@id="userPrice"]') # Trouve l'entrybox pour rentrer un prix
    seleniumSecuritySendKey(entrybox_price, '0') # Demande à payer 0
    seleniumSecuritySendKey(entrybox_price, Keys.RETURN) # Entrée
    seleniumSecurity('//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[3]/div') # Clique sur aller sur la page de téléchargement
    seleniumSecurity('//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[4]/ul/li[3]/span[2]') # Choisit le format .flac
    seleniumSecurity('//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/span/a') # Clique sur télécharger
    
    print("=================================================")
    print(f"Album {i+1}/{len(album_list)}")
    print('\nTéléchargement de ' + album_list[i].strip() + '...')
    
    album_path = str(downloads_path) + f'\\{artist_name} - {album_list[i].strip()}.zip'
    
    while not os.path.isfile(album_path):
        sleep(2)
    
    # Coupe et colle le fichier zip au bon endroit
    new_album_path = str(os.path.abspath(os.getcwd())) + f'\\Music\\{folder_name_for_zip}\\{artist_name} - {album_list[i].strip()}.zip'
    shutil.copyfile(album_path, new_album_path)
    os.remove(album_path)
    
    with ZipFile(new_album_path, 'r') as zip: 
        zip.printdir()
        print('Extraction...') 
        zip.extractall(str(os.path.abspath(os.getcwd())) + f'\\Music\\{folder_name_for_extracted}') 
        print('Terminé! \n')

print("=================================================")
print("Liste des album payants restants à télécharger:")
for k in range(len(unable_to_dl_albums)):
    print(f"{k+1}- {unable_to_dl_albums[k]}")
    
driver.quit()    
    
print("Fin du programme.")