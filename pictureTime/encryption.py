from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import json
import os
import bcrypt
from flask import current_app

#PATH = __file__.rsplit("\\", 1)[0]

def loadUser():
    with open(f"{current_app.config['DATA_FOLDER']}/users.json") as f:
        return json.load(f)

def genHash(password):
    hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashedPasswordBase64 = base64.b64encode(hashedPassword).decode('utf-8')
    return hashedPasswordBase64

def checkPassword(password, hash):
    hashed = base64.b64decode(hash)
    return bcrypt.checkpw(password.encode(), hashed)

if __name__ == "__main__":
    #setupJsonFile(f"{PATH}\\data\\users.json")
    hash = genHash(" ")
    print(hash)
    #print(checkPassword("this is aa test", hash))