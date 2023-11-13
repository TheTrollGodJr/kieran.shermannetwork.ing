from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil

letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","#"]
tableCount = 1
downloading = True
loading = True

print("Choose console game library to download:\nNES\nSMS\nGenesis\nSNES\nSaturn\nPS1\nN64\nDreamcast\nPS2\nXbox\nGameCube\nXbox360\nPS3\nWii\nWiiWare\nGB\nVB\nGBC\nGBA\nDS\nPSP\n\nTo select multiple consoles add a ',' then another console (eg. NES,SNES,Genesis)")
input = input("")

if "," in input:
    consoles = input.split(",")
    print(consoles)
else:
    consoles = [input]
    print(consoles)

#for items in consoles:
driver = webdriver.Chrome()
driver.get("about:blank")

for items in consoles:
    for letter in letters:
        print(f"\n{letter}\n")
        tableCount = 1
        if letter == "#":
            driver.execute_script(f"window.open('https://vimm.net/vault/?p=list&system={items}&section=number', '{letter}');")
            driver.switch_to.window(f"{letter}")
        else:
            driver.execute_script(f"window.open('https://vimm.net/vault/{items}/{letter}', '{letter}');")
            driver.switch_to.window(f"{letter}")
        while True:
            while loading:
                try:
                    loadElement = driver.find_element(By.CLASS_NAME, "active")
                    loading = False
                except:
                    pass
            loading = True
            try:
                table = driver.find_element(By.XPATH, f'//*[@id="main"]/div[2]/div/div[3]/table/tbody/tr[{tableCount}]/td[1]/a')
            except:
                break
            link = table.get_attribute("href")

            driver.execute_script(f"window.open('about:blank', '{tableCount}');")
            driver.switch_to.window(f"{tableCount}")
            driver.get(link)

            button = driver.find_element(By.XPATH, '//*[@id="download_form"]/button')
            button.click()
            try:
                contButton = driver.find_element(By.XPATH, '//*[@id="tooltip4"]/tbody/tr/td/div/input')
                contButton.click()
            except:
                pass

            while downloading:
                for files in os.listdir("//TRUENAS/Games/Downloads"):
                    if files.endswith(".zip") or files.endsiwth(".7z"):
                        fileName = files
                        downloading = False
            
            try:
                shutil.move(f"//TRUENAS/Games/Downloads/{fileName}", f"//TRUENAS/Games/Vimmslair_Archive/{items}")
            except:
                downloading = True
                driver.close()
                driver.switch_to.window(f"{letter}")
                tableCount += 1

            downloading = True

            driver.close()
            driver.switch_to.window(f"{letter}")
            tableCount += 1

        #driver.close()