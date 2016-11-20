# @Author: ganeshkumarm
# @Date:   2016-11-20T00:14:22+05:30
# @Last modified by:   ganeshkumarm
# @Last modified time: 2016-11-20T08:18:39+05:30

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from termcolor import colored
import exception
import requests
import sys
import re
import os

class Serial(object):
    serial_name = ''
    serial_num = 0
    search_word = ''
    def __init__(self, search_word):
        Serial.search_word = search_word
        self.url = 'http://dl.vahidfilm.com/Serial/'
        #self.url = 'http://s1.bia2m.biz/Series/'
        self.serialList()

    def serialList(self):
        print colored("Searching for " + Serial.search_word.upper() + " ...", 'yellow')
        response = requests.get(self.url)
        content = BeautifulSoup(response.content, "lxml")
        self.serial_list = {}
        i = 1
        for a in content.find_all('a', href = True):
            self.serial_list[i] = list([a.string[:-1], str(self.url + a['href'])]) # omit slash at last and add link to dictionary
            i += 1

    def search(self, search_word):
        temp_serial_list = {}
        for key in self.serial_list:
            serial_name = self.serial_list[key][0]
            serial_url = self.serial_list[key][1]
            if fuzz.partial_ratio(search_word.lower(), serial_name.lower()) >= 85:
                temp_serial_list[key] = list([serial_name, serial_url])
        if temp_serial_list == {}:
            print colored("Sorry, No similar serials ...", 'red')
            return

        for key in temp_serial_list:
            print colored(key, 'green') + ' ' + temp_serial_list[key][0]

        self.selectSerial(temp_serial_list)

    def selectSerial(self, temp_serial_list):
        serial_num = raw_input(colored("Enter any serial number to continue: ", 'cyan'))
        if not serial_num.isdigit():
            try:
                raise exception.InvalidEntry("Enter only positive numbers")
            except exception.InvalidEntry, e:
                print colored(e.args, 'red')
                self.selectSerial(temp_serial_list)
        serial_num = int(serial_num)
        if serial_num not in temp_serial_list.keys():
            print colored("Enter a valid serial number", 'red')
            self.selectSerial(temp_serial_list)
        Serial.serial_num = serial_num
        Serial.serial_name = temp_serial_list[serial_num][0]
        self.seasonList(temp_serial_list, serial_num)

    def seasonList(self, temp_serial_list, serial_num):
        serial_name = temp_serial_list[serial_num][0]
        serial_url = temp_serial_list[serial_num][1]
        print "Displaying season list of " + colored(serial_name, 'yellow')
        response = requests.get(serial_url)
        season_content = BeautifulSoup(response.content, "lxml")
        season_list = {}
        i = 1
        for a in season_content.find_all('a', href = True):
            season_list[i] = list([a.string[:-1], str(serial_url + a['href'])]) # omit slash at last and add link to dictionary
            i += 1

        for key in season_list:
            if re.match('[s, S].*', season_list[key][0]):
                print colored(key, 'green') + ' ' + season_list[key][0]
        self.selectSeason(season_list, temp_serial_list)

    def selectSeason(self, season_list, temp_serial_list):
        season_num = raw_input(colored("Enter any season number to continue (Enter 0 to select all seasons): ", 'cyan'))
        if not season_num.isdigit():
            try:
                raise exception.InvalidEntry("Enter only positive numbers")
            except exception.InvalidEntry, e:
                print colored(e.args, 'red')
                self.selectSeason(season_list, temp_serial_list)

        season_num = int(season_num)
        if season_num != 0 and season_num not in season_list.keys():
            self.selectSeason(season_list)
        self.loadSeason(season_list, season_num, temp_serial_list)

    def loadSeason(self, season_list, season_num, temp_serial_list):
        Serial.serial_name = '_'.join(Serial.serial_name.split(' '))
        if not os.path.exists(Serial.serial_name):
            os.system("mkdir " + Serial.serial_name)
        if season_num == 0:
            for i in season_list:
                self.generateTextFile(i, season_list)
        else:
            self.generateTextFile(season_num, season_list)
        self.userPrompt(season_list, temp_serial_list)

    def generateTextFile(self, season_num, season_list ):
        if re.match('[s, S].*', season_list[season_num][0]) == None:
            return
        season_name = season_list[season_num][0]
        season_url = season_list[season_num][1]
        response = requests.get(season_url)
        video_content = BeautifulSoup(response.content, "lxml")
        links = []
        for a in video_content.find_all('a', href = True):
            if a['href'].endswith('mkv') or a['href'].endswith('mp4') or a['href'].endswith('avi'):
                links.append(season_url + a['href'])

        season_name = season_name + '.txt'
        if os.path.exists(Serial.serial_name + '/' + season_name):
            os.system("rm -rf " + season_name)

        with open(Serial.serial_name + '/' + season_name, 'w') as f:
            for link in links:
                f.write(link + '\n')
        print colored("Created " + Serial.serial_name + '/' + season_name, 'green')

    def userPrompt(self, season_list, temp_serial_list):
        print colored("1. ", 'green') + "Season List"
        print colored("2. ", 'green') + "Search other serial"
        print colored("3. ", 'green') + "Quit"
        option = raw_input(colored("Enter your option: ", 'magenta'))
        option = int(option)
        if option == 1:
            self.seasonList(temp_serial_list, Serial.serial_num)
        elif option == 2:
            search_word = raw_input(colored("Enter a serial name to search: ", 'cyan'))
            self.search(search_word)
        elif option == 3:
            print colored("Bye", 'green')
            sys.exit()
        else:
            print colored("Select a valid option", 'red')
            self.userPrompt(season_list)
def main():
    try:
        if len(sys.argv) == 1:
            try:
                raise exception.NoParameterException("Pass any serial name as command line argument")
            except exception.NoParameterException, e:
                print colored(e.args, 'red')
                sys.exit()
        search_word = ''
        for i in range(1, len(sys.argv)):
            search_word += sys.argv[i]
        serial = Serial(search_word)
        serial.search(search_word)
    except KeyboardInterrupt:
        print colored("\nQuitting ...", 'green')
        print colored("Bye", 'green')

if __name__ == "__main__":
    main()
    
