# **MacroScrapper**

## **Table of content**

* What is MacroScrapper?
* Where does it come from?
* How does it work?
* How to use it?
* How to contribute?
* License

## **What is MacroScrapper?**

MacroScrapper is a web scrapper for Bandcamp music. It is a Python script that will download all the music from a Bandcamp artist page, album after album, in your Music directory.

## **Where does it come from?**

![Macroblank Bandcamp banner](./images/macro-banner.png)

MacroScrapper is a project I made for my personal use. I wanted to download all the music from a Bandcamp artist page named [Macroblank](https://macroblank.bandcamp.com/). I didn't want to download the music one by one so I decided to make a script that would do it for me.
That is why the script is named MacroScrapper.

## **How does it work?**

The script will use the [Selenium](https://www.selenium.dev/) library to open a Chrome browser. It will then navigate to the Bandcamp artist page and click on the "Download" button of each album. The script will then use the [Requests](https://requests.readthedocs.io/en/master/) library to download the album. The script will then repeat the process for each album.

Each album will be downloaded in a separate folder. The folder will be named after the album name. The album will be downloaded in a ``.zip`` file then extracted in the folder with the same name as the album.

It will create a ``.csv`` file with the name of the artist and the name of the album. The file will contain the following information:

* Album name
* Album URL
* Album release date
* Album price
* Album genre
* Album tracklist

It will also create a ``.txt`` file with the name of the artist and the name of the album. The file will contain the following information:

* Download date
* Album name
* Artist name
* Album tracklist

The project will download the music in yout Music folder. It will create a folder named MacroScrapper and then create a folder named after the artist's name. The folder will contain all the albums downloaded as zip files and the ``.csv`` and ``.txt`` files.

### **Directory structure**

```bash
Music   
.
|___ MacroScrapper
    |___ Artist1
        |___ Album1
        |___ Album2
        |___ ...
        |___ Zips
    |___ Artist2
        |___ Album1
        |___ Album2
        |___ ...
        |___ Zips
    |___ ...
```

## How to use it?

### Requirements

Python verion 3.11.1 or higher is required.

Requirements are detailed in the ``requirements.txt`` file. You will need:

* webdriver-manager
* selenium
* requests
* pandas

### Installation

* Clone the repository
* Install the requirements with ``pip install -r requirements.txt``

### Usage

* Run the script with `python main.py`
* Enter the name of the artist in the terminal.
* Wait for the script to finish.

## How to contribute?

[I](https://github.com/LOISGALLAUD) develop the MacroScrapper alone. I welcome both pull requests and issues on [GitHub](https://github.com/LOISGALLAUD/MacroScrapper). I will review your pull request as soon as possible.

## License

MacroScrapper is licensed under the [Apashe 2.0 License].
