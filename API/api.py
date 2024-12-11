'''
    This is the program that backs up photos and does video processing

'''

import requests
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.env"))

def getBackupPhotos():
    pass

def checkBackupStatus():
    pass

def processVideo():
    pass

def uploadVideo(apiKey: str):
    pass

def compressVideo():
    pass

# use tkinter to give an error popup -- program should be running as a background task
def displayError():
    pass

if __name__ == "__main__":
    key = os.getenv("API_KEY")