import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import json
import os
import time
#import av
from flask import current_app

'''
USES MEDIAPIPE V0.10.14
'''

mpFaceMesh = mp.solutions.face_mesh
mpDrawing = mp.solutions.drawing_utils

#PATH = __file__.rsplit("\\", 1)[0].replace("\\","/")

def loadJson(filename=str, key=str):
    """
    Open the info.json file

    Parameters:
        key (str): Choose which value in the JSON to return; input "" to return the full JSON file

    Returns a dictionary with the JSON data
    """
    with open(f"{current_app.config['DATA_FOLDER']}/{filename}.json") as f:
        if key != "":
            return json.load(f)[key]
        else:
            return json.load(f)

def setPhotoNum(number=int):
    """
    Set the photo number in the info.json file

    Parameters:
        number (int): The new value of photo_number in info.json
    """
    with open(f"{current_app.config['DATA_FOLDER']}/info.json", "r") as f:
        data = json.load(f)
    data['photo_number'] = number

    with open(F"{current_app.config['DATA_FOLDER']}/info.json", "w") as f:
        json.dump(data, f, indent=4)

def setInfoStatus(jsonKey=str, newValue=str, deleteNewValue=bool):
    """
    Set info for the status.json file; used for download bot to backup photos. All key values have to be lists.

    Parameters:
        jsonKey (str): The json value you want to change
        newValue (str): Appends newValue to the key list
        deleteNewValue (bool): Deletes newValue from the key list instead of appending it
    """
    with open(f"{current_app.config['DATA_FOLDER']}/status.json", "r") as f:
        data = json.load(f)

    keyData: list = data[jsonKey]
    if deleteNewValue:
        keyData.remove(newValue)
    else:
        keyData.append(newValue)
    data[jsonKey] = keyData

    with open(f"{current_app.config['DATA_FOLDER']}/status.json", "w") as f:
            json.dump(data, f, indent=4)

"""
    Mass Image Processing From Local Folders To Number Images By Date
"""
def addDate(date=str) -> str:
    """
    Moves a date to the next day. Will change the month and year accordingly

    Parameters:
        date (str): Date to have a day added to; should be inputed in this format "year-month-day"; day and month must be 2 digits with a 0 if less than 10

    returns the new date as a string
    """
    year, month, day = list(map(int, date.split("-")))
    day += 1

    if month == 2:
        if day > 29:
            day = 1
            month = 3
    
    elif (month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12):
        if day > 31:
            day = 1
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
    
    else:
        if day > 30:
            day = 1
            month += 1
    
    if month < 10: month = f"0{month}"
    if day < 10: day = f"0{day}"

    return str(f"{year}-{month}-{day}")

def convert(inputFile=str, outputFile=str):
    """
    Save an image as a png

    Parameters:
        inputFile (str): File path of the image to be converted
        outputFile (str): File path of the converted png
    """
    # Open the image
    with Image.open(inputFile) as img:
        # Save it as a PNG file
        img.save(outputFile, format='png')

def getFiles(folderInput=str) -> dict:
    """
    Get all files in a folder; creates a dictionary with the date the photo was taken (from the name of the file) and the full image name as the output of the dictionary

    Parameters:
        folderInput (str): The folder to be indexed

    returns the dictinoary
    """
    files = os.listdir(folderInput)
    dic = {}
    for i, item in enumerate(files):
        #files[i] = [item, f"{item[3:7]}-{item[7:9]}-{item[9:11]}"]
        dic[f"{item[3:7]}-{item[7:9]}-{item[9:11]}"] = item

    return dic

def numberPhotos(startNumber=int, startDate=list, endDate=list, folderInputPath=str, folderOutputPath=str):
    """
    Inputs a folder of images and outputs all photos renamed in order of their date.\nThis requires that the photo name is in this format:\nIMG20240922....(fileExtension)

    Parameters:
        startNumber (int): The number you want the function to start counting at when outouting images
        startDate (list): A list with the date of the first image to start indexing on; should be in this format: [year (int), month (int), day (int)]
        endDate (list): A list with the date of the last image to end the function; should be in this format: [year (int), month (int), day (int)]
        folderInputPath (str): The folder path with all images to be processed
        FolderOutputPath (str): The folder path that will have all the outputed images
    """
    files = getFiles(folderInputPath)
    date = "-".join(startDate)
    endDate = "-".join(endDate)
    
    while True:
        time.sleep(.01)
        try:
            imgName = files[date]
            convert(f"{folderInputPath}/{imgName}", f"{folderOutputPath}/{startNumber}.png")
            startNumber += 1
            #print(date, "    ", imgName)
            date = addDate(date)
            if date == endDate: break
            #print(date)
        except:# Exception as e:
            date = addDate(date)
            if date == endDate: break

