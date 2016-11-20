# TVFreak
A python application to extract links for TV Shows

## Features ##
* Allows you to search for tv shows
* Allow you to select seasons of the given tv shows
* generate text file containing the links of all the video of the selected season

## Requirements ##
* python2
* beautifulsoup4
* requests
* fuzzywuzzy
* termcolor
* python-Levenshtein

## Installation ##
``sudo python setup.py install``
[Make sure you are using python2]

## Usage ##
``tvfreak tv_show_name``

tv_show_name = any TV show name

### Example ###
``tvfreak sherlock``


## OUTPUT ##
The output will be a folder containing the name of the TVShow you have given

## HOW TO DOWNLOAD USING THE GENERATED TEXT FILES ##

* You can download <a href="http://ugetdm.com/downloads/" target = "_blank">UGET</a> for any platform
* Install UGET
* Open UGET
* Goto ``File > Batch Downloads > Text File Import(.txt) ..``
* Import the desired text file and continue as per the instructions


**NOTE:** Works on Linux only.
