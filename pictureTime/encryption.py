from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import json
import os
import bcrypt

PATH = __file__.rsplit("\\", 1)[0]

def setupJsonFile(file_path):
    default_content = {"users": [{"username": "guest","password_hash": "JDJiJDEyJE1NVVg4REIxa2tBR3ZGYjNZQmI0eWVYTy9iNVp2Wm0yU1ZWL2JDT056a0E1blFvVnVOTC5x"}]}
    if not os.path.exists(f"{PATH}\\data"): 
        os.mkdir(f"{PATH}\\data")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump(default_content, file, indent=4)

def loadUser():
    with open(f"{PATH}\\data\\users.json") as f:
        return json.load(f)['users']

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