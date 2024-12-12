'''
    This is the program that backs up photos and does video processing

'''

import requests
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "api.env"))

LOCK_FILE = "api.lock"

def delete(filename: str):
    response = requests.get(f"{url}/delete/{filename}")
    if response == 404:
        pass                ######### tkinter error
    elif response == 401:
        pass                ######### tkinter error

def downloadPhoto(filename: str):
    header = {'X-API-KEY':key}
    response = requests.get(f"{url}/{filename}", headers=header)
    if response == 200:
        with open(f"{FILE_DIR}/{filename}", "wb") as f:
            f.write(response.content)
        delete(filename)
    elif response == 404:
        pass                ########## tkinter error
    elif response == 401:
        pass                ########## tkinter error

def checkBackupStatus():
    response = requests.get(f"{url}/status")
    if response == 200:
        data = response.json()
        if data["original"] != "": downloadPhoto(data["original"])
        if data["processed"] != "": downloadPhoto(data["processed"])
    elif response == 404:
        pass                ########## tkinter error

def processVideo():
    pass

def uploadVideo():
    pass

def compressVideo():
    pass

# use tkinter to give an error popup -- program should be running as a background task
def displayError(errorCode: int):
    pass

def isLocked() -> bool:
    if os.path.exists(LOCK_FILE): return True
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return False

def cleanup():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

if __name__ == "__main__":

    if isLocked(): exit(0)

    try:
        key = os.getenv("API_KEY")
        url = os.getenv("URL")
        FILE_DIR = os.getenv("FILE_DIR")
    except Exception as e:
        print(f"An Error Occured: {e}")
    finally:
        cleanup()