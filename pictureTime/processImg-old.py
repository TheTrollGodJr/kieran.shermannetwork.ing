import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw
import json
import os

'''
USES MEDIAPIPE V0.10.14
'''

mpFaceMesh = mp.solutions.face_mesh
mpDrawing = mp.solutions.drawing_utils

PATH = __file__.rsplit("\\", 1)[0].replace("\\", "/")

def getPhotoNum():
    with open(f"{PATH}/data/info.json", "r") as f:
        data = json.load(f)
    photoNum = data['photo_number']
    data['photo_number'] = photoNum + 1

    with open(f"{PATH}/data/info.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return photoNum

def paste_image(base_image, overlay_image, position):
    """
    Paste the overlay_image onto the base_image at the specified position,
    clipping any part of the overlay_image that is outside the base_image dimensions.
    
    :param base_image: The base image on which to paste the overlay image.
    :param overlay_image: The image to be pasted onto the base image.
    :param position: The (x, y) position to paste the overlay image on the base image.
    """
    x, y = position
    h, w = overlay_image.shape[:2]

    # Calculate the region of interest (ROI) on the base image
    x_start = max(0, x)
    y_start = max(0, y)
    x_end = min(x + w, base_image.shape[1])
    y_end = min(y + h, base_image.shape[0])

    # Calculate the dimensions of the part of the overlay image to be pasted
    overlay_x_start = max(0, -x)
    overlay_y_start = max(0, -y)
    overlay_x_end = x_end - x_start
    overlay_y_end = y_end - y_start

    # Clip the overlay image to fit within the bounds of the base image
    clipped_overlay = overlay_image[overlay_y_start:overlay_y_start + overlay_y_end, 
                                    overlay_x_start:overlay_x_start + overlay_x_end]

    # Place the clipped overlay image onto the base image
    base_image[y_start:y_end, x_start:x_end] = clipped_overlay

    return base_image

def processImg(filepath):
    img = cv2.imread(filepath)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mpFaceMesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as faceMesh:
        out = faceMesh.process(imgRGB)

        if out.multi_face_landmarks:
            for landmarks in out.multi_face_landmarks:
                leftEye = (int((landmarks.landmark[130].x * img.shape[1] + landmarks.landmark[243].x * img.shape[1]) / 2), int((landmarks.landmark[130].y * img.shape[0] + landmarks.landmark[243].y * img.shape[0]) / 2))
                rightEye = (int((landmarks.landmark[463].x * img.shape[1] + landmarks.landmark[359].x * img.shape[1]) / 2), int((landmarks.landmark[463].y * img.shape[0] + landmarks.landmark[359].y * img.shape[0]) / 2))

    #cv2.circle(img, rightEye, 30, (0, 255, 0), 3)
    #cv2.circle(img, leftEye, 30, (0, 255, 0), 3)
    print(leftEye, rightEye)

    #cv2.imwrite(f"{PATH}/data/tempfiles/out.png", img)
    #return
    deltaX = rightEye[0] - leftEye[0]
    deltaY = rightEye[1] - leftEye[1]
    angle = np.arctan(deltaY/deltaX)
    angle = (angle * 180) / np.pi

    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))

    #dist1 = 455.0890022841686
    dist1 = 800
    dist2 = np.sqrt((deltaX * deltaX) + (deltaY * deltaY))
    ratio = dist1 / dist2

    dim = (int(w * ratio), int(h * ratio))
    resized = cv2.resize(rotated, dim)
    imgRGB = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    with mpFaceMesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as faceMesh:
        out = faceMesh.process(imgRGB)

        if out.multi_face_landmarks:
            for landmarks in out.multi_face_landmarks:
                leftEye = (int((landmarks.landmark[130].x * img.shape[1] + landmarks.landmark[243].x * img.shape[1]) / 2), int((landmarks.landmark[130].y * img.shape[0] + landmarks.landmark[243].y * img.shape[0]) / 2))
                rightEye = (int((landmarks.landmark[463].x * img.shape[1] + landmarks.landmark[359].x * img.shape[1]) / 2), int((landmarks.landmark[463].y * img.shape[0] + landmarks.landmark[359].y * img.shape[0]) / 2))

    print(leftEye, rightEye)

    #img = Image.open(f"{PATH}/data/tempfiles/resized.png")
    pilImg = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    background = Image.open(f"{PATH}/data/3000x5000.png")
    Image.Image.paste(background, pilImg, (1000 - leftEye[0], 2000 - leftEye[1]))
    draw = ImageDraw.Draw(background)
    draw.ellipse((990,1990, 1010, 2010), fill='red', outline='red')
    #draw.ellipse((1000 - leftEye[0]-20, 2000 - leftEye[1]-20, 1000 - leftEye[0]+20, 2000 - leftEye[1]+20), fill='blue', outline='blue')
    print(1000 - leftEye[0], 2000 - leftEye[1])
    background.save(f"{PATH}/data/tempfiles/{getPhotoNum()}.png")

    '''
    imgRGB = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    with mpFaceMesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as faceMesh:
        out = faceMesh.process(imgRGB)

        if out.multi_face_landmarks:
            for landmarks in out.multi_face_landmarks:
                leftEyeN = (int((landmarks.landmark[130].x * img.shape[1] + landmarks.landmark[243].x * img.shape[1]) / 2), int((landmarks.landmark[130].y * img.shape[0] + landmarks.landmark[243].y * img.shape[0]) / 2))
                rightEyeN = (int((landmarks.landmark[463].x * img.shape[1] + landmarks.landmark[359].x * img.shape[1]) / 2), int((landmarks.landmark[463].y * img.shape[0] + landmarks.landmark[359].y * img.shape[0]) / 2))

    blackScreen = np.zeros((5000, 3000, 3), dtype=np.uint8)
    
    
    xOffset = (1000 - leftEye[0]) + leftEye[0]
    yOffset = (1500 - leftEye[1]) + leftEye[1]
    
    h, w, _ = resized.shape

    blackScreen[yOffset:yOffset + h, xOffset:xOffset + w] = resized
    
    x_start = max(0, -xOffset)
    y_start = max(0, -yOffset)
    x_end = min(resized.shape[1], blackScreen.shape[1] - xOffset)
    y_end = min(resized.shape[0], blackScreen.shape[0] - yOffset)

    cropped_resized = resized[y_start:y_end, x_start:x_end]

    # Calculate the position to place the cropped resized image on the black screen
    new_xOffset = max(0, xOffset)
    new_yOffset = max(0, yOffset)

    # Place the cropped resized image on the black screen
    blackScreen[new_yOffset:new_yOffset + cropped_resized.shape[0], new_xOffset:new_xOffset + cropped_resized.shape[1]] = cropped_resized
    
    print(leftEye)
    blackScreen = paste_image(blackScreen, resized, (leftEye[0],leftEye[1]))
    cv2.circle(blackScreen, (1000,1500), 10, (255, 0, 0), 3)
    cv2.circle(blackScreen, leftEye, 10, (255, 0, 0), 3)
    cv2.imwrite(f"{PATH}/data/tempfiles/{getPhotoNum()}.png", blackScreen)
    '''



if __name__ == "__main__":
    #filePath = f"{PATH}/data/tempfiles/" + os.listdir(f"{PATH}/data/tempfiles")[0]
    processImg(filepath=f"{PATH}/data/tempfiles/e.jpg")