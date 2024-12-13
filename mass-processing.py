'''
    This program is built to process large amounts of images from before using the website
'''

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import argparse
import os

mpFaceMesh = mp.solutions.face_mesh
mpDrawing = mp.solutions.drawing_utils

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
    
    resizedRGB = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    leftEye, rightEye = processFace(resized, resizedRGB)

    imgPIL = Image.fromarray(resizedRGB)
    blackBackground = Image.new("RGB", (3000, 5000), (0,0,0))
    Image.Image.paste(blackBackground, imgPIL, (1200 - leftEye[0], 2500 - leftEye[1]))
    
    resizeAndCompress(blackBackground, f"{args.output_dir}/processed.png", 1080)




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

def getDate(filename: str, method: str) -> tuple:
    date = ""
    if method == "date-ISO":
        for char in filename:
            if char.isdigit(): 
                date += char
                if len(date) == 4 or len(date) == 7: date += "-"
            if len(date) == 10: break
        return (filename, date)

    elif method == "date-metadata":
        pass

def sortFiles(files: list, method: str) -> dict:
    data = {}
    if method == "file-order": return files
    elif method == "date-ISO":
        print("Running ISO sorting")
        for file in files:
            if ".png" in file or ".jpg" in file or ".jpeg" in file:
                pair = getDate(file, method)
                data[pair[0]] = pair[1]
        sortedData = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
        return sortedData

    elif method == "date-metadata":
        pass

def main():
    print("main")
    if args.compile_type == "image":
        print("image")
        files = os.listdir(args.input_dir)
        print(files)
        files = sortFiles(files, args.process_order)
        for file in files.keys():
            processImg(f"{args.input_dir}/{file}")
    else:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("compile_type", choices=["image", "video"], help="Choose whether to mass process images or to compile all processed images into a video.")
    
    parser.add_argument("input_dir", type=str, help="The directory with all the images to compile")
    parser.add_argument("output_dir", type=str, help="The directory to output all images/video")

    parser.add_argument("--filename", "-f", type=str, help="The filename for the video (only do this if you are exporting a video)", required=False)
    parser.add_argument("--process-order", "-p", type=str, choices=["file-order", "date-ISO", "date-metadata"], default="date-ISO", help="Choose in what order to process photos. All processed photos will be numbers 1-x depending on how you process. file-order sorts by the file order on your computer. date-ISO sorts it according to the image name following the universal ISO 8601 format. date-metadata sorts according to the image metadata; if there is none the image will be skipped. The default is date-ISO. This option only applies to image compiling.")
    parser.add_argument("--count-start", "-c", type=int, default=0, help="Choose what number to start on when processing photos. If you have already have numbers, processed photos you can use this to continue from where you ended. This is only used for image compiling.")

    args = parser.parse_args()

    if args.compile_type == "image" and args.filename: 
        parser.error("--filename (-f) is only allowed when compile_type is set to 'video'")
    
    if args.compile_type == "video" and args.process_order:
        parser.error("--process-order (-p) is only allowed when compile_type is set to 'image'")

    if args.compile_type == "video" and args.count_start:
        parser.error("--count-start (-c) is only allowed when compile_type is set to 'image'")
    
    main()