"""
    Processing Faces, Resizing, and Aligning Images
"""
def processFace(img=np.ndarray, imgRGB=np.ndarray) -> tuple:
    """
    Returns coordinates of the left and right eyes on the inputed image

    Parameters:
        img (np.ndarray): original image open with opencv
        imgRGB(np.ndarray): original image process with cv2.cvtColor() with COLOR_BGR2RGB
        
    Returns:
        leftEye (tuple): x and y coords of left eye
        rightEye (tuple): x and y coords of right eye
    """
    with mpFaceMesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as faceMesh:
        out = faceMesh.process(imgRGB)

        if out.multi_face_landmarks:
            for landmarks in out.multi_face_landmarks:
                leftEye = (int((landmarks.landmark[130].x * img.shape[1] + landmarks.landmark[243].x * img.shape[1]) / 2), int((landmarks.landmark[130].y * img.shape[0] + landmarks.landmark[243].y * img.shape[0]) / 2))
                rightEye = (int((landmarks.landmark[463].x * img.shape[1] + landmarks.landmark[359].x * img.shape[1]) / 2), int((landmarks.landmark[463].y * img.shape[0] + landmarks.landmark[359].y * img.shape[0]) / 2))
    return leftEye, rightEye

def horizontalEyeAlign(img=np.ndarray, deltaX=int, deltaY=int) -> np.ndarray:
    """
    Aligns eyes of a person in an image horizontally

    Parameters:
        img (np.ndarray): Image to be aligned; must be opened using opencv
        deltaX (int): Right eye X coordinate - Left eye X coordinate
        deltaY (int): Right eye Y coordinate - Left eye Y coordinate
    
    Returns an np.ndarray of the aligned image
    """
    angle = np.arctan(deltaY/deltaX)
    angle = (angle * 180) / np.pi

    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))

    return rotated

def resize(img=np.ndarray, dist1=int, deltaX=int, deltaY=int) -> np.ndarray:
    """
    Resizing an image of a face based on eye coordinates

    Parameters:
        img (np.ndarray): Image to be resized; must be accessed using opencv
        dist1 (int): Manueling adjusting the distances between the eyes in the image
        deltaX (int): Right eye X coordinate - Left eye X coordinate
        deltaY (int): Right eye Y coordinate - Left eye Y coordinate
    
    Returns a np.ndarray of the resized image
    """
    dist2 = np.sqrt((deltaX * deltaX) + (deltaY * deltaY))
    ratio = dist1 / dist2

    h, w = img.shape[:2]
    dim = (int(w * ratio), int(h * ratio))
    resized = cv2.resize(img, dim)

    return resized

def processImg(filepath=str):
    """
    Function dedicated to resizing, aligning, and pasting an image of a face onto a large black background

    Parameters:
        filepath (str): File path to the image to be processed
        tempFolder (str): Path to a folder for temporary file storage
        outputFolderOriginal (str): Path to the folder for original photos such as the one opened through filepath; original photos are photos before any processing occurs
        outputFolderResized (str): Path to the folder for the processed images; images that have been rotated, resized, and pasted
        backgroundPath (str): Path to the black 3000x5000 background that the processed image gets pasted onto
    """
    img = cv2.imread(filepath)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    leftEye, rightEye = processFace(img, imgRGB)

    deltaX = rightEye[0] - leftEye[0]
    deltaY = rightEye[1] - leftEye[1]

    rotated = horizontalEyeAlign(img, deltaX, deltaY)
    resized = resize(rotated, 700, deltaX, deltaY)
    
    cv2.imwrite(f"{current_app.config['UPLOAD_FOLDER']}/temp.png", resized)
    resizedRGB = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    leftEye, rightEye = processFace(resized, resizedRGB)
    
    imgPIL = Image.open(f"{current_app.config['DATA_FOLDER']}/tempfiles/temp.png")
    blackBackground = Image.open(f"{current_app.config['DATA_FOLDER']}/3000x5000.png")
    Image.Image.paste(blackBackground, imgPIL, (1200 - leftEye[0], 2500 - leftEye[1]))

    photoNum = loadJson("info", "photo_number")
    setPhotoNum(photoNum + 1)

    #blackBackground.save(f"{current_app.config['FILES_DIRECTORY']}/{photoNum}-processed.png")
    resizeAndCompress(blackBackground, f"{current_app.config['FILES_DIRECTORY']}/{photoNum}-processed.png", 1080)

    while os.path.isfile(f"{current_app.config['FILES_DIRECTORY']}/{photoNum}-processed.png") == False:
        time.sleep(.1)

    #appendFrame(f"{PATH}/static/test.mp4", f"{PATH}/static/test.mp4", f"{PATH}/static/{photoNum}-processed.png")

    ###### CHANGE CODE FOR ADDING FRAME


    os.remove(f"{current_app.config['UPLOAD_FOLDER']}/temp.png")
    os.rename(filepath, f"{current_app.config['FILES_DIRECTORY']}/{photoNum}.png")

    setInfoStatus("original", f"{photoNum}.png", False)
    setInfoStatus("processed", f"{photoNum}-processed.png", False)

