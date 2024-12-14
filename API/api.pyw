'''
    This is the program that backs up photos and does video processing

'''

import requests
from dotenv import load_dotenv
import os
import cv2
import numpy as np

load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "api.env"))

LOCK_FILE = "api.lock"

def delete(filename: str):
    header = {"X-API-KEY":key}
    response = requests.get(f"{url}/delete/{filename}", headers=header)
    if response == 404:
        pass                ######### tkinter error
    elif response == 401:
        pass                ######### tkinter error

def downloadPhoto(filename: str, original: bool):
    header = {'X-API-KEY':key}
    response = requests.get(f"{url}/{filename}", headers=header)
    if response.status_code == 200:
        if original:
            with open(f"{ORIGIN_DIR}/{filename}", "wb") as f: f.write(response.content)
        else:
            with open(f"{PROC_DIR}/{filename}", "wb") as f: f.write(response.content)
        delete(filename)
    elif response == 404:
        pass                ########## tkinter error
    elif response == 401:
        pass                ########## tkinter error

def checkBackupStatus():
    response = requests.get(f"{url}/status")
    if response.status_code == 200:
        data = response.json()
        for item in data["original"]: downloadPhoto(item, True)
        for item in data["processed"]: downloadPhoto(item, False)
        return data["processed"]
    elif response == 404:
        pass                ########## tkinter error

#def processVideo():
#    imgs = os.listdir(FILE_DIR)

def appendVideo(processedFiles: list):
    if os.path.exists(f"{VIDEO_DIR}/out.mp4"):
        compileNewVideo()
    else:
        #os.rename(f"{VIDEO_DIR}/out.mp4", f"{VIDEO_DIR}/old.mp4")
        cap = cv2.VideoCapture(f"{VIDEO_DIR}/out.mp4")
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(f"{VIDEO_DIR}/new.mp4", fourcc, fps, (w, h))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        for newFrame in processedFiles:
            img = cv2.imread(f"{PROC_DIR}/{newFrame}")
            out.write(img)
        cap.release()
        out.release()
        os.remove(f"{VIDEO_DIR}/out.mp4")
        os.rename(f"{VIDEO_DIR}/new.mp4", f"{VIDEO_DIR}/out.mp4")
    

def compileNewVideo():
    """
    Compile all processed images into a video. All images must be number 1 - ... with the png file extension
    """
    count = 0
    first = True
    h, w = 0, 0
    files = sorted(os.listdir(ORIGIN_DIR), key=lambda x: int(os.path.splitext(x)[0]))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    while True:
        try:
            img = cv2.imread(f"{ORIGIN_DIR}/{count}.png")
            count += 1
            print(f"{count} images processed")
            if first:
                h, w, _ = img.shape
                out = cv2.VideoWriter(f"{VIDEO_DIR}/out.mp4", fourcc, 20, (w, h))
                first = False

            if img is None:
                raise FileNotFoundError(f"Image {count}.png could not be read. Skipping.")
            
            imgResized = videoCrop(img, (h, w))
            out.write(imgResized)

        except Exception as e:
            if count>= int(files[-1].split(".")[0]): break
            #displayError(e) ## doesn't except e as a value, fix that
    
    out.release()

def videoCrop(img, targetSize: tuple):
    tH, tW = targetSize
    h, w = img.shape[:2]

    if w < tW or h < tH:
        canvas = np.zeros((tH, tW, 3), dtype=np.uint8)
        xOffset = (tW - w) // 2
        yOffset = (tH - h) // 2
        canvas[yOffset:yOffset + h, xOffset:xOffset + w] = img
        return canvas
    
    elif w > tW or h > tH:
        xStart = (w - tW) // 2
        yStart = (h - tH) // 2
        cropped = img[yStart:yStart + tH, xStart:xStart + tW]
        return cropped
    
    return img

def uploadVideo():
    header = {'X-API-KEY':key}
    with open(f"{VIDEO_DIR}/out.mp4", 'rb') as f:
        file = {'file': f}
    requests.post(f"{url}/upload-video", headers=header, files=file)

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

def main():
    try: 
        processed: list = checkBackupStatus()
        appendVideo(processed)
    except Exception as e: print(f"Failed to connect to the server\nError: {e}")

if __name__ == "__main__":
    if isLocked(): 
        exit(0)

    try:
        key = os.getenv("API_KEY")
        url = os.getenv("URL")
        ORIGIN_DIR = os.getenv("ORIGINAL_DIR")
        PROC_DIR = os.getenv("PROCESSED_DIR")
        VIDEO_DIR = os.getenv("VIDEO_DIR")
        main()
    except Exception as e:
        pass                ############ show error message on tkinter window
        print(e)
    finally:
        cleanup()