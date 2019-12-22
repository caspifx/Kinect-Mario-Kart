import cv2
import numpy as np
import time

def get_video_webcam():
    cap  = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Web Cam", frame)
        slice(frame,2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def crop(img, splitby):
    img2 = img
    height, width, channels = img.shape
    # Number of pieces Horizontally
    CROP_W_SIZE = splitby
    # Number of pieces Vertically to each Horizontal
    CROP_H_SIZE = 1
    imgs = []
    for ih in range(CROP_H_SIZE):
        for iw in range(CROP_W_SIZE):
            x = width / CROP_W_SIZE * iw
            y = height / CROP_H_SIZE * ih
            h = (height / CROP_H_SIZE)
            w = (width / CROP_W_SIZE)
            print(type(img))
            img = img[y:y + h, x:x + w]
            imgs.append(img)
            img = img2
    return imgs


def slice(img,sliceby):
    imgs = []
    height, width = img.shape[:2]
    for i in range(sliceby):
        start_row, start_col = int(0), int(width/sliceby) * i
        end_row, end_col = int(height), int(width / sliceby) + start_col
        cropped = img[start_row:end_row, start_col:end_col]
        imgs.append(cropped)
    return imgs


if __name__ == '__main__':
    get_video_webcam()