def resizeAndCompress(img, output_image_path, max_size=1080):
    """
    
    """
    if img.mode == "RGBA":
        img = img.convert('RGB')

    width, height = img.size
    if width > height:
        new_width = max_size
        new_height = int((max_size / width) * height)
    else:
        new_height = max_size
        new_width = int((max_size / height) * width)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    img.save(output_image_path, format="JPEG", quality=70, optimize=True)

"""
    Video Processing
"""
def compileVideo(framesFolder=str, outputPath=str, fps=int):
    """
    Compile all processed images into a video. All images must be number 1 - ... with the png file extension

    Parameters:
        framesFolder (str): File path to the folder with all video frames; frames must be png's number 1 - ...
        outputPath (str): File path to save the video to
        fps (int): Frames per second
    """
    frameCount = len(os.listdir(framesFolder))
    h, w = 5000, 3000

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(outputPath, fourcc, fps, (w, h))

    for i in range(frameCount):
        frame = cv2.imread(os.path.join(framesFolder), f"{i+1}.png")
        videoWriter.write(frame)

    videoWriter.release()

'''
def appendFrame(videoPath=str, outputPath=str, framePath=str):
    """
    Append a single frame to the end of a mp4 video. Used for adding another processed image to the face timelapse

    Parameters:
        videoPath (str): Path to the mp4 that have a frame added to it
        outputPath (str): Output path for the new video (probably the same as the videoPath)
        framePath (str): Path to the frame to be added to the video
    """
    inputContainer = av.open(videoPath)
    videoStream = inputContainer.streams.video[0]

    outputContainer = av.open(outputPath, mode='w')
    outputStream = outputContainer.add_stream('h264', rate=videoStream.rate)

    for frame in inputContainer.decode(videoStream):
        outputContainer.mux(frame)

    frameToAppend = cv2.imread(framePath)
    frameToAppend = cv2.cvtColor(frameToAppend, cv2.COLOR_BGR2RGB)
    frameToAppend = av.VideoFrame.from_ndarray(frameToAppend, format="rgb24")

    outputContainer.mux(frameToAppend)
    
    inputContainer.close()
    outputContainer.close()
    '''


"""
    Processing All Original Photos
"""
'''
def processAllOriginals():
    """
    Process all original photos using processImg() and output them all into the specified output folder

    Parameters:
        inputFolder (str): The folder with all the original photos to be processed
        outputFolder (str): The folder to put all processed photos
    """
    tempFolder = f"{PATH}/data/tempfiles"
    outputFolderOriginal = f"{PATH}/data/permfiles/original"
    outputFolderResized = f"{PATH}/data/permfiles/resized"
    background = f"{PATH}/data/3000x5000.png"

    fileCount = len(os.listdir(outputFolderOriginal))    

    for i in range(fileCount):
        processImg(f"{outputFolderOriginal}/{i+1}.png", tempFolder, outputFolderOriginal, outputFolderResized, background)
'''
        
if __name__ == "__main__":
    #filePath = f"{PATH}/data/tempfiles/" + os.listdir(f"{PATH}/data/tempfiles")[0]
    #processImg(filepath=f"{PATH}/data/tempfiles/f.jpg")
    #compileVideo(f"{PATH}/data/permfiles/resized", f"{PATH}", 30)
    print(loadJson(""))