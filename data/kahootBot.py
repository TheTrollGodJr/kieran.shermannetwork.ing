#run 'pip install selenium' in cmd before running code
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import random
import time

gamePin = input("Enter Kahoot Game Pin:\n")
totalBots = int(input("How many bots do you want to add?\n"))
threadBotCount = str(totalBots / 3)[0]
remainder = totalBots % 3
browserOpen = True

if totalBots < 3:
    print("You must use at least 3 bots")
    exit(1)

def runBot(total):
    count = 0
    loading = True

    while count < int(total) + 1:

        if count == 0:
            driver = webdriver.Chrome()
            driver.get(f"https://kahoot.it/?pin={gamePin}&refer_method=link")
        else:
            driver.execute_script(f"window.open('about:blank', '{count}');")
            driver.switch_to.window(f"{count}")
            driver.get(f"https://kahoot.it/?pin={gamePin}&refer_method=link")

        while loading:
            try:
                textBox = driver.find_element(By.ID, "nickname")
                loading = False
            except:
                pass

        textBox = driver.find_element(By.ID, "nickname")
        button = driver.find_element(By.CLASS_NAME, "nickname-form__SubmitButton-sc-1mjq176-1")

        textBox.send_keys(str(random.randrange(5000)))
        button.click()

        count += 1
        loading = True

    while browserOpen:
        time.sleep(1)


if remainder > 0:
    arg = threadBotCount + 1
    t1 = threading.Thread(target=runBot, args=(arg,))
    remainder -= 1
else:
    t1 = threading.Thread(target=runBot, args=(threadBotCount,))

if remainder > 0:
    arg = threadBotCount + 1
    t2 = threading.Thread(target=runBot, args=(arg,))
    remainder -= 1
else:
    t2 = threading.Thread(target=runBot, args=(threadBotCount,))

if remainder > 0:
    arg = threadBotCount + 1
    t3 = threading.Thread(target=runBot, args=(arg,))
    remainder -= 1
else:
    t3 = threading.Thread(target=runBot, args=(threadBotCount,))


t1.start()
t2.start()
t3.start()

time.sleep(1)
wait = input("Press enter to close Browsers")
browserOpen = False

t1.join()
t2.join()
t3.join()