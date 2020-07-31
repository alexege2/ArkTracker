from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import time
import os

class arkbot():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\alexe\bin\chromedriver.exe")

    def getData(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\alexe\bin\chromedriver.exe")
        print("--Pulling Information From Website--")

        #Create an empty watch, alert, and server list
        watch_list = []
        alert_list = []
        server_list = []
        alerts = ''
        
        #Populate watch list with contents of watchList.txt file
        with open('watchList.txt') as f:
            for line in f:
                watch_list.append(line)

        #Populate alerts list with contents of alertList.txt file
        with open('alertList.txt') as f:
            for line in f:
                alert_list.append(line)

        #Populate server list with contents of serverList.txt file
        with open('serverList.txt') as f:
            for line in f:
                server_list.append(line)

        #Append @ symbol to each name in list, so discord directly mentions the user
        for user in alert_list:
            alerts += "@" + user + " "

        #Log current time to MasterList file
        with open(f'MasterList.txt', 'a', encoding="utf-8") as f:
            f.write(datetime.now().strftime(f"\n---------%m/%d/%Y, %I:%M:%S %p---------\n"))

        #Delete MasterListCurrent so we get fresh information
        if os.path.exists("MasterListCurrent.txt"):
            os.remove("MasterListCurrent.txt")
            print("Removing master list file")

        #Loop through servers and pull information about active players
        for server in server_list:
            alerts = ''
            population = 0
            self.driver.get(f'https://www.battlemetrics.com/servers/ark/{server}')
            i = 0
            for table in self.driver.find_elements_by_xpath('//*[@id="serverPage"]/div[4]/div[1]/table'):
                server_data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
                print("Data:", server_data)
                server_output = ''

                #Get server population
                population = int(len(server_data)/3)

                #Only look at active members
                for x in range(2, len(server_data)):
                    if(i == 1):
                        if(server_data[x] in watch_list):
                            server_output += server_data[x] + " [" + server_data[x+1] + "] - " + alerts + "]\n"
                        else:
                            server_output += server_data[x] + " [" + server_data[x+1] + "]\n"
                    i += 1
                    if(i == 3):
                        i = 0
            
            print("current server:", server)
            #Write content to each individual file
            server = server.strip('\n')

            servers = {
                '7811424':"TheIsland",
                '7811410':"Ragnarok",
                '7811425':"Abberation",
                '7811427':"Valguaro",
                '7811428':"TheCenter",
                '7811429':"ScortchedEarth",
                '7811430':"Genesis",
                '7811412':'CrystalIsles',
                '7811433':"Extinction"
            }
                
            print("Current server:", servers[server])

            #Log to individual files
            with open(f'{servers[server]}Master.txt', 'a', encoding="utf-8") as f:
                f.write(datetime.now().strftime("\n---------%m/%d/%Y, %I:%M:%S %p---------\n"))
                if(len(server_output) > 0):
                    f.write(server_output)
                else:
                    f.write("No players online" + "\n")

            #Log to individual files
            with open(f'{servers[server]}Current.txt', 'w', encoding="utf-8") as f:
                f.write(datetime.now().strftime("\n---------%m/%d/%Y, %I:%M:%S %p---------\n"))
                if(len(server_output) > 0):
                    f.write(server_output)
                else:
                    f.write("No players online" + "\n")

            with open(f'MasterList.txt', 'a', encoding="utf-8") as f:
                f.write(f'\n-----[ {servers[server]} ]-----\n')

            #Log to master file
            with open(f'MasterList.txt', 'a', encoding="utf-8") as f:
                if(len(server_output) > 0):
                    f.write(server_output)
                else:
                    f.write("No players online" + "\n")

            #Log to master file
            with open(f'MasterListCurrent.txt', 'a', encoding="utf-8") as f:
                f.write("\n--------[ " + servers[server] + " ] --------\n")
                if(len(server_output) > 0):
                    f.write(server_output)
                else:
                    f.write("No players online" + "\n")
        
        #Finish Script. Close all windows
        self.driver.quit()

bot = arkbot()

#Run script at beginning of every minute
starttime = time.time()
while True:
    print("Running script at: " + str(datetime.now()))
    bot.getData()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))